This tool fetches 30-day average contract prices from Adam4EVE using TypeIDs and appraises a list of EVE Online items. NOT FULLY COMPLETE!

Adam4EVE Contract Appraisal Tool
================================

This tool fetches 30-day average contract prices from Adam4EVE using TypeIDs
and appraises a list of EVE Online items. Outlier prices (±30% from median)
are filtered for cleaner valuation.

FILES INCLUDED
--------------
1. adam4eve_price_fetcher.py          - Main Python script
2. eve_items_with_typeids.csv         - Your item list with matched TypeIDs
3. invTypes.csv                       - Master item database to resolve TypeIDs pulled from (https://www.fuzzwork.co.uk/dump/latest/)

HOW TO USE
----------
1. Make sure you have Python 3 installed.
2. Open terminal / CMD in this folder and run:

    pip install requests

3. Run the script:

    python adam4eve_price_fetcher.py

4. Your result will be saved to:

    contract_appraisal_results.csv

HOW TO ADD NEW ITEMS
---------------------
1. Open `invTypes.csv` and search for the item name to find its `TYPEID`.
2. Add a new row to `eve_items_with_typeids.csv` with:
   - Item Name
   - Quantity
   - TypeID (from invTypes)
3. Save the file and re-run the script.

NOTE: Items without contract price data or invalid TypeIDs will be skipped.

Fly dangerous o7
