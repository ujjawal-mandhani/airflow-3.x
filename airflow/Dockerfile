FROM apache/airflow:latest
RUN pip install apache-airflow[elasticsearch] psycopg2-binary apache-airflow-providers-apache-spark apache-airflow-providers-oracle apache-airflow-providers-smtp apache-airflow-providers-amazon pandas
USER root 
ENV SPARK_HOME=/usr/local/share/spark
RUN SPARK_VERSION=$(curl -s https://downloads.apache.org/spark/ | grep -o 'spark-[0-9.]\+/' | sed 's#/##' | sort -V | tail -n 1) && \
    echo "https://downloads.apache.org/spark/$SPARK_VERSION/$SPARK_VERSION-bin-hadoop3.tgz" && \
    curl -fL "https://downloads.apache.org/spark/$SPARK_VERSION/$SPARK_VERSION-bin-hadoop3.tgz" | tar xfz - -C /usr/local/share && \
    mv "/usr/local/share/$SPARK_VERSION-bin-hadoop3" "$SPARK_HOME"
ENV PATH="$PATH:$SPARK_HOME/bin"
# COPY ./spark-cluster/sshd_config /etc/ssh/sshd_config
# COPY ./spark-cluster/ssh_config /etc/ssh/ssh_config
# RUN mkdir -p /opt/airflow/spark_scripts
# COPY ./spark-cluster/spark-jobs/spark_job.py /opt/airflow/spark_scripts/
RUN apt-get update -y && apt install default-jre default-jdk openssh-server -y
RUN apt update && apt install unzip && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip
RUN ./aws/install
USER airflow
# 
ENTRYPOINT [ "bash", "-c", "/entrypoint airflow db migrate && (/entrypoint airflow api-server & /entrypoint airflow scheduler & /entrypoint airflow dag-processor & /entrypoint airflow triggerer)" ]
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]
CMD []