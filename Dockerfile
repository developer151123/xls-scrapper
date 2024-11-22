FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install python3.10 curl cron && \
    apt update && apt install python3-pip -y

RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

ARG CACHEBUST=1

WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt
RUN chmod +x start-scrapper.sh

# Copy scrapper-cron file to the cron.d directory
COPY scrapper-cron /etc/cron.d/scrapper-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scrapper-cron

# Apply cron job
RUN crontab /etc/cron.d/scrapper-cron

# Create the log file to be able to run tail
CMD ./start-scrapper.sh && cron -f