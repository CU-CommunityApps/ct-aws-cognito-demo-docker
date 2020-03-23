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
