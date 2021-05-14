FROM debian:stable-slim

WORKDIR /app/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SITEMAP_URL=https://egorovegor.ru/post-sitemap.xml
ENV PULSE_WIDGET_ID=partners_widget_egorovegorru
ENV SLEEP_INTERVAL=3600
ENV BOOST_POINT=20
COPY . .
RUN apt-get update && \
    apt-get -y --no-install-recommends install python3-minimal python3-pip python3-setuptools python3-multidict python3-yarl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* && \
    python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "app.py" ]
