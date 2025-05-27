import pandas as pd
from src import db
from src.models.wip_inventories_history_model import WIP_Inventories


def wip_inventories_history_csv(file):
    try:
        df = pd.read_csv(file,encoding='utf-8-sig')
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]

        records = [
            WIP_Inventories(
                ASSY_Part_Number=row['ASSY_Part_Number'],
                SUBASSY=row['SUBASSY'],
                Manufacturer=row['Manufacturer'],
                Shipping_Class=row['Shipping_Class'],
                Airtight_inspection=row['Airtight_inspection'],
                SCU=row['SCU'],
                Water_Vapor_Inspection=row['Water_Vapor_Inspection'],
                Characteristics_inspection=row['Characteristics_inspection'],
                Characteristic_inspection_odd_lot=row['Characteristic_inspection_odd_lot'],
                Accessories=row['Accessories'],
                FA=row['FA'],
                FA_fractional_items=row['FA_fractional_items'],
                Visual_inspection=row['Visual_inspection'],
                Updated=row['Updated']
            )
            for _, row in df.iterrows()
        ]

        db.session.bulk_save_objects(records)
        db.session.commit()
        return {"message": f"{len(records)} records inserted successfully."}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

 # # def wip_inventories_history_csv(file):
# #     try:
# #         df = pd.read_csv(file,encoding='utf-8-sig')
# #         df.columns = [col.strip().replace(' ', '_') for col in df.columns]

# #         df['Shipping_Class'] = df['Shipping_Class'].astype(str).str.strip()
# #         existing_shipping_class = {
# #             str(lot[0]).strip() for lot in db.session.query(WIP_Inventories.Shipping_Class).all() if lot[0] is not None
# #         }


# #         new_df = df[~df['Shipping_Class'].isin(existing_shipping_class)]

# #         records = [
# #             WIP_Inventories(
# #                 ASSY_Part_Number=row['ASSY_Part_Number'],
# #                 SUBASSY=row['SUBASSY'],
# #                 Manufacturer=row['Manufacturer'],
# #                 Shipping_Class=row['Shipping_Class'],
# #                 Airtight_inspection=row['Airtight_inspection'],
# #                 SCU=row['SCU'],
# #                 Water_Vapor_Inspection=row['Water_Vapor_Inspection'],
# #                 Characteristics_inspection=row['Characteristics_inspection'],
# #                 Characteristic_inspection_odd_lot=row['Characteristic_inspection_odd_lot'],
# #                 Accessories=row['Accessories'],
# #                 FA=row['FA'],
# #                 FA_fractional_items=row['FA_fractional_items'],
# #                 Visual_inspection=row['Visual_inspection'],
# #                 Updated=row['Updated']
# #             )
# #             for _, row in new_df.iterrows()
# #         ]

# #         db.session.bulk_save_objects(records)
# #         db.session.commit()
# #         return {"message": f"{len(records)} records inserted successfully."}

# #     except Exception as e:
# #         db.session.rollback()
# #         return {"error": str(e)}

# def wip_inventories_history_csv(file):
#     try:
#         df = pd.read_csv(file, encoding='utf-8-sig')
#         df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        
#         df['Shipping_Class'] = df['Shipping_Class'].astype(str).str.strip()
#         df = df[df['Shipping_Class'].notna()]
#         df = df.drop_duplicates(subset=['ASSY_Part_Number', 'SUBASSY', 'Manufacturer', 'Shipping_Class'])


#         existing_shipping_class = {
#             str(lot[0]).strip() for lot in db.session.query(WIP_Inventories.Shipping_Class).all() if lot[0] is not None
#         }

#         new_df = df[~df['Shipping_Class'].isin(existing_shipping_class)]

