import re
import json

def parse_europharma_receipt(text):
    # --- 1. Extract Date and Time ---
    # Looking for format: 18.04.2019 11:13:58
    datetime_pattern = r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})'
    dt_match = re.search(datetime_pattern, text)
    date_val = dt_match.group(1) if dt_match else None
    time_val = dt_match.group(2) if dt_match else None

    # --- 2. Extract Payment Method ---
    payment_method = "Unknown"
    if "Банковская карта" in text:
        payment_method = "Card"
    elif "Наличные" in text:
        payment_method = "Cash"

    # --- 3. Extract Products and Prices ---
    products = []
    prices = []
    
    # Split by numbered lines (e.g., "1.", "2.")
    # We use a regex that looks for a number followed by a dot at the start of a line
    items_raw = re.split(r'\n\d+\.\n', text)
    
    for item in items_raw[1:]: # Skip the header part
        lines = [l.strip() for l in item.split('\n') if l.strip()]
        if lines:
            # The first line after the number is the product name
            name = lines[0]
            
            # Find the individual item total (usually the 3rd or 4th line in this format)
            # We look for a line that is a number with a comma (e.g., 1 200,00)
            for line in lines:
                if ',' in line and 'x' not in line and 'Стоимость' not in line:
                    # Clean number: remove spaces, replace comma with dot
                    clean_price = line.replace(' ', '').replace(',', '.')
                    if re.match(r'^\d+\.\d{2}$', clean_price):
                        products.append(name)
                        prices.append(float(clean_price))
                        break

    # --- 4. Extract Total Amount ---
    total_match = re.search(r'ИТОГО:\s*([\d\s,]+)', text)
    total_val = 0.0
    if total_match:
        total_val = float(total_match.group(1).replace(' ', '').replace(',', '.'))

    # Construct JSON
    output = {
        "shop": "EUROPHARMA",
        "metadata": {
            "date": date_val,
            "time": time_val,
            "payment_method": payment_method
        },
        "items": [
            {"name": n, "price": p} for n, p in zip(products, prices)
        ],
        "total_amount": total_val
    }
    
    return output

# Test with your data
receipt_text = """[PASTE YOUR RECEIPT TEXT HERE]"""
# In the actual script, you would use: 
# with open('raw.txt', 'r', encoding='utf-8') as f: receipt_text = f.read()

parsed_json = parse_europharma_receipt(receipt_text)
print(json.dumps(parsed_json, indent=4, ensure_ascii=False))