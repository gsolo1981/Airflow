FROM apache/airflow:2.7.1-python3.9

# Cambiar a usuario root para instalar paquetes del sistema
USER root

# Instalar dependencias del sistema para Oracle y SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    unzip \
    libaio1 \
    unixodbc \
    unixodbc-dev \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Microsoft ODBC Driver 18 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client
RUN mkdir -p /opt/oracle \
    && cd /opt/oracle \
    && wget -q https://download.oracle.com/otn_software/linux/instantclient/2340000/instantclient-basic-linux.x64-23.4.0.24.05.zip \
    && unzip instantclient-basic-linux.x64-23.4.0.24.05.zip \
    && rm instantclient-basic-linux.x64-23.4.0.24.05.zip \
    && echo /opt/oracle/instantclient_23_4 > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

# Configurar timezone del sistema
RUN ln -sf /usr/share/zoneinfo/America/Argentina/Buenos_Aires /etc/localtime \
    && echo "America/Argentina/Buenos_Aires" > /etc/timezone

# Volver al usuario airflow
USER airflow

# Instalar dependencias Python compatibles con Airflow 2.7.1
RUN pip install --no-cache-dir \
    "oracledb>=2.0.0" \
    "cx_Oracle==8.3.0" \
    "python-dotenv>=1.0.0" \
    "pandas>=2.0.0" \
    "openpyxl>=3.1.0" \
    "SQLAlchemy>=1.4.0,<2.0.0" \
    "pyodbc>=5.0.0"

# Configurar variables de entorno
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_23_4:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/opt/oracle/instantclient_23_4
ENV TZ=America/Argentina/Buenos_Aires