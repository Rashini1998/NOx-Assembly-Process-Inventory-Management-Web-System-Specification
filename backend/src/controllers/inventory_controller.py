# import csv
# from src.models.inventory_history import InventoryHistory
# from src import db

# def import_inventory_data_from_csv(csv_file_path):
#     with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
#         reader = csv.DictReader(csvfile, delimiter='\t')  # or ',' if needed

#         for row in reader:
#             row = {k.strip(): v for k, v in row.items()}

#             inventory = InventoryHistory(
#                 ASSY_Part_Number=row.get("ASSY_Part _Number", ""),
#                 SUBASSY_Part_Number=row.get("SUBASSY_Part_Number", ""),
#                 Manufacturer=row.get("Manufacturer", ""),
#                 Shipping_Classification=row.get("Shipping_Classification", ""),
#                 Airtightness_Inspection=int(row.get("Airtightness_Inspection", 0) or 0),
#                 SCU=int(row.get("SCU", 0) or 0),
#                 Water_Vapor_Test=int(row.get("Water_Vapor_Test", 0) or 0),
#                 Characteristic_Inspection=int(row.get("Characteristic_Inspection", 0) or 0),
#                 Characteristic_Inspection_Fractional_Items=int(row.get("Characteristic_Inspection_Fractional_Items", 0) or 0),
#                 Accessories=int(row.get("Accessories", 0) or 0),
#                 FA=int(row.get("FA", 0) or 0),
#                 FA_Fractional_Items=int(row.get("FA_Fractional_Items", 0) or 0),
#                 Visual_Inspection=int(row.get("Visual_Inspection", 0) or 0),
#                 Update_Date_And_Time=row.get("Update_Date_And _Time", "")
#             )

#             db.session.add(inventory)

#         db.session.commit()
#         return f"✅ {reader.line_num - 1} records imported successfully."

import pandas as pd
from src import db
from src.models.inventory_history import InventoryHistory

def process_inventory_csv(file):
    try:
        df = pd.read_csv(file,encoding='utf-8-sig')
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]

        records = [
            InventoryHistory(
                ASSY_Part_Number=row['ASSY_Part_Number'],
                SUBASSY_Part_Number=row['SUBASSY_Part_Number'],
                Manufacturer=row['Manufacturer'],
                Shipping_Classification=row['Shipping_Classification'],
                Airtightness_Inspection=row['Airtightness_Inspection'],
                SCU=row['SCU'],
                Water_Vapor_Test=row['Water_Vapor_Test'],
                Characteristic_Inspection=row['Characteristic_Inspection'],
                Characteristic_Inspection_Fractional_Items=row['Characteristic_Inspection_Fractional_Items'],
                Accessories=row['Accessories'],
                FA=row['FA'],
                FA_Fractional_Items=row['FA_Fractional_Items'],
                Visual_Inspection=row['Visual_Inspection'],
                Update_Date_And_Time=row['Update_Date_And_Time']
            )
            for _, row in df.iterrows()
        ]

        db.session.bulk_save_objects(records)
        db.session.commit()
        return {"message": f"{len(records)} records inserted successfully."}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
