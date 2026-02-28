FROM registry.gitlab.com/islandoftex/images/texlive:latest

ENV TZ=Europe/Berlin

WORKDIR /usr/src/app

COPY requirements.txt .
COPY templates/ templates/
COPY static/ static/
COPY fonts/ fonts/
COPY app.py .

RUN apt-get update && apt-get install -y python3-pip
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

EXPOSE 5100

# log-level: prod=info dev=debug
CMD ["gunicorn", "--bind", "0.0.0.0:5100", "--workers", "4", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
