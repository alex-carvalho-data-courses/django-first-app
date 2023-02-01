# <img src="img/django.png" alt="django first app" width="30" style="vertical-align: middle;"> | django first app tutorial #

## What is this repository for? ##

### Quick summary

Project to follow the official [django - first app tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).  

## How do I get set up? ##

### Summary of set up

1. Install docker  
2. Install Terraform  
3. Install python  
4. Install poetry (python)  
5. Install linux postgres packages
6. Install python dependencies  
7. Generate docker image dependencies  
8. Deploy Terraform infrastructure  
9. Create database tables  

### Dependencies

#### <img src="img/docker.png" alt="docker" width="30" style="vertical-align: middle;"> Docker 20.10.22

#### <img src="img/terraform-logo.png" alt="terraform" width="30" style="vertical-align: middle;"> Terraform 1.3.7

#### <img src="img/python.png" alt="python" width="30" style="vertical-align: middle;"> Python 3.10.6

#### <img src="img/poetry-python.svg" alt="poetry" width="30" style="vertical-align: middle;"> Poetry 1.2.1

#### <img src="img/postgresql.png" alt="postgres" width="30" style="vertical-align: middle;"> PostgreSql Linux Dependencies  

To bridge **python** to **PostgreSql** the library **Psycopg2** is used.  
**Psycopg2** is a python wrapper for the official PostgreSql 
[libpq](https://www.postgresql.org/docs/current/libpq.html) C library.  
**Psycop2** is distributed in two python package flavors:  
- psycopg2-binary
- psycopg2

##### psycopg2-binary
This version has all necessary dependencies and nothing besides the python
package is required, making it a straightforward option. 
The downside from this approach is it can conflict with the official **libpq** 
if its present at the host OS, making it not recommended for production.

##### psycopg2
This is the recommended solution for production 
and the one used in this project.  
For this option, the following linux libraries need to be installed outside 
python:
- python3-dev
- libpq-dev

with the following command:
```shell
sudo apt install python3-dev libpq-dev
```

[psycopg documentation](https://www.psycopg.org/docs/install.html)  

### How to run tests

CHANGE_ME  

### Deployment instructions

#### 1. Install System Dependencies

From [Dependencies section](#dependencies)

#### 2. Install python dependencies  

```shell
poetry install
```

#### 3. Generate docker image dependencies

##### 3.1. Generate wheel for apache docker image

Build the current project:  

````shell
poetry build
````

Place the generated wills file at the **apache** docker image:  

```shell
cp dist/django_first_app-*-py3-none-any.whl infra/docker/django-polls-apache/
```

##### 3.2. Generate static giles for nginx docker image

Set environment variables for django setting to enable manage.py script:  

```shell
. ./django_mysite_settings_envs.sh
```

Run django static files generation 
(it's configured to output it directly into Docker image build dir):  

```shell
poetry run python manage.py collectstatic
```

#### 4. Deploy terraform infrastructure  

The Terraform infrastructure consists basically of a PostgreSql server.  
It has the following objects:
- Volume
- Image
- Container

The volume will contain the PostgreSql files and will enable to destroy the 
container and recreate it without losing the db content.  

The Terraform is split in two folders:
- build
- exec

##### 4.1. Terraform build folder

It creates the PostgreSql volume and downloads the Image from Docker hub.  
It should be executed once.

```shell
cd infra/terraform/build/ && terraform apply && terraform init && cd ../../..
```

##### 4.2. Terraform exec

It runs the PostgreSql server container.  
It should be executed every time you want to turn on the infrastructure.

###### First time

```shell
cd infra/terraform/exec/ && terraform apply && terraform init && cd ../../..
```

###### Other executions

```shell
cd infra/terraform/exec/ && terraform apply && cd ../../..
```

### Database configuration

```shell
poetry run python manage.py migrate
```

## Who do I talk to? ##

### Repo owner or admin

[alex carvalho](mailto:alex.carvalho.data@gmail.com)  

## CHANGE_ME - docker django image build command
```shell
 docker image build -t local/apache-httpd-mod-wsgi:0.3.0 --build-arg DOMAIN_NAME=mysite.com --build-arg DJANGO_PROJECT_NAME=mysite .
```
