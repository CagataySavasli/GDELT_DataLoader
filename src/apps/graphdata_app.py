import streamlit as st
from src.dataloaders.GraphDataLoader import GraphDataLoader
import io
import zipfile
import pandas as pd
from datetime import date, timedelta


class GraphData_APP:
    def __init__(self):
        st.session_state["data_loader"] = GraphDataLoader()
        st.session_state.setdefault("start_date", None)
        st.session_state.setdefault("end_date", None)
        st.session_state.setdefault("data", None)
        st.session_state.setdefault("keywords", "")

    def how_to_use(self):
        st.title("📖 How to Use Graph Data Loader")
        st.markdown(
            """
            This application allows you to scrape GKG (Global Knowledge Graph) data from [GDELT](http://data.gdeltproject.org/gkg/) 
            based on a selected date range and filter it using keywords in the **THEMES** column.
            """
        )

        st.header("1️⃣ Select a Date Range")
        st.markdown(
            """
            - In the **"Date Range"** section, choose a **Start Date** and an **End Date**.
            - The application will download GDELT GKG data for all dates within the selected range.
            """
        )

        st.header("2️⃣ Filter by Keywords (Optional)")
        st.markdown(
            """
            - Enter one or more keywords (separated by commas) to filter the data by the **THEMES** column.
            - If no keywords are entered, the data will include all records.
            """
        )

        st.header("3️⃣ Load Data")
        st.markdown(
            """
            - Click the **"Load Data"** button to start retrieving data from GDELT.
            - A progress bar will indicate the download progress.
            - Once the data is loaded, the application will display the number of records retrieved.
            """
        )

        st.header("4️⃣ Download Data")
        st.markdown(
            """
            - After data is loaded, click **"Download Data as ZIP"** to download the filtered data.
            - The downloaded file will contain a CSV file (`data.csv`) with the processed GKG records.
            """
        )

        st.markdown("---")
        st.subheader("⚠️ Notes")
        st.markdown(
            """
            - The application fetches data from **GDELT in CSV format**.
            - Filtering is performed on the **THEMES** column using the provided keywords.
            - If you don’t select a date range, **no data will be loaded**.
            - Errors may occur if GDELT data is unavailable for certain dates.

            Happy data exploration! 🚀
            """
        )

    def get_dates(self):
        st.write(
            "Please select the date range for which you want to load GDELT GKG data."
        )
        # Varsayılan olarak son 7 gün verilerini seçmek için
        st.session_state["start_date"] = st.date_input("Start Date", value=date.today() - timedelta(days=7))
        st.session_state["end_date"] = st.date_input("End Date", value=date.today() - timedelta(days=1))
        st.session_state["keywords"] = st.text_input("Enter keywords for filtering (comma-separated)", value="")

    def load_data(self):
        start_date = st.session_state.get("start_date")
        end_date = st.session_state.get("end_date")
        keywords = st.session_state.get("keywords")
        data_loader = st.session_state.get("data_loader")

        if start_date is None or end_date is None:
            st.warning("Please select both start and end dates!")
            return

        # İşlenmek üzere anahtar kelimeleri temizleyip listeye dönüştürelim.
        keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()] if keywords else []

        try:
            # data_pipeline, veriyi indirip filtreleyip, TONE ve DATE sütunlarını işler.
            data = data_loader.data_pipeline(start_date, end_date, keyword_list)
        except AttributeError as e:
            st.error("Data loader encountered an attribute error. Please check your configuration.")
            st.error(str(e))
            return
        except Exception as e:
            st.error("An unexpected error occurred while loading data.")
            st.error(str(e))
            return

        st.session_state["data"] = data
        st.write(f"Loaded {len(data)} records.")

    def download_data_button(self):
        data = st.session_state.get("data")
        if data is not None and not data.empty:
            csv_data = data.to_csv(index=False).encode("utf-8")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("data.csv", csv_data)
            zip_buffer.seek(0)
            st.download_button(
                label="Download Data as ZIP",
                data=zip_buffer,
                file_name="data.zip",
                mime="application/zip"
            )
        else:
            st.info("No data loaded! Please load the data first.")
