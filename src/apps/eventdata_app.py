import streamlit as st
from src.dataloaders.EventDataLoader import EventDataLoader
import io
import zipfile
import pandas as pd
from datetime import date, timedelta


class EventData_APP:

    def __init__(self):

        st.session_state["data_loader"] = EventDataLoader()

        st.session_state.setdefault("start_date", None)
        st.session_state.setdefault("end_date", None)
        st.session_state.setdefault("data", None)
        st.session_state.setdefault("actor_code_mask", None)
        st.session_state.setdefault("actor_1_code_list", [])
        st.session_state.setdefault("actor_2_code_list", [])
        st.session_state.setdefault("event_code_list", [])
        st.session_state.setdefault("show_event_code_dict", False)

    def how_to_use(self):
        st.title("📖 How to Use LazyLoader-GDELT 🦥")
        st.markdown(
            """
            This application allows you to scrape event data from [GDELT](http://data.gdeltproject.org/events/index.html)
            based on a selected date range. You can refine the data using various filters:

            - **Actor Filters:** Narrow down events by specifying Actor 1 and Actor 2 codes.
            - **Event Code Filters:** Filter events by specific Event Codes (entered as strings, so "081" remains "081").
            - **Root Event Code Filters:** Target events under broader categories by using Root Event Codes.
            - **Event Code Dictionary:** Browse a hierarchical view of Event Codes and their descriptions to help you decide on filters.
            """
        )

        st.header("1️⃣ Select a Date Range")
        st.markdown(
            """
            - In the **"Date Range"** section, choose a **Start Date** and an **End Date**.
            - The application will download GDELT event data for all dates within the selected range.
            """
        )

        st.header("2️⃣ Filter by Actor Codes (Optional)")
        st.markdown(
            """
            GDELT records interactions between two actors. You can filter data by entering Actor 1 and Actor 2 codes.

            ### **How to Add Actor Codes**
            1. **Enter a country or actor CAMEO code** in the text box under **Actor 1** or **Actor 2**.
            2. Click **"Add Actor 1 Code"** or **"Add Actor 2 Code"** to include the code in the filter list.
            3. To remove the last added code, click **"Remove Actor Code"**.
            4. To clear all Actor codes, click **"Reset Actor List"**.

            💡 **If you don’t enter any actor codes, the data will include all records without filtering by actor.**
            """
        )

        st.header("3️⃣ View the Event Code Dictionary")
        st.markdown(
            """
            - Use the **Event Code Dictionary** section to browse a hierarchical view of Event Codes along with their descriptions.
            - This will help you identify the right codes for filtering.
            - Click the toggle button to show or hide the dictionary.
            """
        )

        st.header("4️⃣ Filter by Event Codes (Optional)")
        st.markdown(
            """
            In addition to actor filters, you can refine your search by applying Event Code filters.

            ### **How to Add Event Codes**
            1. **Enter an Event Code** (as a string, e.g., "081") in the text box.
            2. Click **"Add Event Code"** to include it in the filter list.
            3. To remove the last added code, click **"Remove Event Code"**.
            4. To clear the Event Code list, click **"Reset Event Code List"**.

            💡 **If you don’t add any event codes, the data will include all events without event code filtering.**
            """
        )

        st.header("5️⃣ Filter by Root Event Codes (Optional)")
        st.markdown(
            """
            You can also apply filters based on Root Event Codes to target broader event categories.

            ### **How to Add Root Event Codes**
            1. **Enter a Root Event Code** (e.g., "02") in the provided text box.
            2. Click **"Add Root Event Code"** to include it in the filter list.
            3. To remove the last added code, click **"Remove Root Event Code"**.
            4. To clear the Root Event Code list, click **"Reset Root Event Code List"**.

            💡 **This filter will narrow the data to events corresponding to the specified root category.**
            """
        )

        st.header("6️⃣ Load Data")
        st.markdown(
            """
            - Click the **"Load Data"** button to start retrieving data from GDELT.
            - A progress bar will show the download progress.
            - Once the data is loaded, the application will display the number of records retrieved.
            """
        )

        st.header("7️⃣ Download Data")
        st.markdown(
            """
            - After data is loaded and filtered, you can download it by clicking **"Download Data as ZIP"**.
            - The downloaded file will contain a CSV file (`data.csv`) with the filtered event records.
            """
        )

        st.markdown("---")
        st.subheader("⚠️ Notes")
        st.markdown(
            """
            - The application fetches data from **GDELT in CSV format**.
            - **Actor filters** refine data based on international actor interactions.
            - **Event Code filters** let you narrow down events by specific codes. Be sure to enter event codes as strings (e.g., "081" remains "081").
            - **Root Event Code filters** allow you to target broader event categories.
            - If no date range is selected, **no data will be loaded**.
            - **Errors** may occur if GDELT data is unavailable for certain dates.
            - LazyLoader currently supports data between **2013-04-01** and **yesterday’s date**.

            Happy data scraping! 🚀
            """
        )
    def get_dates(self):
        st.write(
            f"Please select the date range between **2013-04-01** and **{date.today() - timedelta(days=1)}** for the data you want to load."
            " The application will download data for all dates within the selected range."
        )
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

    def camoe_code_searcher(self):
        df = pd.read_csv("src/cameo/CAMEO_country.txt", sep="\t", header=None, names=["CODE", "LABEL"]).loc[1:].reset_index(
            drop=True).copy()

        if df is not None:
            country_dict = dict(zip(df["LABEL"], df["CODE"]))
            search_query = st.text_input("Search for a country:")
            if search_query:
                suggestions = [country for country in country_dict.keys() if
                               country.lower().startswith(search_query.lower())]
                selected_country = st.selectbox("Select a country:", suggestions, index=0 if suggestions else None)
                if selected_country:
                    st.write(f"**Selected Country Code:** {country_dict[selected_country]}")
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

    def eventcode_buttons(self):
        """
        Displays a text input and three buttons (Add, Remove, Reset) for managing
        Event Code filters. The event codes are treated as strings, so an input
        like "081" remains as "081".
        """
        st.session_state.setdefault("event_code_list", [])

        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            event_code = st.text_input("Enter Event Code", key="event_code_input")
        with col2:
            if st.button("Add Event Code", key="add_event_code"):
                if event_code:
                    # Save the event code as a string (e.g., "081" remains "081")
                    st.session_state["event_code_list"].append(event_code)
                    st.success(f"Added Event Code: {event_code}")
                else:
                    st.warning("Please enter an Event Code before adding.")
        with col3:
            if st.button("Remove Event Code", key="remove_event_code"):
                if st.session_state["event_code_list"]:
                    removed = st.session_state["event_code_list"].pop()
                    st.info(f"Removed Event Code: {removed}")
                else:
                    st.warning("No Event Code to remove.")
        with col4:
            if st.button("Reset Event Code List", key="reset_event_code"):
                st.session_state["event_code_list"].clear()
                st.info("Event Code list has been reset.")

        st.write("Current Event Code List:", st.session_state["event_code_list"])

    def root_eventcode_buttons(self):
        """
        Displays a text input and three buttons (Add, Remove, Reset) for managing
        Root Event Code filters. The event codes are treated as strings, so an input
        like "081" remains as "081".
        """
        st.session_state.setdefault("root_event_code_list", [])

        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            root_event_code = st.text_input("Enter Root Event Code", key="root_event_code_input")
        with col2:
            if st.button("Add Root Event Code", key="add_root_event_code"):
                if root_event_code:
                    st.session_state["root_event_code_list"].append(root_event_code)
                    st.success(f"Added Root Event Code: {root_event_code}")
                else:
                    st.warning("Please enter a Root Event Code before adding.")
        with col3:
            if st.button("Remove Root Event Code", key="remove_root_event_code"):
                if st.session_state["root_event_code_list"]:
                    removed = st.session_state["root_event_code_list"].pop()
                    st.info(f"Removed Root Event Code: {removed}")
                else:
                    st.warning("No Root Event Code to remove.")
        with col4:
            if st.button("Reset Root Event Code List", key="reset_root_event_code"):
                st.session_state["root_event_code_list"].clear()
                st.info("Root Event Code list has been reset.")

        st.write("Current Root Event Code List:", st.session_state["root_event_code_list"])


    def eventcode_filter(self):
        """
        Applies the event code filters to the loaded dataset by passing the list of
        event codes to the data loader.
        """
        st.write("Event Codes:", st.session_state["event_code_list"])
        st.write("Event Filters Applied!")
        data_loader = st.session_state.get("data_loader")
        if data_loader:
            data_loader.set_event_filters(st.session_state["event_code_list"])
        else:
            st.error("Data loader not available.")

    def root_eventcode_filter(self):
        """
        Applies the root event code filters to the loaded dataset by passing the list of
        event codes to the data loader.
        """
        st.write("Root Event Codes:", st.session_state["root_event_code_list"])
        st.write("Root Event Filters Applied!")
        data_loader = st.session_state.get("data_loader")
        if data_loader:
            data_loader.set_root_event_filters(st.session_state["root_event_code_list"])
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

    def load_cameo_event_codes(self, file_path):
        """
        Loads the CAMEO event codes from a text file.

        Expects the first line to be a header. Each subsequent line should contain
        the event code and its description separated by a tab or whitespace.

        Parameters:
            file_path (str): Path to the CAMEO event code text file.

        Returns:
            dict: A dictionary mapping event code to a node dictionary containing the
                  code, description, and an empty children dict.
        """
        codes = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Skip the header line
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                parts = line.split()
            code = parts[0]
            description = " ".join(parts[1:])
            codes[code] = {'code': code, 'desc': description, 'children': {}}

        return codes

    def build_event_tree(self, codes):
        """
        Constructs a hierarchical tree of event codes.

        For each code (except top-level 2-digit codes), its parent is determined by
        finding the longest prefix (with a minimum length of 2) that exists in the codes.

        Parameters:
            codes (dict): Dictionary of event code nodes.

        Returns:
            dict: A hierarchical tree of event codes.
        """
        tree = {}
        # Process codes sorted by length (shorter codes first)
        for code in sorted(codes.keys(), key=len):
            node = codes[code]
            if len(code) == 2:
                # Top-level code
                tree[code] = node
            else:
                parent_found = False
                # Look for a parent: try prefixes from len(code)-1 down to 2 characters
                for i in range(len(code) - 1, 1, -1):
                    parent_code = code[:i]
                    if parent_code in codes:
                        codes[parent_code]['children'][code] = node
                        parent_found = True
                        break
                if not parent_found:
                    # If no parent is found, add as a top-level code (rare case)
                    tree[code] = node
        return tree

    def display_event_tree(self, tree, indent=0):
        """
        Recursively displays the event code tree.

        At the top level (indent == 0), each node is displayed as an expander.
        For nested levels (indent > 0), nodes are shown as indented bullet points.

        Parameters:
            tree (dict): Hierarchical event code tree.
            indent (int): Current indentation level.
        """
        for code, node in tree.items():
            if indent == 0:
                # Top-level nodes: use an expander.
                with st.expander(f"{code}: {node['desc']}"):
                    if node['children']:
                        self.display_event_tree(node['children'], indent=indent + 1)
            else:
                # Nested nodes: use indented markdown bullet points.
                st.markdown(" " * (indent * 4) + f"- **{code}:** {node['desc']}")
                if node['children']:
                    self.display_event_tree(node['children'], indent=indent + 1)

    def display_cameo_event_code_dictionary(self):
        """
        Loads the CAMEO event code dictionary from a text file,
        builds the hierarchical tree, and displays it.

        Note: We do not wrap the entire dictionary in an outer expander,
              so that the top-level expanders are not nested.
        """
        file_path = "src/cameo/CAMEO_event.txt"  # Update this path as needed
        codes = self.load_cameo_event_codes(file_path)
        tree = self.build_event_tree(codes)

        st.markdown("### CAMEO Event Code Dictionary")
        st.markdown("Browse the hierarchical event codes by clicking on each top-level expander below.")
        self.display_event_tree(tree)

    def toggle_event_code_dict(self):
        """Toggle the visibility flag for the EventCode Dictionary expander."""
        st.session_state.show_event_code_dict = not st.session_state.show_event_code_dict
    def control_display_cameo_event_code_dictionary(self):
        st.button("Toggle EventCode Dictionary", on_click=self.toggle_event_code_dict)
        if st.session_state.show_event_code_dict:
            self.display_cameo_event_code_dictionary()
            st.markdown("---")