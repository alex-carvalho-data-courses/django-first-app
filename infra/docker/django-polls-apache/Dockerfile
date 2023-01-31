FROM local/apache-httpd-mod-wsgi:0.4.0

##########
# Django #
##########
# for the command `django-admin startproject mysite`,
# DJANGO_PROJECT_NAME should be 'mysite'
ARG DJANGO_PROJECT_NAME
ARG DJANGO_PROJECT_VERSION
# Make args mandatory
ARG CHECK=${DJANGO_PROJECT_NAME:?}
ARG CHECK=${DJANGO_PROJECT_VERSION:?}

ENV DJANGO_PROJECT_NAME=$DJANGO_PROJECT_NAME
ENV DJANGO_WSGI_PYTHON_PATH=/opt/www/python-project
ENV DJANGO_WSGI_PROJECT_DIR=$DJANGO_WSGI_PYTHON_PATH/$DJANGO_PROJECT_NAME
ENV DJANGO_WSGI_SCRIPT_ALIAS=$DJANGO_WSGI_PROJECT_DIR/wsgi.py
ENV POETRY_VIRTUALENVS_PATH=/opt/www//virtualenvs

COPY httpd.conf $HTTPD_PREFIX/conf/httpd.conf

RUN mkdir -p $DJANGO_WSGI_PROJECT_DIR
WORKDIR $DJANGO_WSGI_PYTHON_PATH

COPY pyproject.toml $DJANGO_WSGI_PYTHON_PATH
# TODO: Calculate dynamically the wheels version based on DJANGO_PROJECT_VERSION
COPY django_first_app-0.2.0-py3-none-any.whl $DJANGO_WSGI_PYTHON_PATH
COPY wsgi.py $DJANGO_WSGI_PROJECT_DIR

RUN sed -i'.bak' \
        "s/{{DJANGO_PROJECT_VERSION}}/$DJANGO_PROJECT_VERSION/" \
        pyproject.toml; \
    poetry install --no-root; \
    DJANGO_WSGI_PYTHON_HOME=$(poetry env info --path); \
    chmod 777 $DJANGO_WSGI_PYTHON_HOME; \
    cd $HTTPD_PREFIX/conf; \
    sed -i'.bak' \
        -e "s;{{DJANGO_WSGI_SCRIPT_ALIAS}};$DJANGO_WSGI_SCRIPT_ALIAS;" \
        -e "s;{{DJANGO_WSGI_PYTHON_HOME}};$DJANGO_WSGI_PYTHON_HOME;" \
        -e "s;{{DJANGO_WSGI_PYTHON_PATH}};$DJANGO_WSGI_PYTHON_PATH;" \
        -e "s;{{DJANGO_WSGI_PROJECT_DIR}};$DJANGO_WSGI_PROJECT_DIR;" \
        httpd.conf

VOLUME $DJANGO_WSGI_PYTHON_PATH

WORKDIR $HTTPD_PREFIX