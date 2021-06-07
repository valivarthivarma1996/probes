
# TODO
# 1. Installting deps - DONE
# 2. Application Bootstrap  code and env variables
# 3. Introspecting a token - ISV logic
# 4. Exposing this as an API
# 5. Testing & Debugging
# 6. Logging & Exception
# 7. Docker File and deployment

# Inbuilt Packages
from flask import Flask, request
import yaml
import requests
import logging
import traceback

def read_config():

    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file.read())
    return config

config = read_config()

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
app.config.update(
    DEBUG=True,
    TESTING=True,
    SECRET=config.get('APP_SECRET'),
    CONFIG=config
)


def introspect_isv_token(token: str) -> bool:
    """
    Introspect ISV token and check whether token is valid or not
    :param token: ISV token of the user
    :return: boolean (returns True if token is valid else False)
    :raise: N/A
    """
    url = f"{app.config['CONFIG']['ISV_BASE_URL']}{app.config['CONFIG']['ISV_INTROSPECT_URL']}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": app.config['CONFIG']['ISV_CLIENT_ID'],
        "client_secret": app.config['CONFIG']['ISV_CLIENT_SECRET'],
        "token": token
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()
        logging.info(f"Token status: {data['active']}")
        return data.get('active')
    else:
        raise Exception(f"Introspection call failed ! {response.text} | {response.status_code}")


@app.route('/', methods=['GET'])
def index():
    return "Hello World", 200


@app.route('/introspect', methods=['POST'])
def introspect():
    try:
        logging.info("Running introspection !")
        # Step 1. Check request for API Key
        user_api_key = request.headers['API-KEY']
        application_api_key = app.config['CONFIG']['API_KEY']
        if user_api_key != application_api_key:
            logging.error(f"Wrong API Key ! {user_api_key}")
            return "Unauthorized", 401

        # Step 2. Check for ISV token
        request_json = request.get_json()
        if not request_json or "token" not in request_json:
            return "Bad Request", 400

        # Step 3. Introspect ISV token
        introspect_status = introspect_isv_token(token=request_json.get('token'))

        # Step 4. Prepare response and return
        if introspect_status == True:
            return "Token Valid", 200
        return "Token Invalid", 401
    except Exception as e:
        logging.error(f"Exception: {str(e)} | Traceback: {traceback.format_exc()}")
        return "Something went wrong", 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

