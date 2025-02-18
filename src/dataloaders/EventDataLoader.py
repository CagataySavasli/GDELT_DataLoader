import pandas as pd
import streamlit as st

class EventDataLoader:
    def __init__(self):
        st.session_state.setdefault("root_url", "http://data.gdeltproject.org/events/{DATE}.export.CSV.zip")
        st.session_state.setdefault("columns", [
            'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name',
            'Actor1CountryCode', 'Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code',
            'Actor1Religion2Code', 'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 'Actor2Code',
            'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 'Actor2EthnicCode',
            'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type1Code', 'Actor2Type2Code',
            'Actor2Type3Code', 'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',
            'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone', 'Actor1Geo_Type',
            'Actor1Geo_FullName', 'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_Lat',
            'Actor1Geo_Long', 'Actor1Geo_FeatureID', 'Actor2Geo_Type', 'Actor2Geo_FullName',
            'Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long',
            'Actor2Geo_FeatureID', 'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode',
            'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID', 'DATEADDED',
            'SOURCEURL'
        ])
        st.session_state.setdefault("selected_columns", [
            'SQLDATE', 'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode',
            'EventCode', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_Lat',
            'ActionGeo_Long', 'SOURCEURL'
        ])
        st.session_state.setdefault("actor_1_code_list", [])
        st.session_state.setdefault("actor_2_code_list", [])
        st.session_state.setdefault("event_code_list", [])
        st.session_state.setdefault("root_event_code_list", [])

        print("EventDataLoader initialized.")

    def set_actor_filters(self, actor_1_list, actor_2_list):
        st.session_state["actor_1_code_list"] = actor_1_list
        st.session_state["actor_2_code_list"] = actor_2_list

    def set_eventcode_filters(self, event_code_list):
        st.session_state["event_code_list"] = event_code_list

    def set_root_eventcode_filters(self, root_event_code_list):
        st.session_state["root_event_code_list"] = root_event_code_list

    def fix_event_code(self, row):
        if len(row['EventRootCode']) == 1:
            row['EventCode'] = f"0{row['EventCode']}"
            row['EventRootCode'] = f"0{row['EventRootCode']}"
        return row

    def load_data(self, date):
        url = st.session_state["root_url"].format(DATE=date)
        try:
            df = pd.read_csv(url, sep='\t', header=None, low_memory=False)
        except Exception as e:
            st.error(f"Error loading data for {date}: {e}")
            return pd.DataFrame()
        df.columns = st.session_state["columns"]

        df['EventCode'] = df['EventCode'].astype(str)
        df['EventRootCode'] = df['EventRootCode'].astype(str)
        df = df.apply(self.fix_event_code, axis=1)

        actor_1_codes = st.session_state["actor_1_code_list"]
        actor_2_codes = st.session_state["actor_2_code_list"]
        event_codes = st.session_state["event_code_list"]
        root_event_codes = st.session_state["root_event_code_list"]

        if event_codes:
            mask = df['EventCode'].isin(event_codes)
            df = df[mask].copy()

        if root_event_codes:
            mask = df['EventRootCode'].isin(root_event_codes)
            df = df[mask].copy()

        if actor_1_codes and actor_2_codes:
            mask = (
                ((df['Actor1Code'].isin(actor_1_codes)) & (df['Actor2Code'].isin(actor_2_codes))) |
                ((df['Actor1Code'].isin(actor_2_codes)) & (df['Actor2Code'].isin(actor_1_codes)))
            )
            df = df[mask].copy()
        elif actor_1_codes:
            mask = (df['Actor1Code'].isin(actor_1_codes)) | (df['Actor2Code'].isin(actor_1_codes))
            df = df[mask].copy()
        elif actor_2_codes:
            mask = (df['Actor1Code'].isin(actor_2_codes)) | (df['Actor2Code'].isin(actor_2_codes))
            df = df[mask].copy()

        return df

    def load_data_range(self, start_date, end_date):
        data_frames = []
        # Belirtilen tarih aralığındaki tüm tarihleri "YYYYMMDD" formatında elde ediyoruz.
        date_range = [date.strftime("%Y%m%d") for date in pd.date_range(start=start_date, end=end_date)]

        # Progress bar ve mesaj göstermek için alan oluşturuyoruz.
        progress_bar = st.progress(0)
        progress_text = st.empty()  # İlerleme mesajlarını göstermek için boş bir alan.

        total_dates = len(date_range)
        for i, date in enumerate(date_range):
            # İlerleme mesajını güncelleyelim.
            progress_text.text(f"Loading data for {date}...")
            df = self.load_data(date)
            if not df.empty:
                data_frames.append(df)
            # Progress bar'ı güncelle.
            progress_bar.progress((i + 1) / total_dates)

        progress_text.text("Data loading completed!")

        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
        else:
            st.warning("No data loaded for the given date range.")
            return pd.DataFrame()

