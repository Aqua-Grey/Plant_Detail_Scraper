
# Plant Detail Scraper

This repository contains Python scripts that were used to scrape plant details from the Calscape website before its recent update. The code utilizes tools such as MechanicalSoup and BeautifulSoup for web scraping, with data processing handled through pandas and SQLite. The primary focus of the script was to gather data about plants, including information on companion plants, propagation methods, and their relationships with butterflies and moths.

---

### ⚠️ Important Notice ⚠️

The Calscape website has undergone significant updates, and the structure of the site has changed. As a result, **this code will no longer function with the current version of the website**.

---

### New Features on Calscape

The updated website now includes:
- **companion plant** recommendations.
- **propagation information**.
- **downloadable data**, making it easier to work with plant datasets without web scraping.

Explore the updated Calscape website here: [https://calscape.org/](https://calscape.org/)

---

### Previous Script Capabilities

Before the update, this script was used to:
1. Scrape data from plant detail pages, including common and botanical names.
2. Extract specific plant attributes such as:
   - Companion plants.
   - Propagation details.
   - Host plants for butterflies and moths.
3. Save the gathered data into a processed Excel file for further analysis.

---

### How to Adapt the Script

If you are looking to scrape data from the new Calscape site:
1. Explore the **downloadable datasets** available on the new website. These datasets might provide all the information you need without requiring a scraper.
2. If scraping is still necessary, the script must be updated to accommodate the new structure of the Calscape website. This may involve:
   - Adjusting the parsing logic for updated HTML and CSS.
   - Including new headers and tags used in the website's current layout.

---

### Tools Used
- **MechanicalSoup**: For browser emulation.
- **BeautifulSoup**: For HTML parsing and data extraction.
- **Pandas**: For data manipulation and storage.
- **SQLite**: For optional database integration.

---

Feel free to explore the provided code and adapt it for other use cases. If you encounter any issues or have questions, open an issue in this repository!