#         inserted_count = 0
#         for _, row in new_df.iterrows():
#             try:
#                 record = WIP_Inventories(
#                     ASSY_Part_Number=row['ASSY_Part_Number'],
#                     SUBASSY=row['SUBASSY'],
#                     Manufacturer=row['Manufacturer'],
#                     Shipping_Class=row['Shipping_Class'],
#                     Airtight_inspection=row['Airtight_inspection'],
#                     SCU=row['SCU'],
#                     Water_Vapor_Inspection=row['Water_Vapor_Inspection'],
#                     Characteristics_inspection=row['Characteristics_inspection'],
#                     Characteristic_inspection_odd_lot=row['Characteristic_inspection_odd_lot'],
#                     Accessories=row['Accessories'],
#                     FA=row['FA'],
#                     FA_fractional_items=row['FA_fractional_items'],
#                     Visual_inspection=row['Visual_inspection'],
#                     Updated=datetime.strptime(row['Updated'], "%Y-%m-%d %H:%M:%S")
#                 )
#                 db.session.add(record)
#                 db.session.flush()
#                 inserted_count += 1
#             except Exception:
#                 db.session.rollback()
#                 continue

#         db.session.commit()
#         return {"message": f"{inserted_count} records inserted successfully."}

#     except Exception as e:
#         db.session.rollback()
#         print(f"Skipped row due to error: {e}")
#         traceback.print_exc()
#         return {"error": str(e)}


# import pandas as pd
# from src import db
# from src.models.wip_inventories_history_model import WIP_Inventories

# def wip_inventories_history_csv(file):
#     try:
#         df = pd.read_csv(file, encoding='utf-8-sig')
#         df.columns = [col.strip().replace(' ', '_') for col in df.columns]

#         # Ensure correct data types
#         df['Shipping_Class'] = df['Shipping_Class'].astype(str).str.strip()
#         df = df[df['Shipping_Class'].notna()]
#         df = df.drop_duplicates(subset=['Updated', 'ASSY_Part_Number', 'SUBASSY', 'Manufacturer', 'Shipping_Class'])

#         # Convert Updated column to datetime
#         df['Updated'] = pd.to_datetime(df['Updated'], errors='coerce')
#         df = df[df['Updated'].notna()]  # Drop rows with invalid datetime

#         # Query existing unique combinations to avoid duplicates
#         existing_keys = {
#             (
#                 str(row.Updated),
#                 row.ASSY_Part_Number,
#                 row.SUBASSY,
#                 row.Manufacturer,
#                 row.Shipping_Class
#             )
#             for row in db.session.query(
#                 WIP_Inventories.Updated,
#                 WIP_Inventories.ASSY_Part_Number,
#                 WIP_Inventories.SUBASSY,
#                 WIP_Inventories.Manufacturer,
#                 WIP_Inventories.Shipping_Class
#             ).all()
#         }

#         inserted_count = 0

#         for _, row in df.iterrows():
#             unique_key = (
#                 str(row['Updated']),
#                 row['ASSY_Part_Number'],
#                 row['SUBASSY'],
#                 row['Manufacturer'],
#                 row['Shipping_Class']
#             )

#             if unique_key in existing_keys:
#                 continue  # Skip duplicate

#             try:
#                 record = WIP_Inventories(
#                     ASSY_Part_Number=row['ASSY_Part_Number'],
#                     SUBASSY=row['SUBASSY'],
#                     Manufacturer=row['Manufacturer'],
#                     Shipping_Class=row['Shipping_Class'],
#                     Airtight_inspection=row['Airtight_inspection'],
#                     SCU=row['SCU'],
#                     Water_Vapor_Inspection=row['Water_Vapor_Inspection'],
#                     Characteristics_inspection=row['Characteristics_inspection'],
#                     Characteristic_inspection_odd_lot=row['Characteristic_inspection_odd_lot'],
#                     Accessories=row['Accessories'],
#                     FA=row['FA'],
#                     FA_fractional_items=row['FA_fractional_items'],
#                     Visual_inspection=row['Visual_inspection'],
#                     Updated=row['Updated']
#                 )
#                 db.session.add(record)
#                 db.session.flush()
#                 inserted_count += 1
#             except Exception:
#                 db.session.rollback()
#                 continue

#         db.session.commit()
#         return {"message": f"{inserted_count} records inserted successfully."}

#     except Exception as e:
#         db.session.rollback()
#         return {"error": str(e)}
