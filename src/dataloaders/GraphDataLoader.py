import re
import pandas as pd
import streamlit as st


class GraphDataLoader:
    def __init__(self):
        # Set the default URL in Streamlit's session_state. The URL accepts a date placeholder.
        st.session_state.setdefault("gkg_url", "http://data.gdeltproject.org/gkg/{DATE}.gkg.csv.zip")
        self.data = None
        print("GraphDataLoader has been initialized successfully.")

    def load_data(self, date):
        """
        Loads data for the specified date from the URL and returns it as a DataFrame.
        If an error occurs, an error message is displayed via Streamlit.

        Parameters:
            date (str): Date in 'YYYYMMDD' format.

        Returns:
            pd.DataFrame: The loaded data or an empty DataFrame if an error occurred.
        """
        url = st.session_state["gkg_url"].format(DATE=date)
        try:
            df = pd.read_csv(url, sep='\t', low_memory=False)
        except Exception as e:
            st.error(f"Error while loading data for {date}: {e}")
            return pd.DataFrame()
        return df

    def load_data_range(self, start_date, end_date, keywords):
        """
        Downloads and processes data for a range of dates.
        Progress is displayed via a Streamlit progress bar and status messages.

        Parameters:
            start_date (str or datetime): The start date.
            end_date (str or datetime): The end date.
            keywords (list): List of keywords to filter the 'THEMES' column.
        """
        data_frames = []
        # Create a list of dates in 'YYYYMMDD' format within the specified range.
        date_range = [date.strftime("%Y%m%d") for date in pd.date_range(start=start_date, end=end_date)]

        progress_bar = st.progress(0)
        progress_text = st.empty()
        total_dates = len(date_range)

        for i, date in enumerate(date_range):
            progress_text.text(f"Loading data for date: {date}...")
            df = self.load_data(date).reset_index(drop=True)
            df = self.iterative_filter_data(df, keywords).reset_index(drop=True)
            if not df.empty:
                data_frames.append(df)
            progress_bar.progress((i + 1) / total_dates)

        progress_text.text("Data loading completed successfully!")

        if data_frames:
            self.data = pd.concat(data_frames, ignore_index=True).reset_index(drop=True)
        else:
            st.warning("No data was loaded; the resulting dataset is empty!")
            self.data = pd.DataFrame()

    def get_data_info(self):
        """
        Displays the number of rows and columns in the loaded dataset via Streamlit.
        """
        if self.data is not None:
            rows, columns = self.data.shape
            st.write(f"Data has {rows} rows and {columns} columns.")
        else:
            st.write("Data has not been loaded yet.")

    def filter_data(self, keywords):
        """
        Filters the loaded dataset to include only rows where the 'THEMES' column
        contains any of the specified keywords as separate tokens.

        For example, if 'WAR' is provided as a keyword, it will match entries like
        'WAR_THEME' (where 'WAR' appears as a distinct token) but not 'SOFTWARE'.

        Parameters:
            keywords (list): List of keywords to filter by.
        """
        if self.data is not None and 'THEMES' in self.data.columns:
            # Build regex patterns for each keyword to match as a distinct token
            regex_parts = [fr'(?<=^|_){re.escape(keyword)}(?=$|_)' for keyword in keywords]
            pattern = '|'.join(regex_parts)

            mask = self.data['THEMES'].fillna("").str.contains(pattern, case=False, na=False, regex=True)
            self.data = self.data[mask].copy()
        else:
            st.warning("Data has not been loaded or the 'THEMES' column is missing.")

    def iterative_filter_data(self, df, keywords):
        """
        Filters the given DataFrame to include only rows where the 'THEMES' column
        contains any of the specified keywords as separate tokens.

        For example, if 'WAR' is provided as a keyword, it will accept entries like
        'WAR_THEME' (where 'WAR' appears as a distinct token) but will not match
        strings like 'SOFTWARE'.

        Parameters:
            df (pd.DataFrame): The DataFrame to filter.
            keywords (list): List of keywords to filter by.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        if df is not None and 'THEMES' in df.columns:
            # Build a regex pattern that matches each keyword only if it appears as a separate token.
            # The pattern uses lookbehind and lookahead to ensure the keyword is either at the start/end
            # of the string or preceded/followed by an underscore.
            regex_parts = [fr'(?<=^|_){re.escape(keyword)}(?=$|_)' for keyword in keywords]
            pattern = '|'.join(regex_parts)
            mask = df['THEMES'].fillna("").str.contains(pattern, case=False, na=False, regex=True)
            return df[mask].copy()
        else:
            st.warning("Data is not loaded or the 'THEMES' column is missing.")
            return pd.DataFrame()

    def parse_tone(self, tone_str):
        """
        Parses the value in the TONE column by splitting the string and returning the first value as a float.

        Parameters:
            tone_str (str): The string from the TONE column.

        Returns:
            float or None: The first tone value as a float, or None if parsing fails.
        """
        try:
            return float(tone_str.split(',')[0])
        except Exception:
            return None

    def parse_tone_column(self):
        """
        Processes the TONE column by extracting the first tone value from each entry
        and creating a new column named 'parsed_tone'.
        """
        st.info("Processing the TONE column to extract tone values into 'parsed_tone'.")
        if self.data is not None and 'TONE' in self.data.columns:
            self.data['parsed_tone'] = self.data['TONE'].apply(self.parse_tone)
        else:
            st.warning("Data has not been loaded or the 'TONE' column is missing.")

    def fix_date_column(self):
        """
        Converts the DATE column to datetime objects using the '%Y%m%d' format.
        Invalid dates are removed, and the DATE column is updated to only contain the date part.
        """
        st.info("Processing the DATE column to convert entries to proper datetime objects.")
        if self.data is not None and 'DATE' in self.data.columns:
            # Convert DATE column to datetime, setting errors to NaT for invalid dates.
            self.data['datetime'] = pd.to_datetime(
                self.data['DATE'].astype(str),
                format='%Y%m%d',
                errors='coerce'
            )
            # Remove rows with invalid dates.
            self.data = self.data.dropna(subset=['datetime'])
            # Update the DATE column to contain only the date (without time).
            self.data['DATE'] = self.data['datetime'].dt.date
            self.data.drop(columns=['datetime'], inplace=True)
        else:
            st.warning("Data has not been loaded or the 'DATE' column is missing.")

    def get_data(self):
        """
        Returns the processed dataset.

        Returns:
            pd.DataFrame: The processed data.
        """
        return self.data

    def data_pipeline(self, start_date, end_date, keywords):
        """
        Executes the full data processing pipeline:
            1. Downloads data for the specified date range.
            2. Filters the data based on keywords in the 'THEMES' column.
            3. Processes the TONE column to extract tone values.
            4. Converts and cleans the DATE column.

        Parameters:
            start_date (str or datetime): The start date for data loading.
            end_date (str or datetime): The end date for data loading.
            keywords (list): List of keywords for filtering the 'THEMES' column.

        Returns:
            pd.DataFrame: The fully processed data.
        """
        self.load_data_range(start_date, end_date, keywords)
        self.filter_data(keywords)
        self.parse_tone_column()
        self.fix_date_column()
        return self.get_data()
