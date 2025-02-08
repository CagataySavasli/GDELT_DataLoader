import streamlit as st
from src.DataLoader import DataLoader
import io
import zipfile


class APP:
    _instance = None  # Sınıf düzeyinde tek bir örnek tutulur.

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(APP, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.data_loader = DataLoader()
            self.start_date = None
            self.end_date = None
            self.data = None
            self.actor_code_mask = None
            self.actor_1_code_list = []
            self.actor_2_code_list = []

    def intro_joke(self):
        st.title("LazyLoader-GDELT 🦥")
        st.markdown(
            """
            Hey YOU 🫵 ❗

            Yes, you—the one who thinks Python is just a snake 🐍 and not a programming language! 😎

            I didn’t spend countless hours building this site just so you could effortlessly download your data without lifting a finger 🏋️. 
            Now you've got absolutely no excuse for being lazy, you magnificent slacker! 🥊😂

            So, get ready to roll up your sleeves and dive into some code-crushing magic 🚀✨. 

            (Just kidding—kind of! 😉)
            """
        )

    def get_dates(self):
        self.start_date = st.date_input("Start Date")
        self.end_date = st.date_input("End Date")

    def load_data(self):
        self.data = self.data_loader.load_data_range(self.start_date, self.end_date)
        st.write(f"Loaded {len(self.data)} records.")

    def actor_buttons(self, actor):
        """
        Tek bir fonksiyon kullanarak, Actor 1 veya Actor 2 için
        bir text input ve yan yana 3 buton (Add, Remove, Reset) gösterir.

        Parametre:
            actor: "actor1" veya "actor2" (veya 1 ya da 2) şeklinde verilip,
                   hangi aktörün kod listesinin yönetileceğini belirler.
        """
        # Parametreye göre ilgili liste ve etiket ayarlanıyor.
        if actor == 1 or actor == "actor1":
            actor_list = self.actor_1_code_list
            key_prefix = "actor1"
            actor_label = "Actor 1"
        elif actor == 2 or actor == "actor2":
            actor_list = self.actor_2_code_list
            key_prefix = "actor2"
            actor_label = "Actor 2"
        else:
            st.error("Invalid actor type specified!")
            return

        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            actor_code = st.text_input(f"Enter {actor_label} Code", key=f"{key_prefix}_code_input")
        with col2:
            if st.button(f"Add {actor_label} Code", key=f"add_{key_prefix}"):
                if actor_code:
                    actor_list.append(actor_code)
                    st.success(f"Added {actor_label} code: {actor_code}")
                else:
                    st.warning("Please enter an ActorCode before adding.")
        with col3:
            if st.button(f"Remove {actor_label} Code", key=f"remove_{key_prefix}"):
                if actor_list:
                    removed = actor_list.pop()
                    st.info(f"Removed {actor_label} code: {removed}")
                else:
                    st.warning("No actor code to remove.")
        with col4:
            if st.button(f"Reset {actor_label} List", key=f"reset_{key_prefix}"):
                actor_list.clear()
                st.info(f"{actor_label} list has been reset.")

        st.write(f"Current {actor_label} List:", actor_list)

    def actor_filter(self):
        st.write("Actor 1 Codes:", self.actor_1_code_list)
        st.write("Actor 2 Codes:", self.actor_2_code_list)
        st.write("Actor Filters Applied!")
        self.data_loader.set_actor_filters(self.actor_1_code_list, self.actor_2_code_list)

    def download_data_button(self):
        if self.data is not None:
            # Veriyi CSV formatına dönüştürüyoruz.
            csv_data = self.data.to_csv(index=False).encode('utf-8')

            # Hafızada bir ZIP dosyası oluşturuyoruz.
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("data.csv", csv_data)
            zip_buffer.seek(0)  # BytesIO imlecini başa alıyoruz.

            st.download_button(
                label="Download Data as ZIP",
                data=zip_buffer,
                file_name="data.zip",
                mime="application/zip"
            )
        else:
            st.info("No data loaded! Please load the data first.")
