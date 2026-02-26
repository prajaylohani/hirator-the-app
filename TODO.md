# UPNEXT:

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
- [x] use yaml templates to create fields in flask: changing yaml template update flask fields: changed direction, not more gui fields
- [x] handle photo
- [x] allow yaml as input to create tex
- [x] various tex templates for different styles
- [x] yaml things:
    - [x] care about handling optional fields: everything is optional
    - [x] care about handling multiples/variable entries
    - [x] care about escaping special symbols like %
    - [x] add meta fields like font, font size, margin, title size, etc.
    - [x] custom fonts are complicated due to adding them in directory
        - [x] some more options with \usepackage: let this be a "tex mode" advanced feature
        - [x] fonts in fonts folder works only in "tex mode"
    - [x] give sample yaml as download link
- [x] update dotfiles with streamlink and mpv conf: no mpvc needed, no mpv conf just reload script might not be needed
- [x] stage i flask design: completeeasily !
- [ ] add meaningful exceptions/error messages:
    - [ ] failed pdf compilation: show latex compilation warnings / logs?
    - [x] missing required values: handled by html
    - [ ] uploading wrong file format
    - [x] everything breaks when file not uploaded (if just photo uploaded for example): upload not a required field
    - [ ] refreshing doesn't reset a broken app: make app start a new instance on refresh, handle running / broken instances
    - [ ] refreshing doesn't the app, it continues from the last buffer: maybe temp dir fixes this? app instance thing again might fix
- [x] auto-upload without pressing upload button and drag-drop feature: no, bc sometimes photo
- [x] contact part of the cv is scuffed bc need hfill and | between entries idk how to do this elegantly wo escaping string join fuckery removed the line (|) for now as temp fix
- [ ] check temp directory
- [x] why is the python syntax highlighting better on mac's nvim than linux's nvim? bc treesitter a bitch! branch: master branch shit
- [x] option to edit yaml/tex files online
- [x] add light/dark mode in html
- [x] separate css
- [x] there's no indication if the file is uploaded/selected
- [ ] restructure the project, refer below
  - [ ] fonts and images to static? update directories in tex, images not static so uploads? tf is images dir?
- [x] flutter?: nah, too much overhead
- [x] webpage scuffed on mobile:
  - [x] title's (in heading) fine, but body is left aligned and bleeding over the left edge
  - [x] issue when screen size smaller than the body content width? body doesnt shrink?
  - [x] add adaptive font size or column width or sth
- [x] setup raspi for hosting: docker, tailscale, etc.
- [x] changes in the textarea doesnt go to server file upload: so sample+edit doesnt work as the app currently only take uploaded file as input: make the generate pdf button submit textarea value as file if not empty?
- [x] add favicon
- [x] download button doesnt take back on mobile bookmark thing, check: not fixed, prolly an ios thing
- [x] load sample button is broken: jinja url replace not working in script (bc its static), does it only replace index.html?
- [x] send text to flask and convert to file in server (if needed)?
  - [x] text input is the primary input approach, not file input
  - [x] yaml is the primary input format, tex is an "advanced" option: "tex mode"
  - [x] file input / sample file is used to fill the text area
  - [x] find how to use xelatex with text, else convert text to file in flask
    - [x] prolly better to create a tex file in server, easy for download later (both yaml and tex)
  - [x] clear that js script!
  - [x] clear up html, id is used for js
  - [x] rename variables / functions 
  - [x] fix download yaml and download tex buttons, they won't work without generate pdf
  - [x] fix text area placeholder
- [x] syntax highlighting in online editor?
  - [x] can be done easily with prism, but the implementation is so ass i'm not doing it!
- [x] spacing between buttons
- [ ] add references / hints
- [x] update margin to hmargin and vmargin, add option for columnratio too,  in yaml and tex jinja
- [x] sth wrong with the margin change logic in tex, check sidebar too
- [x] clean cv-image-jinja before pushing
- [x] create german templates: the current cv-image template is german so far
- [x] add option to select cv template: in yaml? try reading from safe_load output
- [x] can \newpage be injected from yaml?: too complicated, use tex mode
- [x] add profile section with support for both para and bullets
- [x] fix \\\\ and vspace drama:
  - [x] \\\\ outside tabularx = underfull + 3 pages
  - [x] last bigskip might cause extra page: move bigskip to before table
  - [x] resolve the \\\\ in itemize entries: same as above? before itemize?
- [x] bullets only profile has more space between bullets and top line above it: fix vspace{-\baselineskip}
- [x] why are there so many tabularx? tables arent even used now, or are they? remove if possible: nah hes carrying the formatting heavy!
- [x] why does sidebar compiles correctly on second compile: using latexmk to handle multiple compiles automatically
- [ ] what happens if 2 or more people try to use the app?
  - [ ] can the site handle multiple app instances
  - [ ] prolly need to use temp directory to avoid overwriting in the exports and uploads directory
- [x] clear slurs before push
- [x] add urls for log: no redirects
- [x] set max text limit: set at 5000, more than double my current doc with comments
- [x] when templates good enough, make de/en of the other versions:
  - [x] handle locale with the same template? too much?
  - [x] update the jinja filenames again
- [ ] draw excalidraw architecture in md here
- [ ] move soft skills inside skills? as a category?

## the commands:
- docker build: `docker build . -t hirator`
- docker run: `docker run --name hirator --rm -p 5100:5100 hirator:latest`
- docker debug: `docker exec -it hirator /bin/bash`

- [ ] update this, or remove from here?
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
 

## typical docker flask app project structure:
```
myflaskapp/
├── app/
│   ├── __init__.py        # create_app(), register blueprints, config loading
│   ├── routes.py          # or views.py / blueprints package
│   ├── models.py          # DB models (SQLAlchemy, etc.)
│   ├── extensions.py      # db, login_manager, etc. (optional)
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
├── tests/
│   └── test_basic.py
├── Dockerfile
├── docker-compose.yml     # optional but very common
├── requirements.txt       # Python dependencies
├── config.py              # app configuration (Dev/Prod), or a config/ package
├── .env                   # environment variables (not committed)
├── .dockerignore
└── README.md
```
