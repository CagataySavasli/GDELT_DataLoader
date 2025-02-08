import streamlit as st
from src.app import APP


def main():
    app = APP()
    app.intro_joke()

    st.markdown("---")

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

    if st.button("Load Data"):
        app.load_data()

    app.download_data_button()


if __name__ == "__main__":
    main()
