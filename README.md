# ct-aws-cognito-demo-docker

A super simple Python Flask App deployed in a Docker Container

This application is used as part of a demo that shows how to configure AWS Application Load Balancer and AWS Cognito to use Azure AD and SAML as identity providers. See [Configure AWS Application Load Balancer to use Cognito and Azure AD (ADFS/OIDC)](https://confluence.cornell.edu/x/kxXEFg) (private to Cornell community).

This image is automatically built and is available on Docker Hub at https://hub.docker.com/repository/docker/pauleallen/ct-aws-cognito-demo-docker.

## Miscellaneous Commands

### Pull the container from Docker Hub

```
docker pull pauleallen/ct-aws-cognito-demo-docker:latest
```

### Build the container locally

```
docker build -t ct-aws-cognito-demo-docker .
```

### Run the container on a server

If you built it locally:
```
docker run --detach --restart always -p 80:5000 ct-aws-cognito-demo-docker:latest
```

If you pulled it from Docker Hub:
```
docker run --detach --restart always -p 80:5000 pauleallen/ct-aws-cognito-demo-docker:latest
```


### How to run the container locally

In this mode, you can hack on `app.py` and the server will reload it when changes are saved.

Ensure your current working directory contains `app.py` before executing this command. To stop the container use `^C`.

```
docker run -it --rm -p 80:5000 -v $(pwd):/app ct-aws-cognito-demo-docker:latest
```

### Caveats

This should NOT be used for production purposes.

## JWT Handling for Ruby

Here's the Ruby equivalent to the JWT handling code in `app.py`:
```
  require 'base64'
  require 'json'
  require 'net/http'
  require 'jwt'
  
  # Step 1: Get the key id from JWT headers (the kid field)    
  encoded_jwt = request.headers['HTTP_X_AMZN_OIDC_DATA']
  jwt_headers = encoded_jwt.split('.').first
  logger.debug "jwt_headers: " + jwt_headers.to_s
  
  decoded_jwt_headers = Base64.decode64(jwt_headers)
  logger.debug "decoded_jwt_headers: " + decoded_jwt_headers.to_s
  logger.debug "decoded_jwt_headers.encoding: " + decoded_jwt_headers.encoding.to_s
  logger.debug "decoded_jwt_headers.class: " + decoded_jwt_headers.class.to_s
  
  decoded_jwt_headers = decoded_jwt_headers.encode("utf-8")
  logger.debug "decoded_jwt_headers: " + decoded_jwt_headers.to_s
  logger.debug "decoded_jwt_headers.encoding: " + decoded_jwt_headers.encoding.to_s
  logger.debug "decoded_jwt_headers.class: " + decoded_jwt_headers.class.to_s

  decoded_json = JSON.parse(decoded_jwt_headers)
  logger.debug "decoded_json.class: " + decoded_json.class.to_s
  
  kid = decoded_json['kid']
  logger.debug "kid: " + kid
  
  # Step 2: Get the public key from regional endpoint
  myresponse = Net::HTTP.get_response(URI('https://public-keys.auth.elb.us-east-1.amazonaws.com/' + kid))
  pub_key = myresponse.body
  logger.debug pub_key
  
      # # Step 3: Get the payload
  payload = JWT.decode(encoded_jwt, OpenSSL::PKey.read(pub_key), true, { algorithm: 'ES256' })
  logger.debug "=============== JWT PAYLOAD ==============="
  payload.first.each { |key, value|
    logger.debug "#{key}: #{value}"
  }

```