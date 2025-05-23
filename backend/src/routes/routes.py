from flask import Blueprint, request, jsonify
from src.controllers.inventory_controller import process_inventory_csv
from src.controllers.status_controller import process_status_csv
from src.controllers.inventory_availability_controller import process_availability_csv
from src.models.inventory_history import InventoryHistory
from src.models.status_model import LabelStatus
from src.models.inventory_availability_model import InventoryAvailability
from src.models.wip_inventories_history_model import WIP_Inventories
from src.models.IITS_Master_model import IITS_Master
from src.models.New_Inventory_Master import New_Inventory_Master
from src import db
from flask import current_app
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy import text

inventory_bp = Blueprint('inventory', __name__)

# Upload data to the inventory_history table
@inventory_bp.route('/api/upload-inventory', methods=['POST'])
def upload_inventory():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    result = process_inventory_csv(file)
    return jsonify(result), 200

# Get inventory data for Vue table
@inventory_bp.route('/api/inventory-history', methods=['GET'])
def get_inventory_history():
    records = InventoryHistory.query.all()
    data = []
    for r in records:
        data.append({
            "manufacturer": r.Manufacturer,
            "assyNumber": r.ASSY_Part_Number,
            "subassyNumber": r.SUBASSY_Part_Number,
            "classification": r.Shipping_Classification,
            "airtightness": r.Airtightness_Inspection,
            "scu": r.SCU,
            "waterVapor": r.Water_Vapor_Test,
            "inspection": r.Characteristic_Inspection,
            "fractional": r.Characteristic_Inspection_Fractional_Items,
            "accessories": r.Accessories,
            "fa": r.FA,
            "faFractional": r.FA_Fractional_Items,
            "visual": r.Visual_Inspection
        })
    return jsonify(data)

# Upload data to the realtime shelf label status table
@inventory_bp.route('/api/upload-status', methods=['POST'])
def upload_status():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    result = process_status_csv(file)
    return jsonify(result), 200


# Get inventory data for Vue table
@inventory_bp.route('/api/label-status', methods=['GET'])
def get_label_status():
    records = LabelStatus.query.all()
    data = []
    for r in records:
        data.append({
            "ShelfTagID": r.ShelfTagID,
            "PartNumber": r.PartNumber,
            "NextProcessName": r.NextProcessName,
            "ProcessingLot": r.ProcessingLot,
            "Quantity": r.Quantity,
            "WorkStatus": r.WorkStatus,
            "ShelfTagRegistrationDate": r.ShelfTagRegistrationDate,
            "ShelfTagUpdateDate": r.ShelfTagUpdateDate,
            "DurationOfStay": r.DurationOfStay
        })
    return jsonify(data)

# Upload data to the spare capacity weekly table
@inventory_bp.route('/api/upload-availability', methods=['POST'])
def upload_availability():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    result = process_availability_csv(file)
    return jsonify(result), 200

# Get inventory availability data for Vue table
@inventory_bp.route('/api/inventory-availability', methods=['GET'])
def get_inventory_availability():
    records = InventoryAvailability.query.all()
    data = []
    for r in records:
        data.append({
            "ProductNumber": r.Product_Number,
            "Manufacturer": r.Manufacturer,
            "ShippingClassification": r.Shipping_Classification,
            "AirtightnessInspection": r.Airtightness_Inspection,
            "SCU": r.SCU,
            "CharacteristicInspection": r.Characteristic_Inspection,
            "CharacteristicInspectionOddLot": r.Characteristic_Inspection_Odd_Lot,
            "Accessories": r.Accessories,
            "FA": r.FA,
            "FAFractionalItems": r.FA_Fractional_Items,
            "VisualInspection": r.Visual_Inspection,
            "StockReceiptRecord": r.Stock_Receipt_Record,
            "PreShipmentInventory": r.Pre_Shipment_Inventory,
            "Plan1": r.Plan_1,
            "Plan2": r.Plan_2,
            "Plan3": r.Plan_3,
            "Plan4": r.Plan_4,
            "Plan5": r.Plan_5,
            "Plan6": r.Plan_6,
            "Plan7": r.Plan_7,
            "Updated": r.Updated,

        })
    return jsonify(data)

# Refresh
@inventory_bp.route('/api/refresh-config', methods=['GET'])
def get_refresh_config():
    refreshInterval = current_app.config.get("REFRESH_INTERVAL", 1)
    return jsonify({"refresh_interval": refreshInterval})



