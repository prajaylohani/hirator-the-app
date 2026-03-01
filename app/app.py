import os
import subprocess
import yaml
import tempfile
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
)

ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png"}
DEFAULT_TEX_TEMPLATE = "cv-compact"
SAMPLE_YAML = "cv-sample.yaml"
DEFAULT_FILENAME = "document"


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000  # 5mb
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


app.jinja_options = {
    "block_start_string": "<BLOCK>",
    "block_end_string": "</BLOCK>",
    "variable_start_string": "<VAR>",
    "variable_end_string": "</VAR>",
    "comment_start_string": "<COMM>",
    "comment_end_string": "</COMM>",
    "trim_blocks": True,
    "lstrip_blocks": True,
    "autoescape": False,
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_TYPES


def escape_yaml_amp_percent(data):
    if isinstance(data, str):
        return data.replace("&", r"\&").replace("%", r"\%")
    elif isinstance(data, dict):
        return {k: escape_yaml_amp_percent(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_yaml_amp_percent(item) for item in data]
    else:
        return data


def tex2pdf(dir, texpath):
    subprocess.run(
        [
            "latexmk",
            "-gg",
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-outdir=" + dir,
            texpath,
        ],
        text=True,
        timeout=60,
    )


def download_yaml(dir, filename):
    return send_from_directory(
        dir,
        filename + ".yaml",
        mimetype="text/plain",
        as_attachment=False,
    )


def download_tex(dir, filename):
    return send_from_directory(
        dir,
        filename + ".tex",
        mimetype="text/plain",
        as_attachment=False,
    )


def download_pdf(dir, filename):
    return send_from_directory(
        dir,
        filename + ".pdf",
        as_attachment=False,
    )


@app.route("/", methods=["GET", "POST"])
def upload_text():
    if request.method == "POST":
        with tempfile.TemporaryDirectory() as tmpdir:
            # get image
            image = request.files.get("image")

            if image and image.filename != "":
                if not allowed_file(image.filename):
                    return f"""
                        <h1> Invalid file type </h1>
                        <p> Please upload a valid image. <br>
                         Accepted image types: {", ".join(ALLOWED_IMAGE_TYPES)} </p>
                    """

                imagename = secure_filename(image.filename)
                imagepath = os.path.join(tmpdir, imagename)
                image.save(imagepath)
            else:
                imagename = None

            action = request.form.get("action")

            # get filename
            filename = request.form.get("filename", DEFAULT_FILENAME).strip()
            if not filename:
                filename = DEFAULT_FILENAME

            # set filepath
            yamlpath = os.path.join(tmpdir, filename + ".yaml")
            texpath = os.path.join(tmpdir, filename + ".tex")

            # read raw data
            rawdata = request.form.get("preview", "")

            # download tex
            if action == "download_tex":
                # save tex
                with open(texpath, "w", encoding="utf-8") as f:
                    f.write(rawdata)

                return download_tex(tmpdir, filename)

            # compile tex
            if action == "compile_tex":
                # save tex
                with open(texpath, "w", encoding="utf-8") as f:
                    f.write(rawdata)

                tex2pdf(tmpdir, texpath)

                return download_pdf(tmpdir, filename)

            # save yaml
            with open(yamlpath, "w", encoding="utf-8") as f:
                f.write(rawdata)

            # download yaml
            if action == "download_yaml":
                return download_yaml(tmpdir, filename)

            # yaml to tex
            data = yaml.safe_load(rawdata)

            # set imagename if available
            if imagename:
                data["meta"]["imagename"] = imagename

            # get template if available
            if "meta" in data and "template" in data["meta"]:
                tex_template = data["meta"]["template"] + ".tex"
            else:
                tex_template = DEFAULT_TEX_TEMPLATE + ".tex"

            escapeddata = escape_yaml_amp_percent(data)
            output = render_template(tex_template, **escapeddata)

            # save tex
            with open(texpath, "w", encoding="utf-8") as f:
                f.write(output)

            # yaml2tex
            if action == "yaml2tex":
                return download_tex(tmpdir, filename)

            tex2pdf(tmpdir, texpath)

            # download pdf
            if action == "download_pdf":
                return download_pdf(tmpdir, filename)

    return render_template("index.html")


@app.route("/downloads/sample")
def download_sample():
    return send_from_directory(app.template_folder, SAMPLE_YAML)
