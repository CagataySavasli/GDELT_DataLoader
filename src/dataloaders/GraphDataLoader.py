import pandas as pd
import streamlit as st


class GraphDataLoader:
    def __init__(self):
        # Streamlit session_state üzerinden varsayılan URL tanımlanıyor.
        st.session_state.setdefault("gkg_url", "http://data.gdeltproject.org/gkg/{DATE}.gkg.csv.zip")
        self.data = None
        print("GraphDataLoader initialized.")

    def load_data(self, date):
        """
        Belirtilen tarih için veriyi URL'den çekip DataFrame olarak döndürür.
        Hata oluşursa Streamlit üzerinden hata mesajı gösterir.
        """
        url = st.session_state["gkg_url"].format(DATE=date)
        try:
            df = pd.read_csv(url, sep='\t', low_memory=False)
        except Exception as e:
            st.error(f"{date} tarihli veriler yüklenirken hata oluştu: {e}")
            return pd.DataFrame()
        return df

    def load_data_range(self, start_date, end_date, keywords):
        """
        Belirtilen tarih aralığındaki verileri yükler. 
        Streamlit progress bar ve mesajlarıyla indirme süreci takip edilir.
        """
        data_frames = []
        # Tarih aralığını "YYYYMMDD" formatında oluşturuyoruz.
        date_range = [date.strftime("%Y%m%d") for date in pd.date_range(start=start_date, end=end_date)]

        progress_bar = st.progress(0)
        progress_text = st.empty()
        total_dates = len(date_range)

        for i, date in enumerate(date_range):
            progress_text.text(f"{date} tarihli veriler yükleniyor...")
            df = self.load_data(date)
            df = self.iterative_filter_data(df, keywords)
            if not df.empty:
                data_frames.append(df)
            progress_bar.progress((i + 1) / total_dates)

        progress_text.text("Veri yükleme tamamlandı!")

        if data_frames:
            self.data = pd.concat(data_frames, ignore_index=True)
        else:
            st.warning("Verilen tarih aralığı için hiç veri yüklenemedi.")
            self.data = pd.DataFrame()

    def get_data_info(self):
        """
        Yüklenen veri kümesinin satır ve sütun sayısını Streamlit üzerinden bildirir.
        """
        if self.data is not None:
            st.write(f"Veri kümesinde {self.data.shape[0]} satır ve {self.data.shape[1]} sütun mevcut.")
        else:
            st.write("Veri kümesi henüz yüklenmedi.")

    def filter_data(self, keywords):
        """
        'THEMES' sütununda verilen anahtar kelimeleri içeren satırları filtreler.
        """
        if self.data is not None and 'THEMES' in self.data.columns:
            mask = self.data['THEMES'].fillna("").str.contains('|'.join(keywords), case=False, na=False)
            self.data = self.data[mask].copy()
        else:
            st.warning("Veri yüklenmedi veya 'THEMES' sütunu mevcut değil.")

    def iterative_filter_data(self, df, keywords):
        """
        'THEMES' sütununda verilen anahtar kelimeleri içeren satırları filtreler.
        """
        if df is not None and 'THEMES' in df.columns:
            mask = df['THEMES'].fillna("").str.contains('|'.join(keywords), case=False, na=False)
            df = df[mask].copy()
            return df
        else:
            st.warning("Veri yüklenmedi veya 'THEMES' sütunu mevcut değil.")

    def parse_tone(self, tone_str):
        """
        TONE sütunundaki değeri parçalayarak ilk değeri float olarak döndürür.
        """
        try:
            return float(tone_str.split(',')[0])
        except Exception:
            return None

    def parse_tone_column(self):
        """
        TONE sütunundan parsed_tone adında yeni bir sütun oluşturur.
        """
        if self.data is not None and 'TONE' in self.data.columns:
            self.data['parsed_tone'] = self.data['TONE'].apply(self.parse_tone)
        else:
            st.warning("Veri yüklenmedi veya 'TONE' sütunu mevcut değil.")

    def fix_date_column(self):
        """
        DATE sütununu datetime formatına çevirir, hatalı tarihleri çıkartır 
        ve ayrıca 'date_only' sütununu oluşturur.
        """
        st.info("DATE sütunu düzenleniyor...")
        if self.data is not None and 'DATE' in self.data.columns:
            self.data['datetime'] = pd.to_datetime(
                self.data['DATE'].astype(str),
                format='%Y%m%d%H%M%S',
                errors='coerce'
            )
            self.data = self.data.dropna(subset=['datetime'])
            self.data['date_only'] = self.data['datetime'].dt.date
        else:
            st.warning("Veri yüklenmedi veya 'DATE' sütunu mevcut değil.")

    def get_data(self):
        """
        Yüklenen veri kümesini döndürür.
        """
        return self.data

    def data_pipeline(self, start_date, end_date, keywords):
        """
        Belirtilen tarih aralığı için veriyi indirir, filtreler, TONE sütununu işler
        ve DATE sütununu düzenler. Sonuçta işlenmiş veri kümesini döndürür.
        """
        self.load_data_range(start_date, end_date, keywords)
        st.write(f"Veri kümesinde {self.data.shape[0]} satır ve {self.data.shape[1]} sütun mevcut.")
        self.filter_data(keywords)
        st.write(f"Veri kümesinde {self.data.shape[0]} satır ve {self.data.shape[1]} sütun mevcut.")
        self.parse_tone_column()
        st.write(f"Veri kümesinde {self.data.shape[0]} satır ve {self.data.shape[1]} sütun mevcut.")
        self.fix_date_column()
        st.write(f"Veri kümesinde {self.data.shape[0]} satır ve {self.data.shape[1]} sütun mevcut.")
        return self.get_data()
