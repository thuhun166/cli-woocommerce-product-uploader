import csv
import os
import json
import random

def read_csv(file_path):
    """Read CSV file and return the data as a list of dictionaries."""
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def parse_product_csv(csv_file):
    """Parse CSV file to extract product information."""
    products = read_csv(csv_file)
    product_data = []

    for product in products:
        product_data.append({
            "website": product["website"],
            "club_name": product["club_name"],
            "player_name": product["player_name"],
            "product_type": product["product_type"],
            "category": product["category"],
            "item_type": product["item_type"],
            "socks": product["socks"],
            "season_year": product["season_year"],
            "category_ids": product["category_ids"].split(","),
            "variations_raw": product["variations_raw"].split(","),
        })
    return product_data

def get_club_data(club_name, website):
    """Get club data from the corresponding club CSV file."""
    club_file = os.path.join('club', f"{website.lower()}_club.csv")
    if not os.path.exists(club_file):
        return None
    clubs = read_csv(club_file)
    for club in clubs:
        if club['club_name'].lower() == club_name.lower():
            category_ids = club['category_id'].split(',')
            return {**club, 'category_ids': category_ids}
    return None

def get_product_price_and_variations(title, website):
    """Get product price and variations."""
    prices_file = os.path.join('prices', f"{website.lower()}_prices.csv")
    if not os.path.exists(prices_file):
        return None, None, []
    prices = read_csv(prices_file)
    title_words = set(title.lower().split())
    best_match_score = 0
    best_price = None
    for price_entry in prices:
        product_type_words = set(price_entry['product_type'].lower().split())
        match_score = len(title_words.intersection(product_type_words))
        if match_score > best_match_score:
            best_match_score = match_score
            best_price = price_entry
    if best_price:
        variations = best_price.get('variations', '')
        variation_list = variations.split(',') if variations else []
        return best_price['regular_price'], best_price['sale_price'], variation_list
    else:
        return None, None, []

def get_seo_data(website):
    """Get SEO data for the given website."""
    seo_file = os.path.join('seo', f"{website.lower()}_seo.csv")
    if not os.path.exists(seo_file):
        return {"seo_title": "Default Title", "meta_description": "Default Description"}
    seo_data = read_csv(seo_file)
    return random.choice(seo_data)


def load_api_keys(web_name):
    try:
        with open("api_keys.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get(web_name)
    except FileNotFoundError:
        messagebox.showerror("Error", "API keys file not found!")
        return None