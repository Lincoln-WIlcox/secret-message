import sys
import requests
import pandas as pd
import bs4 as bs

SECRET_MESSAGE_TABLE_COLUMNS = ["Character", "x-coordinate", "y-coordinate"]

def _get_google_doc_tables(url):
    html = requests.get(url).text

    soup = bs.BeautifulSoup(html, "html.parser")

    tables = []
    for table in soup.find_all("table"):
        rows = []
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            rows.append([cell.get_text(strip=True) for cell in cells])

        if not rows:
            continue

        df = pd.DataFrame(rows)

        #columns becomes the first row, which is the header of the table in the google doc
        df.columns = df.iloc[0]
        #remove first row, which was the header row
        df = df[1:].reset_index(drop=True)

        tables.append(df)

    tables.append

    return tables

def _filter_tables_by_columns(tables, required_columns):
    filtered_tables = []

    for df in tables:
        if all(col in df.columns for col in required_columns):
            filtered_tables.append(df)

    return filtered_tables


def get_secret_message(doc_url):
    tables = _get_google_doc_tables(doc_url)
    characters_tables = _filter_tables_by_columns(tables, SECRET_MESSAGE_TABLE_COLUMNS)
    return