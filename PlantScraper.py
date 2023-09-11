#!/usr/bin/env python

import sqlite3
import mechanicalsoup
from bs4 import Comment
import pandas as pd
import pprint
import time
import requests_cache
import re
import textwrap
import csv
import os.path
import sys

requests_cache.install_cache('demo_cache')
pp = pprint.PrettyPrinter(indent=4).pprint
browser = mechanicalsoup.StatefulBrowser()

def clean_label(tag):
    label = tag.text
    label = label.replace("?", "")
    label = label.replace("SHOW ALL", "")
    label = label.replace("moths", "Moths")
    label = re.sub("\(.*\)", "", label)
    return label.strip()

def fetch_info(url):
    print(f"Fetching info from {url} ...")
    # timing is optional. Browser.open is not
    before = time.time()
    browser.open(url)
    after = time.time()
    print(" Time to load page (possibly from cache): ", after - before)

    data = {}

    # Extract the common name and botanical name from the page
    pt_tag = browser.page.find("div", attrs={"class": "page_title"})
    if pt_tag is None:
        error_tag = browser.page.find("ul", attrs={"class": "error"})
        if error_tag is not None:
            print("=== Error: ", error_tag.text.strip())
        else:
            print("Could not find page title, do not know why no error found.")
            print(browser.page)
        return

    cn_tag = pt_tag.find("div", attrs={"class": "common_name"})
    for child in cn_tag.children:
        if isinstance(child,Comment):
            child.extract()
    cn = ''.join(cn_tag.findAll(string=True, recursive=False)).strip()
    bn = cn_tag.find_next_sibling("div").text.strip()
    print(f"=== {bn} ({cn}) ===")

    tag_Label = browser.page.find_all("div", attrs={"class": "label"})
    clean_tagLabel = [clean_label(value) for value in tag_Label]

    # This species_text span is set to display:none in the CSS
    # so it is not visible on the page.  But it is in the HTML
    # and can be extracted (removed).
    for span in browser.page.find_all("span", attrs={"class": "species_text"}):
        span.extract()

    labels = ["Companion Plants", "Propagation", "Butterflies & Moths hosted"]
    for label in labels:
        if label in clean_tagLabel:
            index = clean_tagLabel.index(label)
            info = tag_Label[index].find_next_sibling("div").text.strip()
            data[label] = info
        else:
            print(f"Could not find {label} in the list of labels")

    return(data)

def main(df):
    # Iterate through the rows in the dataframe, exctract URL, fetch,
    # and add data to the row.
    for index, item in df.iterrows():
        # we have two ways this can show up, depending on which data
        # we're importing:
        try:
            url = item['URL']
        except KeyError:
            url = item["Plant Url"]

        info = fetch_info(url)
        if info is not None:
            for key,value in info.items():
                df.loc[index, key] = value

    # Change the filepath for the updated Excel file and create new file
    updated_filepath = "plants_updated.xlsx"
    writer = pd.ExcelWriter(updated_filepath, engine='openpyxl', mode='w')
    df.to_excel(writer, index=False)
    writer._save()

    print(f"Created {updated_filepath} with modified data.")


if __name__ == '__main__':
    existing_filepath = "../DataAnalysis_plantDataset/Companion_Plants_Detailed.xls"
    alternate_filepath = "sample-data.csv"
    if os.path.exists(existing_filepath):
        df = pd.read_excel(existing_filepath)
        # Our downloaded spreadsheet has some header-type stuff in the
        # first three rows... so, drop those first three rows and set
        # the fourth row as the header (for column names):
        df = df.iloc[3:]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        # they leave out the https: in these, so... add it:
        df["Plant Url"] = df["Plant Url"].map(lambda x: "https:" + x)

    elif os.path.exists(alternate_filepath):
        df = pd.read_csv(alternate_filepath)
    else:
        print(f"File does not exist. Please download {existing_filepath} first.")
        sys.exit(1)

    main(df)
