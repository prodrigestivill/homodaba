FROM python:3.8.3

ARG APP_SRC_PATH=homodaba

ENV PYTHONUNBUFFERED=1 \
  SECRET_KEY=${SECRET_KEY} \
  ES_DSL_HOSTS=${ES_DSL_HOSTS} \
  ALLOWED_HOSTS=${ALLOWED_HOSTS} \
  SQLITE_ROOT="/opt/app/sqlite" \
  IMPORT_ROOT="/opt/app/import"

WORKDIR /opt/app

# Directorio con la bbdd sqlite
VOLUME ${SQLITE_ROOT}

# Directorio para labores de importacion, escaneo...
# (csvs con la info de los medios, puntos de montaje de red para scanear...)
VOLUME ${IMPORT_ROOT}

ADD homodaba/python-requirements.txt /opt/app/homodaba/python-requirements.txt

RUN pip3 install -r homodaba/python-requirements.txt

EXPOSE 8000

COPY docker/app/init-homodaba.sh /opt/app/init-homodaba.sh

# Añadido cliente MariaDB para comprobar que el servicio está listo.
ARG db_engine
RUN if [ "x$db_engine" = "xmysql" ]; then apt-get update && apt-get install -y mariadb-client; fi

CMD ["/opt/app/init-homodaba.sh"]
