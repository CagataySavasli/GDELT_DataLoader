import streamlit as st
from src.apps.eventdata_app import EventData_APP
from src.apps.graphdata_app import GraphData_APP

class APP:
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

    def apps_infos(self):
        with st.sidebar.expander("ℹ️ About the Apps"):
            st.markdown(
                """
                **Event Data App:**
                - Downloads GDELT event data based on a selected date range.
                - Allows filtering by entering Actor 1 and Actor 2 codes.
                - You can download the filtered data as a ZIP file.

                **Graph Data App:**
                - Downloads GDELT Graph (GKG) data based on a selected date range.
                - Filters data using keywords in the THEMES column.
                - Processed data can be downloaded as a ZIP file.
                """
            )
    def select_app(self):
        st.sidebar.title("🦥 LazyLoader-GDELT")
        app_selection = st.sidebar.radio("Select an App", ["Event Data", "Graph Data"])

        if app_selection == "Event Data":
            self.event_data_app()
        elif app_selection == "Graph Data":
            self.graph_data_app()

        self.apps_infos()

    def event_data_app(self):
        app = EventData_APP()

        with st.expander("📖 How to Use LazyLoader-GDELT 🦥"):
            app.how_to_use()

        st.markdown("# Date Range:")
        app.get_dates()

        st.markdown("---")

        st.markdown("# Actor Code Filter:")

        with st.expander("🔎 Country Codes Searcher 🌍"):
            app.camoe_code_searcher()

        st.subheader("Filter by Actor 1")
        app.actor_buttons("actor1")

        st.subheader("Filter by Actor 2")
        app.actor_buttons("actor2")

        st.markdown("---")

        if st.button("Apply Actor Filter"):
            app.actor_filter()

        st.markdown("---")
        app.control_display_cameo_event_code_dictionary()

        st.subheader("Event Code Filter")
        app.eventcode_buttons()

        if st.button("Apply Event Code Filter"):
            app.eventcode_filter()

        st.markdown("---")

        st.subheader("Root Event Code Filter")
        app.root_eventcode_buttons()

        if st.button("Apply Root Event Code Filter"):
            app.root_eventcode_filter()

        st.markdown("---")


        if st.button("Load Data"):
            app.load_data()

        app.download_data_button()

    def graph_data_app(self):
        app = GraphData_APP()

        with st.expander("📖 How to Use Graph Data Loader"):
            app.how_to_use()

        st.markdown("# Date Range & Keywords:")
        app.get_dates()

        st.markdown("---")

        if st.button("Load Data", key="graph_data_load"):
            app.load_data()

        app.download_data_button()

