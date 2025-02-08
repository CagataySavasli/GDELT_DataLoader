import streamlit as st
from src.app import APP


def main():
    app = APP()
    app.intro_joke()

    st.markdown("---")

    st.markdown("# Date Range:")
    st.write("Please select the date range for the data you want to load.")
    app.get_dates()

    st.markdown("---")

    st.markdown("# Actor Code Filter:")
    st.subheader("Filter by Actor 1")
    app.actor_buttons("actor1")

    st.subheader("Filter by Actor 2")
    app.actor_buttons("actor2")

    st.markdown("---")

    if st.button("Apply Actor Filter"):
        app.actor_filter()

    if st.button("Load Data"):
        app.load_data()

    app.download_data_button()

if __name__ == "__main__":
    main()
