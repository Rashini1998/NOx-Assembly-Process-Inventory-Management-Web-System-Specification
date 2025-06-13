from flask import Blueprint, request, jsonify
from src.controllers.inventory_controller import process_inventory_csv
from src.controllers.status_controller import process_status_csv
from src.controllers.inventory_availability_controller import process_availability_csv
from src.models.inventory_history import InventoryHistory
from src.models.inventory_history import InventoryHistoryNew
from src.models.status_model import LabelStatus
from src.models.status_model import LabelStatusNew
from src.models.inventory_availability_model import InventoryAvailability
from src.models.wip_inventories_history_model import WIP_Inventories
from src.models.IITS_Master_model import IITS_Master
from src.models.imm_setting_screen_model import IMM_Setting
# from src.models.New_Inventory_Master import New_Inventory_Master
from src import db
from flask import current_app
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy import text
from datetime import datetime,timedelta
from collections import defaultdict

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
            "ShelfTagUpdateDate": r.ShelfTagRegistrationDate,
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



# Get all inventory availability data for Vue table
@inventory_bp.route('/api/wip-inventories-histories', methods=['GET'])
def get_wip_inventories_histories():
    records = WIP_Inventories.query.all()
    data = []
    for r in records:
        data.append({
            "ASSY品番": r.ASSY品番,
            "SUBASSY品番": r.SUBASSY品番,
            "メーカ": r.メーカ,
            "出荷区分": r.出荷区分,
            "気密検査": r.気密検査,
            "SCU": r.SCU,
            "水蒸気検査": r.水蒸気検査,
            "特性検査": r.特性検査,
            "特性検査端数品": r.特性検査端数品,
            "アクセサリ": r.アクセサリ,
            "FA": r.FA,
            "FA端数品": r.FA端数品,
            "外観検査": r.外観検査,
            "更新日時": r.更新日時,

        })
    return jsonify(data)

