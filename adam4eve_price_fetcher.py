import requests
import csv
import time
import re
import statistics

# --- Configuration ---
INPUT_CSV = "eve_items_with_typeids.csv"  # Your input CSV file with TypeIDs
OUTPUT_CSV = "contract_appraisal_results.csv"
DELAY_SECONDS = 1  # Be polite to the Adam4EVE server

# --- Adam4EVE base URL for full page scraping ---
BASE_URL = "https://www.adam4eve.eu/contract_price.php"
FORGE_REGION_ID = 10000002  # The Forge
DAYS = 30

results = []
total_sum = 0.0

print("Reading input file...")
with open(INPUT_CSV, newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        item_name = row["Item Name"].strip()
        quantity = int(row["Quantity"])
        type_id = row["TypeID"]

        if not type_id or type_id == '':
            print(f"Skipping {item_name}, missing TypeID")
            results.append({
                "Item Name": item_name,
                "Quantity": quantity,
                "TypeID": type_id,
                "Average Price (30d)": "N/A",
                "Total Value (ISK)": "N/A"
            })
            continue

        url = f"{BASE_URL}?typeID={type_id}&regionID={FORGE_REGION_ID}&days={DAYS}"
        print(f"Fetching price for: {item_name} (TypeID: {type_id})...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text

            # Extract all ISK values with M or k suffix
            raw_prices = re.findall(r">([\d.,]+)([Mk])<", html)
            prices = []
            for value, suffix in raw_prices:
                try:
                    number = float(value.replace(',', '.'))
                    multiplier = 1_000_000 if suffix == 'M' else 1_000
                    price_in_isk = number * multiplier
                    prices.append(price_in_isk)
                except:
                    continue

            if prices:
                median_price = statistics.median(prices)
                # Filter out prices that deviate too much from the median (e.g. > ±30%)
                filtered_prices = [p for p in prices if 0.7 * median_price <= p <= 1.3 * median_price]

                if filtered_prices:
                    avg_price_isk = sum(filtered_prices) / len(filtered_prices)
                    avg_price_mil = avg_price_isk / 1_000_000  # convert to M for output
                else:
                    avg_price_isk = None
                    avg_price_mil = None
            else:
                avg_price_isk = None
                avg_price_mil = None

            total_value = avg_price_isk * quantity if avg_price_isk else None
            if total_value:
                total_sum += total_value

        except Exception as e:
            print(f"Error fetching {item_name}: {e}")
            avg_price_mil = None
            total_value = None

        results.append({
            "Item Name": item_name,
            "Quantity": quantity,
            "TypeID": type_id,
            "Average Price (30d)": round(avg_price_mil, 2) if avg_price_mil else "N/A",
            "Total Value (ISK)": round(total_value, 2) if total_value else "N/A"
        })

        time.sleep(DELAY_SECONDS)

# --- Format total summary line ---
def format_isk_millions(value):
    return f"{round(value / 1_000_000, 2)}M"

summary_row = {
    "Item Name": "TOTAL VALUE",
    "Quantity": "",
    "TypeID": "",
    "Average Price (30d)": "",
    "Total Value (ISK)": format_isk_millions(total_sum)
}

# --- Write output ---
print(f"\nWriting results to {OUTPUT_CSV}...")
with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ["Item Name", "Quantity", "TypeID", "Average Price (30d)", "Total Value (ISK)"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)
    writer.writerow(summary_row)

print("Done!")
