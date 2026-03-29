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

def _build_secret_message_table(characters_table):
    max_x = characters_table["x-coordinate"].astype(int).max()
    max_y = characters_table["y-coordinate"].astype(int).max()

    #make table using the given dimensions filled with spaces; we'll replace the spaces later
    secret_message_tables = pd.DataFrame([[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)])

    for _, row in characters_table.iterrows():
        x = int(row["x-coordinate"])
        y = int(row["y-coordinate"])
        char = row["Character"]

        secret_message_tables.iloc[y, x] = char

    return secret_message_tables

def _build_secret_message_tables(characters_tables):
    secret_message_tables = []
    for character_table in characters_tables:
        secret_message_table = _build_secret_message_table(character_table)
        secret_message_tables.append(secret_message_table)
    
    return secret_message_tables

def _build_secret_message(secret_message_table):
    secret_message = ""

    for row in secret_message_table.itertuples(index=False):
        for value in row:
            secret_message += value
        secret_message += "\n"
    
    return secret_message

def _build_secret_messages(secret_message_tables):
    secret_messages = []
    for secret_message_table in secret_message_tables:
        secret_message = _build_secret_message(secret_message_table)
        secret_messages.append(secret_message)
    
    return secret_messages

def get_secret_messages(doc_url):
    tables = _get_google_doc_tables(doc_url)
    characters_tables = _filter_tables_by_columns(tables, SECRET_MESSAGE_TABLE_COLUMNS)
    secret_message_tables = _build_secret_message_tables(characters_tables)
    secret_messages = _build_secret_messages(secret_message_tables)
    return secret_messages

def print_secret_messages(doc_url):
    secret_messages = get_secret_messages(doc_url)
    for secret_message in secret_messages:
        print(secret_message)