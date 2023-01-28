FROM local/apache-httpd-mod-wsgi:0.4.0

##########
# Django #
##########
# for the command `django-admin startproject mysite`,
# DJANGO_PROJECT_NAME should be `mysite
# TODO: Fix css with apache setup
ARG DJANGO_PROJECT_NAME
ARG DJANGO_PROJECT_GIT_REPO
# Make args mandatory
ARG CHECK=${DJANGO_PROJECT_NAME:?}
ARG CHECK=${DJANGO_PROJECT_GIT_REPO:?}

ENV DJANGO_PROJECT_NAME=$DJANGO_PROJECT_NAME
ENV DJANGO_WSGI_PYTHON_PATH=/opt/www/python-project
ENV DJANGO_WSGI_PROJECT_DIR=$DJANGO_WSGI_PYTHON_PATH/$DJANGO_PROJECT_NAME
ENV DJANGO_WSGI_SCRIPT_ALIAS=$DJANGO_WSGI_PROJECT_DIR/wsgi.py
ENV APACHE_SITE_DOCUMENTS=/opt/www/documents
ENV POETRY_VIRTUALENVS_PATH=$DJANGO_WSGI_PYTHON_PATH/virtualenvs

COPY httpd.conf $HTTPD_PREFIX/conf/httpd.conf

RUN mkdir -p $DJANGO_WSGI_PYTHON_PATH, \
    mkdir -p $APACHE_SITE_DOCUMENTS
WORKDIR $DJANGO_WSGI_PYTHON_PATH

RUN git clone $DJANGO_PROJECT_GIT_REPO .; \
    git checkout apache; \
    poetry install --no-root; \
    DJANGO_WSGI_PYTHON_HOME=$(poetry env info --path); \
    chmod 777 $DJANGO_WSGI_PYTHON_HOME; \
    cd $HTTPD_PREFIX/conf; \
    sed -i'.bak' \
        -e "s;{{DJANGO_WSGI_SCRIPT_ALIAS}};$DJANGO_WSGI_SCRIPT_ALIAS;" \
        -e "s;{{DJANGO_WSGI_PYTHON_HOME}};$DJANGO_WSGI_PYTHON_HOME;" \
        -e "s;{{DJANGO_WSGI_PYTHON_PATH}};$DJANGO_WSGI_PYTHON_PATH;" \
        -e "s;{{DJANGO_WSGI_PROJECT_DIR}};$DJANGO_WSGI_PROJECT_DIR;" \
        -e "s;{{APACHE_SITE_DOCUMENTS}};$APACHE_SITE_DOCUMENTS;" \
        httpd.conf

# TODO: Add volume to store the cloned directory $DJANGO_WSGI_PYTHON_PATH
# TODO: Try to mount this volume with the local pycharm code

WORKDIR $HTTPD_PREFIX