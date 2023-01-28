terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.1"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "postgres" {
  name = "postgres:14"
}

resource "docker_volume" "postgres_django" {
  name = "postgres-django"
}

resource "docker_image" "apache_httpd_mod_wsgi" {
  name = "local/apache-httpd-mod-wsgi"

  build {
    context = "../../docker/apache-httpd-mod-wsgi/"
    tag     = ["local/apache-httpd-mod-wsgi:0.4.0"]
    label = {
      author : "alex carvalho"
    }
  }
}

resource "docker_image" "django_mysite_polls" {
  name = "local/django-mysite-polls"

  depends_on = [docker_image.apache_httpd_mod_wsgi]

  build {
    context = "../../docker/django-mysite-polls/"
    tag     = ["local/django-mysite-polls:0.2.0"]
    build_args = {
      DJANGO_PROJECT_NAME : "mysite"
    }
    label = {
      author : "alex carvalho"
    }
  }
}