FROM python:3.10-slim

WORKDIR /app/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SITEMAP_URL=https://egorovegor.ru/post-sitemap.xml
ENV PULSE_WIDGET_ID=partners_widget_egorovegorru
ENV SLEEP_INTERVAL=3600
ENV BOOST_POINT=20
COPY . /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "app.py" ]
