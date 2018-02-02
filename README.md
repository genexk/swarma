# SwarmA
This project aims to provide a centralized tool built on top of Django and Ansible to manage multiple instances of Docker Swarm clusters.

## Get started
### Rerequisites
Before you can deploy this tool, you will need to install Docker.
### To Install
- clone this repo
```
git clone https://github.com/genexk/swarma.git
```
- build the docker image Dockerfile
```
cd swarma
docker build -t swarma .
```
- deploy the image
```
docker run -d -p 80:8000 swarma
```
