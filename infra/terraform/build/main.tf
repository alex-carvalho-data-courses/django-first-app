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

resource "docker_volume" "postgres_django" {
  name = "postgres-django"
}

resource "docker_image" "postgres" {
  name = "postgres:14"
}