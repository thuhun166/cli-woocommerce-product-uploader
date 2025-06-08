import argparse
import os  
from woo_utils import upload_product, update_product
from file_utils import parse_product_csv, load_api_keys

def upload_products_from_csv(csv_file):
    """Upload products to WooCommerce from a CSV file."""
    
    if not os.path.exists(csv_file):
        print(f"File '{csv_file}' does not exist.")
        return  
    product_data = parse_product_csv(csv_file)
    
    for data in product_data:
        website = data["website"]
        config = load_api_keys(website)
        if not config:
            print(f"API configuration for website '{website}' not found.")
            continue
        wp_user = config["wp_user"]
        app_password = config["app_password"]
        consumer_key = config["consumer_key"]
        consumer_secret = config["consumer_secret"]
        
        upload_product(csv_file, website, wp_user, app_password, consumer_key, consumer_secret)

def update_product_from_csv(csv_file):
    """Update existing products in WooCommerce from a CSV file."""
    pass  

def process_cli(args):
    """Process CLI commands and flags."""
    parser = argparse.ArgumentParser(description="CLI tool for uploading and updating products in WooCommerce.")
    parser.add_argument('-upload', '--upload', help="Upload products from a CSV file", metavar="FILE")
    parser.add_argument('-update', '--update', help="Update existing products from a CSV file", metavar="FILE")

    parsed_args = parser.parse_args(args)

    if parsed_args.upload:
        upload_products_from_csv(parsed_args.upload)
    elif parsed_args.update:
        update_product_from_csv(parsed_args.update)
    else:
        print("No valid flags provided. Use -upload or -update.")