# Get specific inventory availability data for given partNumber, process, start and end dates
@inventory_bp.route('/api/wip-inventories-histories-new', methods=['GET'])
def get_wip_inventories_histories_new():
    part_number = request.args.get('partNumber')
    process = request.args.get('process')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Validate required parameters
    if not part_number or not process:
        return jsonify({"error": "partNumber and process are required"}), 400

    # Validate the process parameter
    valid_processes = [
        '気密検査', 'SCU', '水蒸気検査', '特性検査', 
        '特性検査端数品', 'アクセサリ', 'FA', 'FA端数品', '外観検査'
    ]
    
    if process not in valid_processes:
        return jsonify({"error": f"Invalid process. Valid options: {', '.join(valid_processes)}"}), 400

    # Validate date parameters
    if not start_date or not end_date:
        return jsonify({"error": "Both startDate and endDate are required"}), 400

    try:
        start_dt = datetime.strptime(start_date, "%Y/%m/%d")
        end_dt = datetime.strptime(end_date, "%Y/%m/%d") + timedelta(days=1)
    except ValueError as e:
        return jsonify({"error": "Invalid date format. Use YYYY/MM/DD"}), 400

    # Build the query
    try:
        records = WIP_Inventories.query.filter(
            WIP_Inventories.ASSY品番 == part_number,
            WIP_Inventories.更新日時 >= start_dt,
            WIP_Inventories.更新日時 < end_dt
        ).with_entities(
            WIP_Inventories.更新日時,
            getattr(WIP_Inventories, process)
        ).order_by(WIP_Inventories.更新日時.asc()).all()

        # Format the response
        data = [{
            "timestamp": record.更新日時.isoformat() if record.更新日時 else None,
            "value": getattr(record, process)
        } for record in records]

        return jsonify({
            "success": True,
            "partNumber": part_number,
            "process": process,
            "startDate": start_date,
            "endDate": end_date,
            "data": data,
            "count": len(data)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

# Get all inventory availability data for Vue table
@inventory_bp.route('/api/iitsMaster', methods=['GET'])
def get_iits_master():
    records = IITS_Master.query.all()

    data = []
    for r in records:
        data.append({
            "品番": r.品番,
            "在庫管理グループ名称": r.在庫管理グループ名称,
            "基準在庫数": r.基準在庫数,
            "基準在庫上限数": r.基準在庫上限数,
            "基準在庫下限数": r.基準在庫下限数,
        })

    print("Total data sent in response:", len(data))
    return jsonify(data)


# Get all inventory availability data for given partNumber and the process
@inventory_bp.route('/api/nox_assy_inv_mgt_thresh', methods=['GET'])
def get_threshold_data():
    # Get query parameters
    part_number = request.args.get('partNumber')
    process = request.args.get('process')
    
    # Base query
    query = IITS_Master.query
    
    # Apply filters if parameters are provided
    if part_number:
        query = query.filter(IITS_Master.品番 == part_number)
    if process:
        query = query.filter(IITS_Master.在庫管理グループ名称 == process)
    
    # Execute query
    records = query.all()
    
    data = []
    for r in records:
        data.append({
            "品番": r.品番,
            "在庫管理グループ名称": r.在庫管理グループ名称,
            "基準在庫数": float(r.基準在庫数) if r.基準在庫数 is not None else None,
            "基準在庫上限数": float(r.基準在庫上限数) if r.基準在庫上限数 is not None else None,
            "基準在庫下限数": float(r.基準在庫下限数) if r.基準在庫下限数 is not None else None,
        })
    
    print(f"Threshold data sent in response for part {part_number} and process {process}: {len(data)} records")
    return jsonify(data)


@inventory_bp.route('/api/dynamic-table', methods=['GET'])
def get_dynamic_table():

    table_name = request.args.get('table')
    
    if not table_name:
        return jsonify({'error': 'Table name not provided'}), 400
    
    try:
        if table_name == 'inventory_history':
            # Get inventory history data
            records = InventoryHistoryNew.query.all()
            data = []
            for r in records:
                data.append({
                    "ASSY品番": r.ASSY品番,
                    "SUBASSY品番": r.SUBASSY品番,
                    "メーカ": r.メーカ,
                    "出荷区分": r.出荷区分,
                    "気密検査": r.気密検査,
                    "SCU": r.SCU,
                    "水蒸気検査": r.水蒸気検査,
                    "特性検査": r.特性検査,
                    "特性検査端数品": r.特性検査端数品,
                    "アクセサリ": r.アクセサリ,
                    "FA": r.FA,
                    "FA端数品": r.FA端数品,
                    "外観検査": r.外観検査,
                    "更新日時": r.更新日時
                })
            
            # Get column names from the first record if exists
            columns = list(data[0].keys()) if data else []
            
        elif table_name == 'realtime_shelf_label_status':
            # Get shelf label status data
            records = LabelStatusNew.query.all()
            data = []
            for r in records:
                data.append({
                    "棚札ID": r.棚札ID,
                    "品番": r.品番,
                    "次工程名称": r.次工程名称,
                    "加工Lot": r.加工Lot,
                    "数量": r.数量,
                    "作業状況": r.作業状況,
                    "棚札登録日時": r.棚札登録日時,
                    "棚札更新日時": r.棚札更新日時,
                    "滞留日数": r.滞留日数
                })
            
            # Get column names from the first record if exists
            columns = list(data[0].keys()) if data else []
            
        else:
            return jsonify({'error': 'Invalid table name'}), 400
        
        return jsonify({
            'columns': columns,
            'data': data
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching dynamic table data: {str(e)}")
        return jsonify({'error': 'Failed to fetch table data'}), 500
    

@inventory_bp.route('/api/imm-setting', methods=['GET'])
def get_imm_setting():
    records = IMM_Setting.query.all()
    data = []
    for r in records:
        data.append({
            "id":r.id,
            "設備グループID": r.設備グループID,
            "設備機番": r.設備機番,
            "設備グループ名称": r.設備グループ名称,
            "在庫管理グループID": r.在庫管理グループID,
            "在庫管理グループ名称": r.在庫管理グループ名称,
            "基準在庫日数": r.基準在庫日数,
            "基準在庫管理幅": r.基準在庫管理幅
        })
    return jsonify(data)
    

@inventory_bp.route('/api/imm-setting', methods=['POST'])
def add_imm_setting():
    data = request.json
    new_row = IMM_Setting(
        設備グループID=data['設備グループID'],
        設備機番=data['設備機番'],
        設備グループ名称=data['設備グループ名称'],
        在庫管理グループID=data['在庫管理グループID'],
        在庫管理グループ名称=data['在庫管理グループ名称'],
        基準在庫日数=data['基準在庫日数'],
        基準在庫管理幅=data.get('基準在庫管理幅')
    )
    db.session.add(new_row)
    db.session.commit()
    return jsonify({'message': 'Row added successfully'}), 201
