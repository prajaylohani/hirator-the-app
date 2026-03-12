# [WIP] todo of the readme (meta):
refer well documented projects like:
- [hypr](https://wiki.hypr.land/Configuring/Variables)
- [niri](https://github.com/niri-wm/niri)
- [rofi](https://github.com/davatorium/rofi)

# Hirator

## Table of Contents

- [About](#about)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#Architecture)
- [Debugging](#debugging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

Hirator is an open source webapp that lets you create pdf documents, like resume, using simple text from webbrowser.

- [ ] add more details here

## Features

- Generate well formatted pdf document from a simple human readable yaml file
- Multiple customization options from yaml, such as template, language, font, colour, etc.
- Supports image
- Dynamic content sections with various formats, such as bullets, paragraph, time, bold, italics, etc.
- Highly flexible, almost every field is optional - the document adapts for missing values and use defaults when needed
- Unlock full potential of LaTeX by using the Advanced TeX mode

## Screenshots

- [ ] add generic template images

![Screenshot](docs/screenshot.png)

## Installation

Before following the installation steps, make sure you have the following prerequisites installed.

### Prerequisite:

- [Git](https://git-scm.com/install)
- [Docker](https://docs.docker.com/engine/install)

Clone the repository and start the docker services:
```bash
git clone https://github.com/prajaylohani/hirator-the-app.git
cd hirator-the-app
docker compose up -d --build
```

Visit `http://localhost:5100` on web browser

## Usage

There are 2 ways to use the webapp:
1. [Normal way](#normal-way)
2. [Advanced TeX way](#advanced-tex-way) **(use only if you know LaTeX)**

**Note:** No data is stored! So make sure to download your source if you'd like to use it again later.

### Normal way

Type your document content in the input text area in YAML format and press `Download PDF` button.
You can learn more about YAML [here](https://www.yaml.info/learn/index.html), you don't really need to.
To get started, you can fill the input with sample data using `Or fill sample data` button. This will give an idea on how the input text should look like.
All the available options in the YAML input is documented [below](#options).
If you already have a source file, then you can also fill the input field from it using `Fill from source file` button.
Give your document a name. It'll default to `document` if left empty.
You can also select an image (if the document template supports) using `Select image file` button.

**To be changed:**
The current sample displays **ALL** the available options.
Use it to see all the options, but I wouldn't recommend using it as it is in the input.
It'll be updated with a more relevant sample and all the options will be documented in [options section](#options) below.

#### Options
- [ ] add detailed description for options (with references and defaults): ref hypr docs
- [ ] link the complete list of available fonts (need to find)
- [ ] [list of available colours: section 4.3 (svgnames) and 4.4 (x11names)](https://ftp.rrzn.uni-hannover.de/pub/mirror/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf)

```yaml
meta:
  language: ngerman
  template: cv-image
  hmargin: 0.02\paperwidth
  vmargin: 2.5\hmargin
  fontstyle: TeX Gyre Heros
  customfont: Figtree
  fontsize: 10pt
  titlesize: 42pt
  sidebarcolor: SkyBlue
  columnratio: 0.22

contact:
  name: firstname lastname
  position: position
  email: id@domain.com
  linkedin: linkedin.com/in/username
  phone: +12 3456789
  address: str. 12, 34567 city
  dateofbirth: 31.12.1984

profile:
  paragraph: paragraph
  list:
    - this
    - that
    - and that

workexperience:
  - position: position
    company: company
    location: city, country
    time:
      from: "then"
      till: "now"
    description:
      - did this
      - did that
      - and that

education:
  - degree: degree
    institute: institute
    location: country
    time:
      from: "01.1234"
      till: "02.1234"
    focus:
      - this
      - that
      - and that
    thesis:
      title: "thesis: title"
      institute: institute
      location: country
      description:
        - did this
        - did that

certifications:
  - name: certification
    affiliation: affiliation
    platform: platform
    time:
      from: "then"
      till: "now"
    content:
      - this
      - that
      - and that

skills:
  - category: category
    list:
      - this
      - that
      - and that

softskills:
  - this
  - that
  - and that

hobbies:
  - this
  - that
  - and that
```

##### UNVERIFIED: Standard font collections

1. TeX Gyre Collection (Most common, XeLaTeX-ready)
- TeX Gyre Termes      # Times New Roman
- TeX Gyre Heros       # Arial/Helvetica
- TeX Gyre Pagella     # Palatino
- TeX Gyre Bonum       # Bookman
- TeX Gyre Schola      # Utopia
- TeX Gyre Cursor      # Courier
- TeX Gyre Adventor    # Avant Garde
- TeX Gyre Chorus      # Zapf Chancery

2. Latin Modern (Enhanced Computer Modern)
- Latin Modern Roman    # Default LaTeX font, improved
- Latin Modern Mono
- Latin Modern Sans
 
3. Computer Modern (LaTeX default, always there)
- Computer Modern Roman
- Computer Modern Sans
- Computer Modern Typewriter

4. AMS Fonts (Math + extras)
- Euler Fraktur, Script
- Computer Modern bold variants (cmmib, cmbsy)
 
5. STIX Fonts (Scientific publishing)
- STIX Two Text
- STIX Two Math

### Advanced TeX way

If you're comfortable in LaTeX, then you can take advantage of compiling the PDF directly from a LaTeX source code.
On the backend, the project is running the latest (at the time of deployment) [TeX Live docker image](https://gitlab.com/islandoftex/images/texlive).
Simply fill the input text area with your LaTeX code and press the `Download PDF` button in the `Advanced TeX` section to compile it.
The `Download source as TeX` button saves your input as a `.tex` file.
There's also an option to generate LaTeX file from normal YAML input using the `YAML to TeX` button.

**Note:** Debugging the code is not possible online. If your code compilation fails, then the app throws a generic `Not Found` error message without any log.

## Architecture

- [ ] draw excalidraw architecture in md: mermaid
- [ ] explain the tech stack in detail: latex (texlive), jinja, flask, nginx, docker, python, html, css, js, yaml, gunicorn, raspi, cloudflared
- [ ] refer hint for jinja latex config: [thomas niebler](www.thomas-niebler.de/2022/02/02/jinja-in-latex/)

## Debugging

Data is not saved in the host machine or in the containers.
So, besides the traditional methods like docker logs, when running locally I'd suggest:
- changing the source code to save data temporarily, and/or
- running a shell inside the container using the following commands:
``` bash
# for flask app
docker exec -it app /bin/bash

# for nginx proxy
docker exec -it proxy /bin/ash
```

## License

- [ ] update after adding license

## Contributing

Thanks for considering to contribute to this project!
I haven't thought of any standard code of conduct for contribution yet.

Here's a simple workflow you can follow:
1. Fork the repo & clone locally
2. Create a feature branch
3. Make your changes and commit
4. Push to branch
5. Open a pull request

## Contact

Please open an [issue](https://github.com/prajaylohani/hirator-the-app/issues) with relevant label or start a [dicussion](https://github.com/prajaylohani/hirator-the-app/discussions) for project related topics.
For other topics, mail me at [prajaylohani@gmail.com](mailto:prajaylohani@gmail.com).
