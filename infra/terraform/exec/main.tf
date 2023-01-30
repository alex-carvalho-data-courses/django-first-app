terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "2.25.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "django_network" {
  name = "django-network"
}

resource "docker_image" "postgres" {
  name = "postgres:14"
  keep_locally = true
}

resource "docker_container" "postgres_django" {
  name = "postgres_django"
  image = docker_image.postgres.name

  env = [
    "POSTGRES_DB=django_db",
    "POSTGRES_USER=django",
    "POSTGRES_PASSWORD=alex123x"
  ]

  networks_advanced {
    name = docker_network.django_network.name
  }

  volumes {
    container_path = "/var/lib/postgresql/data"
    volume_name = "postgres-django"
  }

  ports {
    internal = 5432
    external = 5432
  }
}

resource "docker_image" "django_polls_apache" {
  name = "local/django-polls-apache:latest"
  keep_locally = true
}

resource "docker_container" "django_polls_apache" {
  name = "django-polls-apache"
  image = docker_image.django_polls_apache.name

  depends_on = [docker_container.postgres_django]

  env = [
    "DJANGO_PROJECT_NAME=mysite",
    "DJANGO_POSTGRES_HOST=postgres_django",
    "DJANGO_POSTGRES_PORT=5432",
    "DJANGO_POSTGRES_DB=django_db",
    "DJANGO_POSTGRES_USER=django",
    "DJANGO_POSTGRES_PASSWORD=alex123x"
  ]

  networks_advanced {
    name = docker_network.django_network.name
  }

  ports {
    internal = 80
    external = 8081
  }

  # TODO: Test back the local volume binding
  #volumes {
  #    container_path = "/opt/www/python-project"
  #    host_path = "/home/alex/00alex/git/courses/django-first-app"
  #  }
}

resource "docker_image" "django_polls_nginx_static" {
  name = "nginx:1.23"
}

resource "docker_container" "django_polls_nginx_static" {
  name  = "django-polls-nginx-static"
  image = docker_image.django_polls_nginx_static.name

  networks_advanced {
    name = docker_network.django_network.name
  }

  ports {
    internal = 80
    external = 8082
  }

  volumes {
    container_path = "/usr/share/nginx/html"
    host_path = "/home/alex/00alex/git/courses/django-first-app/infra/docker/django-polls-apache"
  }
}