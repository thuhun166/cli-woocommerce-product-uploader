
def generate_title(data, website, club_name, season_year, image_paths=None):
    """Generate product title based on input data."""
    product_type = data['product_type']
    category = data['category']
    item_type = data['item_type']
    player_name = data.get('player_name', '')
    socks = "With Socks" if data['socks'] == 'Yes' else "No Socks"

    if website == "RFS" and image_paths:
        title = f"{club_name} {product_type} {category} Football {item_type} {season_year} {player_name} {socks}"
    elif website == "CFS":
        title = f"{club_name} {player_name} {product_type} {category} Cheap Football {item_type} {season_year} {socks}"
    return title

def generate_sku(data, website, club_name, player_name, season_year):
    """Generate SKU based on input data."""
    sku = f"{website[:3].upper()}_{club_name[:3].upper()}_{player_name[:3].upper()}_{data['product_type'][:2].upper()}_{data['category'][:2].upper()}_{season_year}"
    return sku

def generate_tags(data, club_name, season_year):
    """Generate tags for the product."""
    tags = [
        club_name,
        f"{club_name} {season_year}",
        f"{club_name} {data['product_type']} {data['category']} {data['item_type']}",
        f"New Arrivals {season_year}"
    ]
    if data.get('player_name', ''):
        tags.append(data['player_name'].capitalize())
    return tags

def generate_description(data, website, club_name, season_year, image_paths=None):
    """Generate product description based on input data."""
    html_template = website["description_html"]  
    if website == "RFS" and image_paths:
        prompt = f"Generate a description for the following image: {image_paths[0]}"
        ai_description = generate_content_from_openai(prompt) 
        ai_block = f"<h2>Description of {data['title']}</h2><p>{ai_description}</p>" if ai_description else ""
        description = html_template.replace("{$formatted_title}", data['title']) \
            .replace("{$ai_gen_description}", ai_block) \
            .replace("{$html_content_about_club}", f"<h2><strong>About {club_name}</strong></h2><p>{club_name}</p>") \
            .replace("{$year}", season_year)
    else:
        description = html_template.replace("{$formatted_title}", data['title']) \
            .replace("{$html_content_about_club}", f"<h2>Description of {club_name}</h2><p>{club_name}</p>") \
            .replace("{$year}", season_year)
    return description

def generate_short_description(data, club_name):
    """Generate short description for the product."""
    short_description = f"{club_name} {data['product_type']} {data['category']} {data['item_type']}"
    if data.get('player_name', ''):
        short_description += f" - {data['player_name']}"
    return short_description

def generate_variations(data):
    """Generate variations for the product."""
    variations = [map_variation_to_website_size(v.strip()) for v in data['variations_raw']]  # Đảm bảo hàm map_variation_to_website_size đã được định nghĩa
    variation_data = []
    if variations:
        for variation in variations:
            size_number = variation.split()[0]
            variation_sku = f"{data['sku']}_{size_number}"
            variation_data.append({
                "attributes": [{"id": 3, "option": variation}],
                "regular_price": data['regular_price'],
                "sale_price": data['final_sale_price'],
                "sku": variation_sku
            })
    return variation_data
