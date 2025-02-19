FROM apache/airflow:2.10.3-python3.12

USER root

COPY requirements.txt ./requirements.txt
COPY ./config /opt/airflow/config

RUN rm -rf /var/lib/apt/lists/* && apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends gcc python3-dev openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to airflow user before running pip
USER airflow

RUN pip install --no-cache-dir -r ./requirements.txt

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64