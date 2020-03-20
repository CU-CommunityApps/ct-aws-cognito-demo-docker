# ct-aws-cognito-demo-docker

A super simple Python Flask App deployed in a Docker Container

## How to run the container locally

In this mode, you can hack on `app.py` and the server will reload it when changes are saved.

```
docker build -t ct-aws-cognito-demo-docker .
docker run -it --rm -p 80:5000 -v $(pwd):/app ct-aws-cognito-demo-docker:latest
```

## Caveats

This should NOT be used for production purposes.