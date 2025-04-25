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
