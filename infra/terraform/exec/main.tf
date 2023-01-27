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

resource "docker_image" "apache_httpd_mod_wsgi" {
  name = "local/apache-httpd-mod-wsgi:0.3.0"
  keep_locally = true
}

resource "docker_container" "django_mysite" {
  name = "django_mysite"
  image = docker_image.apache_httpd_mod_wsgi.name

  env = [
    "DJANGO_PROJECT_NAME=mysite",
    "DJANGO_POSTGRES_DB_HOST=postgres_django",
    "DJANGO_POSTGRES_DB_PORT=5432",
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
}