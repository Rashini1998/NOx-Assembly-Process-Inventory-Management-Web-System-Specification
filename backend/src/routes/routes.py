from flask import Blueprint, request, jsonify
from src.controllers.inventory_controller import process_inventory_csv
from src.controllers.status_controller import process_status_csv
from src.models.inventory_history import InventoryHistory
from src import db

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