import requests
from product_utils import generate_title, generate_sku, generate_tags, generate_description, generate_short_description, generate_variations
from file_utils import parse_product_csv, get_product_price_and_variations, get_seo_data, get_club_data

def upload_product(csv_file, website, wp_user, app_password, consumer_key, consumer_secret):
    """Upload products to WooCommerce from CSV."""
    product_data = parse_product_csv(csv_file)
    
    for data in product_data:
        title = generate_title(data, website, data['club_name'], data['season_year'])
        sku = generate_sku(data, website, data['club_name'], data.get('player_name', ''), data['season_year'])
        tags = generate_tags(data, data['club_name'], data['season_year'])
        description = generate_description(data, website, data['club_name'], data['season_year'])
        short_description = generate_short_description(data, data['club_name'])
        variations = generate_variations(data)

        regular_price, sale_price, variations_raw = get_product_price_and_variations(title, website)
        
        final_sale_price = sale_price if sale_price else regular_price

        seo = get_seo_data(website)
        category_ids = data['category_ids']

        product_data = {
            "name": title,
            "sku": sku,
            "regular_price": regular_price,
            "sale_price": final_sale_price,
            "description": description,
            "short_description": short_description,
            "tags": [{"name": tag} for tag in tags],
            "categories": [{"id": int(id.strip())} for id in category_ids],
        }

        try:
            api_url = f"{website}/wp-json/wc/v3/products"
            response = requests.post(api_url, auth=(consumer_key, consumer_secret), json=product_data)
            
            if response.status_code == 201:
                product_id = response.json()['id']
                print(f"Product '{title}' uploaded successfully with ID: {product_id}")
                
                if variations:
                    variation_data = generate_variations(data)
                    upload_variations(product_id, variation_data, website, consumer_key, consumer_secret)
                    print(f"Variations for '{title}' uploaded successfully.")
            else:
                raise Exception(f"Product upload failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error uploading product '{title}': {e}")

def upload_variations(product_id, variations_data, website, consumer_key, consumer_secret):
    """Upload variations for a product."""
    variations_url = f"{website}/wp-json/wc/v3/products/{product_id}/variations/batch"
    response = requests.post(
        variations_url,
        auth=(consumer_key, consumer_secret),
        json={"create": variations_data}
    )

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Variations upload failed: {response.status_code}, {response.text}")


def update_product(product_id, updated_data, website, consumer_key, consumer_secret):
    """Update an existing product in WooCommerce."""
    api_url = f"{website}/wp-json/wc/v3/products/{product_id}"
    
    response = requests.put(api_url, auth=(consumer_key, consumer_secret), json=updated_data)
    
    if response.status_code == 200:
        print(f"Product with ID {product_id} updated successfully.")
        return response.json()
    else:
        print(f"Error updating product with ID {product_id}: {response.status_code}, {response.text}")
        return None