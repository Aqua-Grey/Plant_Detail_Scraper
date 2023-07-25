
import sqlite3
import mechanicalsoup
import pandas as pd
#import numpy as np

# Import the function from module_testCode.py
from module_testCode import main



# Load the dataset
data = pd.read_excel("../DataAnalysis_plantDataset/Companion_Plants_Detailed.xls")

# Drop the first three rows and set the fourth row as the header
data = data.iloc[3:]
data.columns = data.iloc[0]
data = data.iloc[1:]

# Select the Scientific Name and Common Name columns
plants = data[["Current Botanical Name", "Common Name"]]

# Create an empty DataFrame
df = pd.DataFrame(columns=["Scientific Name", "Common Name", "URL"])

for _, row in plants.iterrows():
    scientific_name = row["Current Botanical Name"]
    common_name = row["Common Name"]

    # Format the search query for URL
    query = f"{scientific_name.replace(' ', '-')}--({common_name})"

    # Construct the URL
    url = f"https://calscape.org/{query}"

    # Append the data to the DataFrame
    df = pd.concat([df, pd.DataFrame({"Scientific Name": scientific_name,
                                      "Common Name": common_name,
                                      "URL": url},
                                      index=[0])], ignore_index=True)


# Call the function to run the code
main(df)