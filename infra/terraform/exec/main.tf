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

resource "docker_image" "postgres" {
  name = "postgres:14"
  keep_locally = true
}

resource "docker_container" "postgres_django" {
  name = "postgres_django"
  image = docker_image.postgres.name
  volumes {
    container_path = "/var/lib/postgresql/data"
    volume_name = "postgres-django"
  }
  env = [
    "POSTGRES_DB=django_db",
    "POSTGRES_USER=django",
    "POSTGRES_PASSWORD=alex123x"
  ]
  ports {
    internal = 5432
    external = 5432
  }
}