# Get inventory availability data for Vue table
@inventory_bp.route('/api/wip-inventories-histories', methods=['GET'])
def get_wip_inventories_histories():
    records = WIP_Inventories.query.all()
    data = []
    for r in records:
        data.append({
            "ASSYPartNumber": r.ASSY_Part_Number,
            "SUBASSY": r.SUBASSY,
            "Manufacturer": r.Manufacturer,
            "ShippingClass": r.Shipping_Class,
            "AirtightInspection": r.Airtight_inspection,
            "SCU": r.SCU,
            "WaterVaporInspection": r.Water_Vapor_Inspection,
            "CharacteristicsInspection": r.Characteristics_inspection,
            "CharacteristicInspectionOddLot": r.Characteristic_inspection_odd_lot,
            "Accessories": r.Accessories,
            "FA": r.FA,
            "FAFractionalItems": r.FA_fractional_items,
            "VisualInspection": r.Visual_inspection,
            "Updated": r.Updated,

        })
    return jsonify(data)

# Get inventory availability data for Vue table

@inventory_bp.route('/api/iitsMaster', methods=['GET'])
def get_iits_master():
    records = IITS_Master.query.all()
    print("Total records fetched from DB:", len(records))
    
    group_names = set(r.Inventory_Management_Group_Name for r in records)
    print("Group names retrieved:", group_names)

    data = []
    for r in records:
        data.append({
            "Part_Number": r.Part_Number,
            "Inventory_Management_Group_Name": r.Inventory_Management_Group_Name,
            "Standard_Stock_Quantity": r.Standard_Stock_Quantity,
            "Standard_Inventory_Limit": r.Standard_Inventory_Limit,
            "Standard_Stock_Minimum_Quantity": r.Standard_Stock_Minimum_Quantity,
        })

    print("Total data sent in response:", len(data))
    return jsonify(data)


@inventory_bp.route('/api/raw_iits_test', methods=['GET'])
def raw_iits_test():
    result = db.session.execute(text("SELECT DISTINCT Inventory_Management_Group_Name FROM nox_assy_inv_mgt_thresh"))
    groups = [row[0] for row in result]
    print("Distinct groups from raw SQL:", groups)
    
    all_rows = db.session.execute(text("SELECT * FROM nox_assy_inv_mgt_thresh"))
    all_rows_list = [dict(row) for row in all_rows]
    print(f"Total rows fetched with raw SQL: {len(all_rows_list)}")
    
    return jsonify({
        "distinct_groups": groups,
        "total_rows": len(all_rows_list),
        "sample_row": all_rows_list[0] if all_rows_list else None
    })

@inventory_bp.route('/api/all-new-interim-transactions', methods=['GET'])
def get_new_inventory():
    records = New_Inventory_Master.query.all()
    # count = len(records)  # Correct way to count records
    # print("Count:", count)
    data = []
    for r in records:
        data.append({
                "ASSYPartNumber" : r.ASSYPartNumber,
                "SUBASSY" : r.SUBASSY,
                "Manufacturer" : r.Manufacturer,
                "ShippingClass" : r.ShippingClass,
                "AirtightInspection": r.AirtightInspection,
                "SCU" : r.SCU,
                "WaterVaporInspection" : r.WaterVaporInspection,
                "CharacteristicsInspection" : r.CharacteristicsInspection,
                "CharacteristicInspectionOddLot" : r.CharacteristicInspectionOddLot,
                "Accessories" : r.Accessories,
                "FA" : r.FA,
                "FAFractionalItems" : r.FAFractionalItems,
                "VisualInspection" : r.VisualInspection,
                # "Updated" : r.Updated,
                "Updated": r.Updated.isoformat() if r.Updated else None,
                "InventoryManagementGroupName" : r.InventoryManagementGroupName,
                "StandardStockQuantity" : r.StandardStockQuantity,
                "StandardInventoryLimit" : r.StandardInventoryLimit,
                "StandardStockMinimumQuantity" : r.StandardStockMinimumQuantity,

        })
    return jsonify(data)


# @inventory_bp.route('/api/distinct-im-groups', methods=['GET'])
# def distinct_groups():
#     result = db.session.execute(text("SELECT DISTINCT InventoryManagementGroupName FROM all_new_interim_transactions"))
#     return jsonify([row[0] for row in result])



# @inventory_bp.route('/api/all-data', methods=['GET'])
# def all_groups():
#     results = db.session.execute(text("SELECT *  FROM all_new_interim_transactions"))
#     return jsonify([row[0] for row in results])


@inventory_bp.route('/api/all-results', methods=['GET'])
def get_new_inventory_data():
    # Count total rows
    result = db.session.execute(text("SELECT COUNT(*) FROM all_new_interim_transactions"))
    count = result.scalar()
    print("Total rows in DB table:", count)

    # Fetch limited rows with SQL Server syntax
    result2 = db.session.execute(text("SELECT TOP 10 * FROM all_new_interim_transactions"))
    rows = result2.fetchall()

    # Get column names from the ResultProxy metadata
    keys = result2.keys()

    print("Sample rows:", rows)
    print("Column keys:", keys)

    # Map rows to dicts manually
    data = [dict(zip(keys, row)) for row in rows]

    return jsonify(data)
