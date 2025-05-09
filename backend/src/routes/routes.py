from flask import Blueprint, request, jsonify
from src.controllers.inventory_controller import process_inventory_csv
from src.controllers.status_controller import process_status_csv
from src.controllers.inventory_availability_controller import process_availability_csv
from src.models.inventory_history import InventoryHistory
from src.models.status_model import LabelStatus
from src.models.inventory_availability_model import InventoryAvailability
from src import db
from flask import current_app

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
            "Updated": r.Updated,

        })
    return jsonify(data)

# Refresh
@inventory_bp.route('/api/refresh-config', methods=['GET'])
def get_refresh_config():
    refreshInterval = current_app.config.get("REFRESH_INTERVAL", 1)
    return jsonify({"refresh_interval": refreshInterval})
