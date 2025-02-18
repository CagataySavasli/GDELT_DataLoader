# LazyLoader-GDELT 🦥  
*Download GDELT Data the Lazy Way!*

LazyLoader-GDELT is a playful, Streamlit-based application that lets even non-coders effortlessly download and filter GDELT data. Tired of writing code just to fetch event data? With LazyLoader-GDELT, all you need is a few clicks to get your hands on the data—while enjoying a bit of humor along the way.

---

## Features

- **User-Friendly Interface:**  
  An interactive web app built with Streamlit that makes data downloading as easy as a few clicks.

- **Multiple Apps in One:**  
  Choose between two powerful tools:
  - **Event Data App:**  
    - **Date Range Selection:** Easily choose a start and end date to define your data range.
    - **Actor Filtering:** Filter event data by specifying Actor 1 and Actor 2 codes with simple Add, Remove, and Reset buttons.
    - **Event Code Filtering:**  
      - **Hierarchical CAMEO Event Code Dictionary:** View event codes and their descriptions in a collapsible, hierarchical format.
      - **Toggle Button:** Use a toggle button to show or hide the EventCode Dictionary as needed.
    - **Downloadable Data:** Export your filtered event data as a ZIP file containing a CSV.
  - **Graph Data App:**  
    - **Date Range & Keyword Filtering:** Download GKG (Global Knowledge Graph) data based on a selected date range and filter it using keywords in the THEMES column.
    - **Downloadable Data:** Export your processed graph data as a ZIP file containing a CSV.

- **Progress Indicators:**  
  Visual progress bars and status messages keep you informed during the data loading process.

- **Lazy Attitude:**  
  Designed for those who prefer an effortless, click-only solution—with a dash of humor along the way!

---

## How It Works

1. **Select an App:**  
   Use the sidebar to choose between the **Event Data App** and the **Graph Data App**. An expandable info panel provides details about what each app does.

2. **Set Your Date Range:**  
   Specify the start and end dates for the data you want to load.

3. **Apply Filters:**  
   - For the **Event Data App**, enter Actor codes to filter by country or actor. You can also filter by Event Codes using the hierarchical CAMEO Event Code Dictionary.
   - For the **Graph Data App**, enter keywords (comma-separated) to filter the data based on the THEMES column.

4. **Toggle EventCode Dictionary:**  
   In the Event Data App, click the **Toggle EventCode Dictionary** button to show or hide the collapsible, hierarchical view of CAMEO Event Codes.

5. **Load and Download Data:**  
   Click the **Load Data** button to fetch data. A progress bar indicates the download process, and once completed, you can download your data as a ZIP file containing a CSV.

---

## Live Demo

Skip the cloning and installation process—just visit the live app to get started:

[**LazyLoader-GDELT Live App**](https://lazyloader-gdelt.streamlit.app)

---

## Contributing

Contributions are always welcome! If you have suggestions or improvements, please:
- Open an [issue](https://github.com/CagataySavasli/LazyLoader-GDELT/issues)
- Submit a pull request

---

## Acknowledgements

Inspired by the GDELT project and built with a dash of humor to make data downloading as effortless as possible. Remember: sometimes, being lazy is the best way to get things done!

---

*Happy data loading!*
EOF
