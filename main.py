import streamlit as st
from src.app import APP


def main():
    app = APP()
    app.intro_joke()
    st.markdown("---")
    app.select_app()




if __name__ == "__main__":
    main()
