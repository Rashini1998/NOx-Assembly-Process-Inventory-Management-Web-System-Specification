import pandas as pd
from datetime import datetime, timedelta
from src import db
from src.models.status_model import LabelStatus

# def parse_time_fragment(fragment: str):
#     try:
#         minutes, seconds = map(float, fragment.split(":"))
#         base_time = datetime(2025, 1, 1)  # Arbitrary fixed date
#         return base_time + timedelta(minutes=minutes, seconds=seconds)
#     except:
#         return None

def process_status_csv(file):
    try:
        df = pd.read_csv(file, encoding='utf-8-sig')
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        df = df.drop_duplicates(subset=['ProcessingLot'])

        existing_lots = {
            lot[0].strip() for lot in db.session.query(LabelStatus.ProcessingLot).all()
        }

        # Normalize ProcessingLot to full precision string
        # df['ProcessingLot'] = df['ProcessingLot'].apply(
        #     lambda x: '{0:.0f}'.format(x) if pd.notna(x) and isinstance(x, float) else str(x).strip()
        # )

        # Remove internal duplicates in CSV
        # df = df.drop_duplicates(subset=['ProcessingLot'])

        new_df = df[~df['ProcessingLot'].isin(existing_lots)]
        # new_df['PartNumber'] = new_df['PartNumber'].astype(str)
        new_df = new_df.where(pd.notnull(new_df), None)
        new_df['PartNumber'] = new_df['PartNumber'].apply(lambda x: str(int(x)) if pd.notna(x) and isinstance(x, float) else str(x).strip())
        # Normalize existing ProcessingLot values for matching
        # existing_lots = {
        #     str(lot[0]).strip() for lot in db.session.query(LabelStatus.ProcessingLot).all()
        # }

        # records = [
        #     LabelStatus(
        #         # ShelfTagID=str(row['ShelfTagID']).strip()[:16] if pd.notna(row['ShelfTagID']) else '',
        #         # PartNumber=str(row['PartNumber']).strip()[:20] if pd.notna(row['PartNumber']) else '',
        #         # NextProcessName=str(row['NextProcessName']).strip()[:200] if pd.notna(row['NextProcessName']) else '',
        #         # ProcessingLot=row['ProcessingLot'][:24] if pd.notna(row['ProcessingLot']) else '',
        #         # Quantity=int(float(row['Quantity'])) if pd.notna(row['Quantity']) else 0,
        #         # WorkStatus=int(float(row['WorkStatus'])) if pd.notna(row['WorkStatus']) else 0,
        #         # ShelfTagRegistrationDate=parse_time_fragment(row['ShelfTagRegistrationDate']),
        #         # ShelfTagUpdateDate=parse_time_fragment(row['ShelfTagUpdateDate']),
        #         # DurationOfStay=int(float(row['DurationOfStay'])) if pd.notna(row['DurationOfStay']) else 0
        #         # ShelfTagID=str(row['ShelfTagID']).strip()[:16] if pd.notna(row['ShelfTagID']) else '',
        #         # PartNumber=str(row['PartNumber']).strip()[:20] if pd.notna(row['PartNumber']) else '',
        #         # NextProcessName=str(row['NextProcessName']).strip()[:200] if pd.notna(row['NextProcessName']) else '',
        #         # ProcessingLot=row['ProcessingLot'][:24] if pd.notna(row['ProcessingLot']) else '',
        #         # Quantity=int(float(row['Quantity'])) if pd.notna(row['Quantity']) else 0,
        #         # WorkStatus=int(float(row['WorkStatus'])) if pd.notna(row['WorkStatus']) else 0,
        #         # ShelfTagRegistrationDate=str(row['ShelfTagRegistrationDate']).strip()[:200] if pd.notna(row['ShelfTagRegistrationDate']) else '',
        #         # ShelfTagUpdateDate= str(row['ShelfTagUpdateDate']).strip()[:200] if pd.notna(row['ShelfTagUpdateDate']) else '',
        #         # DurationOfStay=int(float(row['DurationOfStay'])) if pd.notna(row['DurationOfStay']) else 0
        #         ShelfTagID=row['ShelfTagID'],
        #         PartNumber=row['PartNumber'],
        #         NextProcessName=row['NextProcessName'],
        #         ProcessingLot=row['ProcessingLot'],
        #         Quantity=row['Quantity'],
        #         WorkStatus=row['WorkStatus'],
        #         ShelfTagRegistrationDate=row['ShelfTagRegistrationDate'],
        #         ShelfTagUpdateDate= row['ShelfTagUpdateDate'],
        #         DurationOfStay=row['DurationOfStay']
        #     )
        #     for _, row in df.iterrows()
        #     # if row['ProcessingLot'] not in existing_lots
        # ]
        records = [
            LabelStatus(
                ShelfTagID=row['ShelfTagID'],
                PartNumber=row['PartNumber'],
                NextProcessName=row['NextProcessName'],
                ProcessingLot=row['ProcessingLot'],
                Quantity=row['Quantity'],
                WorkStatus=row['WorkStatus'],
                ShelfTagRegistrationDate=row['ShelfTagRegistrationDate'],
                ShelfTagUpdateDate=row['ShelfTagUpdateDate'],
                DurationOfStay=row['DurationOfStay']
            )
        for _, row in new_df.iterrows()
]


        db.session.bulk_save_objects(records)
        db.session.commit()
        return {"message": f"{len(records)} status records inserted successfully."}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
