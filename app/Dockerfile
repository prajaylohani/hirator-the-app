FROM registry.gitlab.com/islandoftex/images/texlive:latest

ENV TZ=Europe/Berlin

WORKDIR /usr/src/app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends python3-pip \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/
COPY fonts/ fonts/

EXPOSE 5100

# log-level: prod=info dev=debug
CMD ["gunicorn", "--bind", "0.0.0.0:5100", "--workers", "4", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
