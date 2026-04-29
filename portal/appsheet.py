import requests
import uuid
import datetime

# const de configuracion appsheet
APPSHEET_APP_ID = "8da6bee6-447d-42a1-94c1-a79d18b58102"
APPSHEET_ACCESS_KEY = "V2-IoQrd-VsB7I-nkrvs-WHNrw-M3MuK-1pk18-PpRHP-uX335"
BASE_URL = f"https://api.appsheet.com/api/v2/apps/{APPSHEET_APP_ID}/tables"

def get_headers():
    # retorna headers requeridos por appsheet
    return {
        "ApplicationAccessKey": APPSHEET_ACCESS_KEY,
        "Content-Type": "application/json"
    }

def execute_action(table, action, rows=[]):
    # invoca la api generica de appsheet
    url = f"{BASE_URL}/{table}/Action"
    payload = {
        "Action": action,
        "Properties": {"Locale": "es-ES"},
        "Rows": rows
    }
    try:
        req = requests.post(url, headers=get_headers(), json=payload)
        if req.status_code == 200:
            try:
                return True, req.json()
            except ValueError:
                return True, req.text # if response is empty or non-JSON
        else:
            try:
                return False, req.json()
            except ValueError:
                return False, req.text
    except Exception as e:
        return False, str(e)

def get_all(table):
    # obtiene todos los registros
    success, data = execute_action(table, "Find")
    if success and isinstance(data, list):
        filtered_data = []
        for item in data:
            if not item.get("ID") and not item.get("Row ID"):
                continue  # ignorar filas vacias de app sheet
            if "Row ID" in item:
                item["Row_ID"] = item["Row ID"]
            if "Categoría" in item:
                item["Categoria"] = item["Categoría"]
            if "email" in item:
                item["Email"] = item["email"]
            filtered_data.append(item)
        return filtered_data
    return []

def get_by_id(table, key_field, key_value):
    # consultar o verificar un registro
    all_data = get_all(table)
    return next((item for item in all_data if item.get(key_field) == key_value), None)

def create_record(table, data):
    # inserta registro asegurando un id unico
    if "ID" not in data:
        data["ID"] = str(uuid.uuid4())[:8]
    return execute_action(table, "Add", [data])

def update_record(table, data):
  
    return execute_action(table, "Edit", [data])

def delete_record(table, key_value):
    # elimina registro por su Row ID
    return execute_action(table, "Delete", [{"Row ID": key_value}])
