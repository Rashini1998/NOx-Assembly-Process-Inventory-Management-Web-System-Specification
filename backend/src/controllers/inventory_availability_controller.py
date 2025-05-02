import pandas as pd
from src import db
from src.models.inventory_availability_model import InventoryAvailability
from datetime import datetime

def process_availability_csv(file):
    try:
        df = pd.read_csv(file,encoding='utf-8-sig')
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        
        df = df.drop_duplicates(subset=['Product_Number'])

        existing_lots = {
            lot[0].strip() for lot in db.session.query(InventoryAvailability.Product_Number).all()
        }

        new_df = df[~df['Product_Number'].isin(existing_lots)]

        records = [
            InventoryAvailability(
                    Product_Number=row['Product_Number'],
                    Manufacturer = row ['Manufacturer'],
                    Shipping_Classification = row ['Shipping_Classification'],
                    Airtightness_Inspection	= row ['Airtightness_Inspection'],
                    SCU	= row['SCU'],
                    Water_Vapor_Test = row ['Water_Vapor_Test'],
                    Characteristic_Inspection = row['Characteristic_Inspection'],
                    Characteristic_Inspection_Odd_Lot = row['Characteristic_Inspection_Odd_Lot'],
                    Accessories = row['Accessories'],
                    FA 	= row['FA'],
                    FA_Fractional_Items = row['FA_Fractional_Items'],
                    Visual_Inspection = row['Visual_Inspection'],
                    Stock_Receipt_Record = row['Stock_Receipt_Record'],
                    Pre_Shipment_Inventory = row['Pre_Shipment_Inventory'],
                    Plan_1 	= row['Plan_1'],
                    Plan_2 	= row['Plan_2'],
                    Plan_3	= row['Plan_3'],
                    Plan_4 	= row['Plan_4'],
                    Plan_5 	= row['Plan_5'],
                    Plan_6 	= row['Plan_6'],
                    Plan_7 = row['Plan_7'],
                    # Updated = row['Updated']
                    Updated = datetime.strptime(row['Updated'], "%m/%d/%Y %H:%M")

            )
         for _, row in new_df.iterrows()

        ]

        db.session.bulk_save_objects(records)
        db.session.commit()
        return {"message": f"{len(records)} records inserted successfully."}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}