import requests
import json



class PigeonsDB:

    __connection = None
    __index_path = None

    @staticmethod
    def search(query_text, k, metadata_filters=None, keywords=None):
        if PigeonsDB.__connection is None:
            print("Error: Connection not initialized.")
            return

        url = "http://test-search-1248249294.us-east-2.elb.amazonaws.com:8080/search"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_path,
            "query_text": query_text,
            "k": k,
            "metadata_filters": metadata_filters,
            "keywords": keywords
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print the response
        print(response.text)

    @staticmethod
    def init(API, DB_Name):
        index_path, connection = PigeonsDB.get_db_info(API, DB_Name)
        if connection:
            PigeonsDB.__connection = connection
            PigeonsDB.__index_path = index_path
        else:
            print("API key or DB name not found")

    @staticmethod
    def get_db_info(api_key, db_name):
        url = "http://ec2-52-14-162-65.us-east-2.compute.amazonaws.com/api/v1/sdk/get-db-info"
        headers = {"Content-Type": "application/json"}
        data = {"api_key": api_key, "dbname": db_name}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Extract data from the response
        db_info = response.json().get('DB info', {})
        index_path = db_info.get('index_path')

        # Create db object with specific keys
        keys = ['dbname', 'user', 'password', 'host']
        connection = {key: db_info.get(key) for key in keys}

        return index_path, connection


    @staticmethod
    def add(documents, metadata_list):
        if PigeonsDB.__connection is None:
            print("Error: Connection not initialized.")
            return

        url = "http://add-dev-177401989.us-east-2.elb.amazonaws.com:8080/add_documents"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_path,
            "documents": documents,
            "metadata_list": metadata_list
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print the response
        print(response.text)



