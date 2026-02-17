FROM registry.gitlab.com/islandoftex/images/texlive:latest

ENV TZ=Europe/Berlin

WORKDIR /usr/src/app

COPY requirements.txt .
COPY templates/ templates/
COPY static/ static/
COPY fonts/ fonts/
# COPY images/ images/
COPY app.py .

# Install pip
RUN apt-get update && apt-get install -y python3-pip

# Install python dependencies
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
# RUN pip install --no-cache-dir --break-system-packages Flask

# RUN xelatex CV.tex
# RUN xelatex --output-directory="./downloads" --jobname="output-filename" CV.tex # UNVERIFIED

# EXPOSE 8000
EXPOSE 5100

# CMD ["python3", "-m", "http.server", "8000"]
CMD ["python3", "app.py"]
