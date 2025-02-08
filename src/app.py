import streamlit as st
from src.DataLoader import DataLoader
import io
import zipfile

class APP:
    # _instance = None  # Singleton instance
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(APP, cls).__new__(cls)
    #     return cls._instance

    def __init__(self):
        # if not hasattr(self, "_initialized"):
        #     self._initialized = True

        # Gerekli session_state anahtarlarını güvenli şekilde oluşturuyoruz.
        st.session_state.setdefault("data_loader", DataLoader())
        st.session_state.setdefault("start_date", None)
        st.session_state.setdefault("end_date", None)
        st.session_state.setdefault("data", None)
        st.session_state.setdefault("actor_code_mask", None)
        st.session_state.setdefault("actor_1_code_list", [])
        st.session_state.setdefault("actor_2_code_list", [])

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
        st.session_state["start_date"] = st.date_input("Start Date")
        st.session_state["end_date"] = st.date_input("End Date")

    def load_data(self):
        start_date = st.session_state.get("start_date")
        end_date = st.session_state.get("end_date")
        data_loader = st.session_state.get("data_loader")
        if start_date is None or end_date is None:
            st.warning("Please select both start and end dates!")
            return

        try:
            data = data_loader.load_data_range(start_date, end_date)
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

    def actor_buttons(self, actor):
        """
        Tek bir fonksiyon kullanarak, Actor 1 veya Actor 2 için
        bir text input ve yan yana 3 buton (Add, Remove, Reset) gösterir.

        Parametre:
            actor: "actor1" veya "actor2" (veya 1 ya da 2)
        """
        st.session_state.setdefault("actor_1_code_list", [])
        st.session_state.setdefault("actor_2_code_list", [])

        if actor == 1 or actor == "actor1":
            actor_list = st.session_state["actor_1_code_list"]
            key_prefix = "actor1"
            actor_label = "Actor 1"
        elif actor == 2 or actor == "actor2":
            actor_list = st.session_state["actor_2_code_list"]
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
        st.write("Actor 1 Codes:", st.session_state["actor_1_code_list"])
        st.write("Actor 2 Codes:", st.session_state["actor_2_code_list"])
        st.write("Actor Filters Applied!")
        data_loader = st.session_state.get("data_loader")
        if data_loader:
            data_loader.set_actor_filters(
                st.session_state["actor_1_code_list"],
                st.session_state["actor_2_code_list"]
            )
        else:
            st.error("Data loader not available.")

    def download_data_button(self):
        data = st.session_state.get("data")
        if data is not None:
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
