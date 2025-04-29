FROM apache/airflow:2.10.5
#FROM acryldata/airflow-datahub:latest

ARG AIRFLOW_VERSION=2.10.5

COPY airflow.requirements.txt /opt/airflow/airflow.requirements.txt

COPY msodbcsql18.sh /opt/microsoft/msodbcsql18.sh

USER root

RUN rm -rf /var/lib/apt/lists/*

#RUN bash /opt/microsoft/msodbcsql18.sh

# Add Microsoft repo and install msodbcsql18 + mssql-tools
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends\
    build-essential \
    ca-certificates \
    libssl-dev \
    libffi-dev \
    gcc \
    python3-dev \
    curl \
    apt-transport-https \
    gnupg2 \
    libxml2-dev \
    libxmlsec1-dev \
    libpq-dev \
    pkg-config \
    freetds-dev \
    firebird-dev \
    openjdk-17-jdk

RUN /opt/microsoft/msodbcsql18.sh

RUN apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow

RUN pip3 install --upgrade pip setuptools && \
    pip3 install acryl-datahub[airflow] && \
    pip3 install acryl-datahub-airflow-plugin[plugin-v2] && \
    pip3 install -U acryl-datahub[datahub-rest] && \
    pip3 install --no-cache-dir -r /opt/airflow/airflow.requirements.txt


#docker exec -it local-airflow-worker-1 airflow connections add  --conn-type datahub-rest datahub_rest_default --conn-host http://datahub-gms:8080