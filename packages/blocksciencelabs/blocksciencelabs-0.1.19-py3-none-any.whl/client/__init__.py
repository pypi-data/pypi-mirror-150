import common
import functools, json, operator, pickle, requests, subprocess, sys

LABS_API = "https://api.blocksciencelabs.com"
WHEEL_BASE_URL = "https://models-private.s3.us-east-2.amazonaws.com"
WHEEL_NAME = "pkg-0.0.0-py3-none-any.whl"

Config = dict[str, str]
    
class Client:
    def __init__(self, config: Config):
        if "email" not in config and "password" not in config:
            raise Exception(common.ERROR_MISSING_PARAMETERS)
        else:
            response = requests.post(f'{LABS_API}/login', config)
            if response.status_code == 400:
                raise Exception(response.text)
            elif response.status_code == 401:
                raise Exception(json.loads(response.text)["message"])
            else:
                self.account = json.loads(response.text)["payload"]
                
    def authenticated_request(self, method: str = "GET", endpoint: str = "ping", data: any = None):
        response = None;
        url = f'{LABS_API}/{endpoint}'
        headers = {"Authorization": f'Bearer {self.account["token"]}'}
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = request.post(url, headers=headers, data=data)
        else:
            response = request.get(url, headers=headers)
            
        return response

    def fetch_results(self, simulation_id):
        response = self.authenticated_request("GET", f'fetch-results?simulationId={simulation_id}')

        unserialized = []
        
        if response.status_code == 200:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--ignore-installed", "--no-warn-script-location", get_wheel_url(simulation_id)])
            for record in json.loads(response.text)["payload"]:
                unserialized.append(pickle.loads(bytes.fromhex(record["data"])))

            return functools.reduce(operator.iconcat, unserialized, [])    
        else:
            return []
    
def get_wheel_url(simulation_id):
        return f'{WHEEL_BASE_URL}/{simulation_id}/{WHEEL_NAME}'