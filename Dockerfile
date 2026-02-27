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

CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5100"]
