# hirator

[Visit Website](https://hirator.prajaylohani.com)

hirator is an open source webapp that lets you create pdf documents, like resume, using simple text from webbrowser.

**Note:** This documentation is still in WIP phase.

## About

- [ ] add more details here

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

### Prerequisites:

- [Git](https://git-scm.com/install)
- [Docker](https://docs.docker.com/engine/install)

Clone the repository and start the docker services using the following commands:
```bash
git clone https://github.com/prajaylohani/hirator-the-app.git
cd hirator-the-app
docker compose up -d --build
```

Visit `http://localhost:5100` on web browser

## Usage

Type your document content in the input text area in YAML format and press `Download PDF` button.
You can learn more about YAML [here](https://www.yaml.info/learn/index.html), you don't really need to.

To get started, you can fill the input with sample data using `Or fill sample data` button.
This will give an idea on how the input text should look like.

All the available options in the YAML input is documented [below](#options).

If you already have a source file, then you can also fill the input field from it using `Fill from source file` button.

Give your document a name. It'll default to `document` if left empty.

You can also select an image (if the document template supports) using `Select image file` button.

#### Options
- [ ] add detailed description for options (with references and defaults): ref hypr docs
- [ ] link the complete list of available fonts (need to find)
- [ ] [list of available colours: section 4.3 (svgnames) and 4.4 (x11names)](https://ftp.rrzn.uni-hannover.de/pub/mirror/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf)
- [ ] add note to use dates in double quotes, else leading zero is removed
- [ ] add note to use unescaped characters (like colon : ) in double quotes, like `"Master Thesis: XYZ"`
- [ ] remove softskills section
- [ ] certifications.name to certifications.title (updated in the table below)

| Name | Description | Type | Default | Options |
| - | - | - | - | - |
| meta | format customization | [ ] | - | - |
| meta.language | document language | string | english | english, ngerman |
| meta.template | document template | string | cv-compact | cv-compact, cv-image, cl-compact |
| meta.hmargin | horizontal margin | length | 0.75cm | [latex margin doc] |
| meta.vmargin | vertical margin | length | 1cm | [latex margin doc] |
| meta.fontstyle | font style | string | TeX Gyre Termes | [font list (?)] |
| meta.fontsize | font size | length | 10pt | [latex fontsize doc] |
| meta.titlesize | font size of title | length | 36pt | [latex fontsize doc] |
| meta.sidebarcolor | sidebar color | string | Silver | [list of colours] |
| meta.columnratio | ratio of left column to textwidth | float(?) | 0.25 | [paracol columnratio] |
| contact | contact information | [ ] | - | - |
| contact.name | name | string | - | - |
| contact.position | position | string | - | - |
| contact.email | email address, creates link | string | - | - |
| contact.linkedin | linkedin account without "https://www.", creates link | string | - | - |
| contact.phone | phone number, creates link | string | - | - |
| contact.address | address | string | - | - |
| contact.dateofbirth | date of birth | string | - | - |
| profile | profile / summary / motivation | [ ] | - | - |
| profile.paragraph | profile in paragraph format | string | - | - |
| profile.list | profile in list format | list | - | - |
| workexperience | work experience | list | - | - |
| workexperience.position | position | string | - | - |
| workexperience.company | company | string | - | - |
| workexperience.location | location | string | - | - |
| workexperience.time | time | time | - | [time type readme] |
| workexperience.description | description | list | - | - |
| education | education | list | - | - |
| education.degree | degree | string | - | - |
| education.institute | institute | string | - | - |
| education.location | location | string | - | - |
| education.time | time | time | - | [time type readme] |
| education.focus | focus | list | - | - |
| education.thesis | thesis | [ ] | - | - |
| education.thesis.title | title | string | - | - |
| education.thesis.institute | institute | string | - | - |
| education.thesis.location | location | string | - | - |
| education.thesis.description | description | list | - | - |
| certifications | certifications | list | - | - |
| certifications.title | title | string | - | - |
| certifications.affiliation | affiliation | string | - | - |
| certifications.platform | platform| string | - | - |
| certifications.time | time | time | - | [time type readme] |
| certifications.content | content | list | - | - |
| skills | skills | list | - | - |
| skills.category | category | string | - | - |
| skills.list | list | list  | - | - |
| softskills | soft skills | list | - | - |
| hobbies | hobbies | list | - | - |
| * time | time | [ ] | - | - |
| * time.from | from when, write inside double quotes | "string" | - | - |
| * time.till | till when, write inside double quotes | "string" | - | - |

##### Standard font collections (to be removed)

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

### Advanced TeX

If you're comfortable in LaTeX, then you can take advantage of compiling the PDF directly from a LaTeX source code.

On the backend, the project is running the latest (at the time of deployment) [TeX Live docker image](https://gitlab.com/islandoftex/images/texlive).

Simply fill the input text area with your LaTeX code and press the `Download PDF` button in the `Advanced TeX` section to compile it.

The `Download source as TeX` button saves your input as a `.tex` file.

Use `YAML to TeX` button to generate LaTeX file from normal YAML input.

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

The project is licensed under [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).

See the [LICENSE](./LICENSE) file for more details.

## Contributing

Thanks for considering to contribute to this project!

There is no standard code of conduct for contributing to this project.

Here's a general workflow you can follow:

1. Fork the repo & clone locally
2. Create a feature branch
3. Make your changes and commit
4. Push to branch
5. Open a pull request

## Contact

Please open an [issue](https://github.com/prajaylohani/hirator-the-app/issues) with relevant label or start a [dicussion](https://github.com/prajaylohani/hirator-the-app/discussions) for project related topics.

For other topics, mail me at [prajaylohani@gmail.com](mailto:prajaylohani@gmail.com).
