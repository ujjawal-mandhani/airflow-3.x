import requests
import json 
import time
from datetime import datetime
health_check_url = "http://elasticsearch-cont:9200/_cluster/health"
response = {}
response["status"] = "red"
time.sleep(40)
print(":::::::::::::Sleeping for 40 seconds")
# log_name = str(datetime.now().year)
log_name = "airflow"

while response["status"] in ["green", "yellow"]:
    try:
        response = requests.request("GET", health_check_url).json()
        print(response["status"])
    except:
        print("::::::Exception for elastic search")
        time.sleep(10)

index_url = f"http://elasticsearch-cont:9200/{log_name}"
response = requests.request("GET", index_url).json()

headers = { 
  'Content-Type': 'application/json'
}

print(response)
if response.get("error") not in ['', None] and response.get("error").get("root_cause")[0].get("type") == "index_not_found_exception":
    print("index does not exist")
    index_create_url = f'http://elasticsearch-cont:9200/{log_name}'
    payload = {
        "mappings": {
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "log_level": {
                    "type": "keyword"
                },
                "message": {
                    "type": "text"
                },
                "dag_id": {
                    "type": "keyword"
                },
                "task_id": {
                    "type": "keyword"
                },
                "run_id": {
                    "type": "keyword"
                },
                "map_index": {
                    "type": "integer"
                },
                "try_number": {
                    "type": "integer"
                },
                "hostname": {
                    "type": "keyword"
                },
                "log_id": {
                    "type": "text"
                }
            }
        }
    }
    response = requests.request("PUT", index_create_url, headers=headers, data=json.dumps(payload)).json()
    print(response)
else:
    print("index exist")