# UPNEXT
- nginx
  - ssl

# do this, do that, king in the castle, king in the castle
- [x] docker runs everything in a container at the top level
- [x] flask just creates and hosts the webapp to take inputs
- [x] the jinja template thing for flask
- [x] python (flask) compiles the latex and uploads the pdf as done in rembg
- [x] no db, no local storage, clear all
- [x] store inputs to db, then access them from db to populate tex file? for what?: no
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
- [x] add meaningful exceptions/error messages:
    - [x] failed pdf compilation: show latex compilation warnings / logs?: log available from url /log
    - [x] missing required values: handled by html
    - [x] uploading wrong file format: handled by js
    - [x] everything breaks when file not uploaded (if just photo uploaded for example): upload not a required field
    - [x] refreshing doesn't reset a broken app: make app start a new instance on refresh, handle running / broken instances: fixed with latexmk -gg
    - [x] refreshing doesn't the app, it continues from the last buffer: maybe temp dir fixes this? app instance thing again might fix: fixed with latexmk -gg
- [x] auto-upload without pressing upload button and drag-drop feature: no, bc sometimes photo
- [x] contact part of the cv is scuffed bc need hfill and | between entries idk how to do this elegantly wo escaping string join fuckery removed the line (|) for now as temp fix
- [x] check temp directory
- [x] why is the python syntax highlighting better on mac's nvim than linux's nvim? bc treesitter a bitch! branch: master branch shit
- [x] option to edit yaml/tex files online
- [x] add light/dark mode in html
- [x] separate css
- [x] there's no indication if the file is uploaded/selected
- [x] restructure the project, refer below
  - [x] fonts and images to static? update directories in tex, images not static so uploads? tf is images dir?: removed image
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
  - [ ] [list of available colours: section 4.3 (svgnames) and 4.4 (x11names)](https://ftp.rrzn.uni-hannover.de/pub/mirror/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf)
  - [ ] add readme: move things from here
  - [ ] draw excalidraw architecture in md here: mermaid
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
- [x] what happens if 2 or more people try to use the app?
  - [x] can the site handle multiple app instances: multithreads for dev, wsgi for prod
  - [x] avoid file sharing, delete after exec: use tempfile
  - [x] prolly need to use temp directory to avoid overwriting in the exports and uploads directory
  - [x] check threads in app.run() for dev: security and performance issues on high traffic, so not for prod
  - [x] check wsgi for prod: gunicorn (clanker's fav), uwsgi, waitress?: gunicorn better overall, uwsgi is in maintenance mode, for high peformance, waitress for windows (eww)
  - [x] app.run() vs flask run: use flask run its modern, app.run() is hardcoded in code for dev: use neither for prod, go for wsgi!
  - [x] check uuid? maybe useful for keeps data, not needed
  - [x] check sessions: nah fuck cookies! its useful for keeping user logged in for a session, also fuck logins!
  - [x] check celery / redis: useful as a task queue management for long / slow operation, so maybe not here
  - [x] fastAPI for async?: no, its good for high performance api specific usecases, not for html rendering: experiment later
  - [x] nginx: for safe internet expose: reverse proxy + ssl + handle slow clients and static files
  - [x] remove debug / dev mode things before public:
    - [x] remove from flask command
    - [x] remove from docker run
  - [x] user -> nginx -> gunicorn -> flask
  - [x] update commands below then
  - [x] update requirements for imports
- [x] clear slurs before push
- [x] add urls for log: added then remove due to request bound tempfile: add a line to copy log before deletion
- [x] set max text limit: set at 50000, more than double my current doc with comments
- [x] when templates good enough, make de/en of the other versions:
  - [x] handle locale with the same template? too much?
  - [x] update the jinja filenames again
- [x] move soft skills inside skills? as a category?: nah leave it, this adds the possibility to keep it in the next page, its anyway possible to do so in skills category
- [x] use flash to show warnings/messages: no, needs secret_key and session and cookies: useful for cryptographic security for logins, sessions, etc.
- [x] add x11names in xcolor
- [x] ux improvements:
  - [x] make error message larger
  - [x] create a filled lorem sample?: too confusing as it needs injecting commands from yaml, prob just a dummy filled yaml
  - [x] change placeholder text to sample?: nah, too crowded
  - [x] change download yaml to download source? care the ext, currently saves tex also as .yaml: avoiding context awareness
  - [x] download tex online works with yaml input, change to compile tex? but there's already compile tex
  - [x] download pdf only works with yaml. what a mess!: fixed!
  - [x] name like yaml2pdf, yaml2tex, tex2pdf? and separate tex options?: no, not user friendly names
  - [x] add download source as tex and download source as yaml? or content aware with a single download source button?: no context aware, added complexity
- [x] optimize dockerfile for better layer caching
- [ ] check if lighter alternative for texlive (>2gb):
  - [ ] texlive base/minimal image? might need to install some packages manually
  - [x] kjarosh?: texlive is better maintained
  - [x] whats sharelatex, backend of overleaf?: yes, so its a full setup with db and editer, so no bc overkill

## the commands:
- docker build: `docker build . -t hirator`
- docker run: `docker run --name hirator --rm -p 5100:5100 hirator:latest`
- docker debug: `docker exec -it hirator /bin/bash`
- docker compose: `docker compose up --build`

- [ ] update this, or remove from here? can i link the cv-sample content here?
## sample input (* optional):
full file at [cv-sample.yaml](./app/templates/cv-sample.yaml)

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
