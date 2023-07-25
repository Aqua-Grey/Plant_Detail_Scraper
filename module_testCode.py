
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
    data = {'Plant Url': url}
    print(f"Fetching info from {url} ...")
    # timing is optional. Browser.open is not
    before = time.time()
    browser.open(url)
    after = time.time()
    print(" Time to load page (possibly from cache): ", after - before)

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

    #print("pt_tag: ", pt_tag, pt_tag.text)
    cn_tag = pt_tag.find("div", attrs={"class": "common_name"})
    for child in cn_tag.children:
        if isinstance(child,Comment):
            child.extract()
    #print("cn_tag: ", cn_tag, cn_tag.text)
    cn = ''.join(cn_tag.findAll(string=True, recursive=False)).strip()
    #cn = cn_tag.contents[0].strip()
    bn = cn_tag.find_next_sibling("div").text.strip()
    print(f"=== {bn} ({cn}) ===")

    tag_Label = browser.page.find_all("div", attrs={"class": "label"})
    clean_tagLabel = [clean_label(value) for value in tag_Label]
    #pp(clean_tagLabel)

    # This species_text span is set to display:none in the CSS
    # so it is not visible on the page.  But it is in the HTML
    # and can be extracted (removed).
    for span in browser.page.find_all("span", attrs={"class": "species_text"}):
        span.extract()

    labels = ["Companion Plants", "Propagation", "Butterflies & Moths hosted"]
    for label in labels:
        if label in clean_tagLabel:
            index = clean_tagLabel.index(label)
            #print(f"  {label}:")
            info = tag_Label[index].find_next_sibling("div").text.strip()
            #print('\n'.join(textwrap.wrap(info, initial_indent=indent, subsequent_indent=indent)))
            data[label] = info
        else:
            print(f"Could not find {label} in the list of labels")

    return(data)

'''
def main(df):
    urls = df['URL'].tolist()

    # Iterate through the column containing URLs
    for url in urls:
        fetch_info(url)
'''

def main(df):
    try:
        urls = df['URL'].tolist()
    except KeyError:
        df["Plant Url"] = df["Plant Url"].map(lambda x: "https:" + x)
        urls = df["Plant Url"].tolist()
   
    data = []

    # Create a Pandas dataframe to hold the scraped data
    df_plants = pd.DataFrame(columns=['Name', 'Botanical Name', 'Companion Plants', 'Propagation',
                                      'Butterflies & Moths hosted'])

    # Iterate through the column containing URLs
    for url in urls:
        info = fetch_info(url)
        if info is not None:
            data.append(info)
            #df_plants.append(info, ignore_index=True)
            #df_plants.concat(["a", "b", "c","d", "e"])
    df_plants = pd.DataFrame(data)
    # Add the fetched data to the existing dataframe
    df_updated = pd.concat([df, df_plants])

    # Change the filepath for the updated Excel file and create new file
    updated_filepath = "plants_updated.xlsx"
    writer = pd.ExcelWriter(updated_filepath, engine='openpyxl', mode='w') 
    df_updated.to_excel(writer, index=False) 
    writer.save()

    print("Data appended to the existing dataframe and a new file was created.")


if __name__ == '__main__':
    existing_filepath = "../DataAnalysis_plantDataset/Companion_Plants_Detailed.xls" 
    if os.path.exists(existing_filepath):
        df = pd.read_excel(existing_filepath)
        # Drop the first three rows and set the fourth row as the header
        df = df.iloc[3:]
        df.columns = df.iloc[0]
        df = df.iloc[1:]

        main(df)
    else: 
        print(f"File does not exist. Please download {existing_filepath} first.")
        sys.exit(1)
