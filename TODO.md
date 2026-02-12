# UPNEXT:
- GIT ALL!
- upload niri config

# do this, do that, king in the castle, king in the castle
- [x] docker runs everything in a container at the top level
- [x] flask just creates and hosts the webapp to take inputs
- [x] the jinja template thing for flask
- [x] python (flask) compiles the latex and uploads the pdf as done in rembg
- [x] no db, no local storage, clear all
- [x] NO! or... store inputs to db, then access them from db to populate tex file? for what?
- [x] no login data storage
- [x] give option to download data (tex? db?) then uploading that file acts as sign in to fill in the data for editing, smart?
- [x] how about json? it has nested structure
- [x] yaml better: easy read, easy edit, no trailing commas issue, more flexible, easy escaping
- [x] architecture: `flask -> yaml -> latex -> pdf`
- [ ] use yaml templates to create fields in flask: changing yaml template will update flask fields
- [ ] handle photo
- [x] allow yaml as input to create tex
- [ ] various tex templates for different styles
- [ ] yaml things:
    - [x] care about handling optional fields: everything is optional
    - [x] care about handling multiples/variable entries
    - [x] care about escaping special symbols like %
    - [x] add meta fields like font, font size, margin, title size, etc.
    - [x] custom fonts are complicated due to adding them in directory
        - [ ] some more options with \usepackage
    - [x] give sample yaml as download link
- [x] update dotfiles with streamlink and mpv conf: no mpvc needed, no mpv conf just reload script might not be needed
- [x] stage i flask design: complete!
- [ ] add meaningful exceptions/error messages:
    - [ ] failed pdf compilation
    - [ ] missing required values
    - [ ] uploading wrong file format
    - [ ] everything breaks when file not uploaded (if just photo uploaded for example)
    - [ ] refreshing doesn't reset a broken app
    - [ ] refreshing doesn't the app, it continues from the last buffer: maybe temp dir fixes this?
- [x] no, bc sometimes photo: auto-upload without pressing upload button and drag-drop feature
- [x] contact part of the cv is scuffed bc need hfill and | between entries idk how to do this elegantly wo escaping string join fuckery removed the line (|) for now as temp fix
- [ ] check temp directory
- [ ] why is the python syntax highlighting better on mac's nvim than linux's nvim? is it pylint?
- [ ] option to edit yaml/tex files online
- [ ] add light/dark mode in html
- [ ] separate css
- [ ] there's no indication if the file is uploaded/selected

![Architecture](./architecture.png "Stages' Architecture")

## the commands:
- for bash: `docker run -it --rm --name latex -v "$PWD":/usr/src/app -w /usr/src/app registry.gitlab.com/islandoftex/images/texlive:latest bash`
- for xelatex compile: `docker run -i --rm --name latex -v "$PWD":/usr/src/app -w /usr/src/app registry.gitlab.com/islandoftex/images/texlive:latest xelatex CV.tex`
- for localhost pdf: `docker run --rm -p 8000:8000 hirator:latest`

## container:
- copy: tex templates, fonts, flask app (python codes)
- run: install dependencies from requirements.txt - flask (use pyproject.toml?)
- cmd: flask app

## python:
- run flask app
- take inputs (start with fixed inputs then dynamic?)
- fill tex template with inputs
- run xelatex to compile pdf
- upload pdf to webapp

## db scheme for table types in cv (* optional):

```yaml
meta:
  margin: 0.02\paperwidth
  fontstyle: TeX Gyre Heros
  fontsize: 10pt
  titlesize: 42pt
  sidebarcolor: SkyBlue

contact:
  name: firstname lastname
  email: id@domain.com
  linkedin: https://linkedin.com/id
  phone: +12 3456789
  address: str. 12, 34567 city

work_experience:
  - position: position 1
    company: company 1
    location: city, country 1
    time:
      from: then
      till: now
    description:
      - 100% did 48 % this
      - did & that
      - and that

education:
  - degree: degree 1
    institute: institute 1
    location: country 1
    time:
      from: then
      till: now
    thesis:
      title: thesis title 1
      institute: institute 1
      location: country 1
      description:
        - did this
        - did that

skills:
  - category: category 1
    list:
      - this
      - that
      - and that

certifications:
  - name: certification 1
    affiliation: affiliation 1
    platform: platform 1
    time:
      from: then
      till: now
    content:
      - this
      - that
      - and that

hobbies:
  - this
  - that
  - and that
```

## UNVERIFIED: Standard font collections

### 1. TeX Gyre Collection (Most common, XeLaTeX-ready)
- TeX Gyre Termes      # Times New Roman
- TeX Gyre Heros       # Arial/Helvetica  
- TeX Gyre Pagella     # Palatino
- TeX Gyre Bonum       # Bookman
- TeX Gyre Schola      # Utopia
- TeX Gyre Cursor      # Courier
- TeX Gyre Adventor    # Avant Garde
- TeX Gyre Chorus      # Zapf Chancery

### 2. Latin Modern (Enhanced Computer Modern)
- Latin Modern Roman    # Default LaTeX font, improved
- Latin Modern Mono
- Latin Modern Sans
 
### 3. Computer Modern (LaTeX default, always there)
- Computer Modern Roman
- Computer Modern Sans
- Computer Modern Typewriter

### 4. AMS Fonts (Math + extras)
- Euler Fraktur, Script
- Computer Modern bold variants (cmmib, cmbsy)
 
### 5. STIX Fonts (Scientific publishing)
- STIX Two Text
- STIX Two Math
 
