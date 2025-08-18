FROM apache/airflow:latest
RUN pip install apache-airflow[elasticsearch] psycopg2-binary apache-airflow-providers-apache-spark apache-airflow-providers-oracle apache-airflow-providers-smtp apache-airflow-providers-amazon pandas apache-airflow-providers-apache-spark
RUN pip install selenium beautifulsoup4 lxml python-dateutil webdriver-manager seleniumbase pyautogui dbt-core dbt-spark[PyHive]
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
RUN apt-get update -y && apt install default-jre default-jdk openssh-server xz-utils wget -y
RUN apt update && apt install unzip && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip
RUN ./aws/install
# Installation of Selenium
RUN mkdir -p /home/dependencies/
RUN curl -fSL https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz -o /home/dependencies/geckodriver-v0.36.0-linux64.tar.gz \
    && tar -xvzf /home/dependencies/geckodriver-v0.36.0-linux64.tar.gz --directory=/home/dependencies/ \
    && rm /home/dependencies/geckodriver-v0.36.0-linux64.tar.gz
RUN curl -fSL https://ftp.mozilla.org/pub/firefox/releases/136.0.4/linux-x86_64/en-US/firefox-136.0.4.tar.xz -o /home/dependencies/firefox-136.0.4.tar.xz && \
    tar -xJf /home/dependencies/firefox-136.0.4.tar.xz --directory=/home/dependencies/ \
    && rm /home/dependencies/firefox-136.0.4.tar.xz
RUN apt update -y && apt --fix-broken install -y && apt upgrade -y && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    (dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y)

RUN CHROME_VERSION=$(google-chrome --version | cut -d' ' -f3) && echo "Latest ChromeDriver version : $CHROME_VERSION" && \
    wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \ 
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver-linux64.zip
RUN apt-get install -y bzip2 libgtk-3-common libasound2 libdbus-glib-1-2 gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN ln -s  /home/dependencies/firefox/firefox /usr/bin/firefox
USER airflow
# 
ENTRYPOINT [ "bash", "-c", "/entrypoint airflow db migrate && (/entrypoint airflow api-server & /entrypoint airflow scheduler & /entrypoint airflow dag-processor & /entrypoint airflow triggerer)" ]
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]
CMD []