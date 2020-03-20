# ct-aws-cognito-demo-docker

A super simple Python Flask App deployed in a Docker Container

## Pull the container from Docker Hub

```
docker pull pauleallen/ct-aws-cognito-demo-docker:latest
```

## Build the container

```
docker build -t ct-aws-cognito-demo-docker .
```

## How to run the container on a server

If you build it locally:
```
 docker run --detach --restart always -p 80:5000 ct-aws-cognito-demo-docker:latest
```

If you pulled it from Docker Hub:
```
 docker run --detach --restart always -p 80:5000 pauleallen/ct-aws-cognito-demo-docker:latest
```


## How to run the container locally

In this mode, you can hack on `app.py` and the server will reload it when changes are saved.

Ensure your current working directory contains `app.py` before executing this command. To stop the container use `^C`.

```
docker run -it --rm -p 80:5000 -v $(pwd):/app ct-aws-cognito-demo-docker:latest
```

## Caveats

This should NOT be used for production purposes.