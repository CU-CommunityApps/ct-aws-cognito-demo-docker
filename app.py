# flask_web/app.py

import flask
from flask import Flask
import pprint
from logzero import logger
import jwt
import requests
import base64
import json
import pprint

app = Flask(__name__)

@app.route('/azure')
def azure():
  if 'X-Amzn-Oidc-Accesstoken' in flask.request.headers:
    oidc_accesstoken = flask.request.headers['X-Amzn-Oidc-Accesstoken'] 
  logger.debug("oidc_accesstoken")
  logger.debug(oidc_accesstoken)
  graph_data = requests.get(  # Use token to call downstream service
   'https://graph.microsoft.com/v1.0/me?$select=userPrincipalName,id,onPremisesSecurityIdentifier',
    headers={'Authorization': 'Bearer ' + oidc_accesstoken},
    ).json()
  logger.debug(graph_data)
  return(graph_data)

@app.route('/cognito')
def cognito():
  if 'X-Amzn-Oidc-Accesstoken' in flask.request.headers:
    oidc_accesstoken = flask.request.headers['X-Amzn-Oidc-Accesstoken'] 
  logger.debug("oidc_accesstoken")
  logger.debug(oidc_accesstoken)

  graph_data = requests.get(  # Use token to call downstream service
   'https://pea1-kognito-oidc.auth.us-east-1.amazoncognito.com/oauth2/userInfo',
    headers={'Authorization': 'Bearer ' + oidc_accesstoken},
    ).json()
  logger.debug(graph_data)
  return(graph_data)

@app.route('/')
def index():
  
# https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html  
  oidc_accesstoken = "NOT_FOUND"
  oidc_identity = "NOT_FOUND"
  oidc_data = "NOT_FOUND"
  payload = {}
  if 'X-Amzn-Oidc-Accesstoken' in flask.request.headers:
    oidc_accesstoken = flask.request.headers['X-Amzn-Oidc-Accesstoken']
  
  if 'X-Amzn-Oidc-Identity' in flask.request.headers:
    oidc_identity = flask.request.headers['X-Amzn-Oidc-Identity']

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
  for h in headers:
    result += "<tr><td>" + h + "</td><td>" + headers[h] + "</td></tr>"
    
  # result += "<tr><td><b>X-Amzn-Oidc-Identity</b></td><td>" + oidc_identity + "</td></tr>"
  # result += "<tr><td><b>X-Amzn-Oidc-Data</b></td><td>" + oidc_data + "</td></tr>"
  # result += "<tr><td><b>X-Amzn-Oidc-Accesstoken</b></td><td>" + oidc_accesstoken + "</td></tr>"

  for k in payload:
    result += "<tr><td>JWT Payload: " + str(k) + "</td><td>" + str(payload[k]) + "</td></tr>"

  result += "</table>"
  return result

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
