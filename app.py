"""
Simple Flask application to show Cognito JWT data
"""
import pprint
import json
import base64
import requests
import jwt
import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    """
    Grab and decode data from request headers and ALB headers
    """

    # https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html
    oidc_data = "NOT_FOUND"
    payload = {}

    if 'X-Amzn-Oidc-Data' in flask.request.headers:
        oidc_data = flask.request.headers['X-Amzn-Oidc-Data']

        # Step 1: Get the key id from JWT headers (the kid field)
        encoded_jwt = oidc_data
        jwt_headers = encoded_jwt.split('.')[0]
        decoded_jwt_headers = base64.b64decode(jwt_headers)
        decoded_jwt_headers = decoded_jwt_headers.decode("utf-8")
        decoded_json = json.loads(decoded_jwt_headers)
        kid = decoded_json['kid']
        print("===============decoded_jwt_headers===============")
        pprint.pprint(decoded_json)
        print("=================================================")

        # Step 2: Get the public key from regional endpoint
        region = 'us-east-1'
        url = 'https://public-keys.auth.elb.' + region + '.amazonaws.com/' + kid
        req = requests.get(url)
        pub_key = req.text

        # Step 3: Get the payload
        payload = jwt.decode(encoded_jwt, pub_key, algorithms=['ES256'])
        print("===============payload===========================")
        pprint.pprint(payload)
        print("=================================================")

    result = "<table border=1>"
    headers = dict(flask.request.headers)
    for header in headers:
        result += "<tr><td>"+header+"</td><td>"+headers[header]+"</td></tr>"

    for key in payload:
        result += "<tr><td>JWT Payload: "+str(key)+"</td><td>"+str(payload[key])+"</td></tr>"

    result += "</table>"
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
