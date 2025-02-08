import pandas as pd


class DataLoader:
    def __init__(self):
        self.root_url = "http://data.gdeltproject.org/events/{DATE}.export.CSV.zip"
        self.columns = ['GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate', 'Actor1Code', 'Actor1Name',
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
                        'SOURCEURL']

        self.selected_columns = ['SQLDATE', 'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode',
                                 'EventCode', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_Lat',
                                 'ActionGeo_Long', 'SOURCEURL']

        self.actor_1_list = None
        self.actor_2_list = None

    def set_actor_filters(self, actor_1_list, actor_2_list):
        self.actor_1_list = actor_1_list
        self.actor_2_list = actor_2_list

    def load_data(self, date):
        url = self.root_url.format(DATE=date)
        df = pd.read_csv(url, sep='\t', header=None)
        df.columns = self.columns

        if self.actor_1_list and self.actor_2_list:
            mask = (df['Actor1Code'].isin(self.actor_1_list)) & (df['Actor2Code'].isin(self.actor_2_list)) | \
                     (df['Actor1Code'].isin(self.actor_2_list)) & (df['Actor2Code'].isin(self.actor_1_list))
            df = df[mask].copy()
        elif self.actor_1_list:
            mask = (df['Actor1Code'].isin(self.actor_1_list)) | (df['Actor2Code'].isin(self.actor_1_list))
            df = df[mask].copy()
        elif self.actor_2_list:
            mask = (df['Actor1Code'].isin(self.actor_2_list)) | (df['Actor2Code'].isin(self.actor_2_list))
            df = df[mask].copy()

        return df

    def load_data_range(self, start_date, end_date):
        data = []
        date_range = [date.strftime("%Y%m%d").replace("-", "") for date in
                      pd.date_range(start=start_date, end=end_date)]
        for date in date_range:
            print(f"Loading data for {date}...")
            data.append(self.load_data(date))

        return pd.concat(data, ignore_index=True)
