import sys
from sqlite_utils import Database

def main():
    search_text = sys.argv[1]
    search_all(search_text)

def search_all(text):
    db_name = 'subtitles.db'
    db = Database(db_name)

    rows = list(db["Subtitles"].search(text))
    for i in rows:
        print(i, type(i))

if __name__ == '__main__':
    main()