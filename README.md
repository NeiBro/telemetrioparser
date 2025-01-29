# Telegram Channel Parser

This script parses pages from the Telegram channel catalog on [Telemetr.io](https://telemetr.io/) and collects @usernames if they are present.

## 🚀 Features
- Collects channel links from pages of the catalog.
- Extracts all @usernames from each channel page.
- Saves them in the `usernames.txt` file.
- Filters data by removing lines containing "bot".

## 📦 Installation and Usage

### 1. Install Dependencies
The script requires `requests` and `beautifulsoup4`. Install them with:
```sh
pip install requests bs4
```

### 2. Run the Parser
```sh
python parser.py
```

After execution, the usernames will be saved in `usernames.txt`.

## 🛠 Requirements
- Python 3.7+
- Libraries: `requests`, `beautifulsoup4`

## 📜 License
This project is distributed under the MIT License.

