import os
import subprocess
import yaml
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    send_file,
    send_from_directory,
)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
DEFAULT_TEX_TEMPLATE = "cv-compact-en"
SAMPLE_YAML = "cv-sample.yaml"
DEFAULT_FILENAME = "document"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.instance_path, "uploads")
app.config["EXPORT_FOLDER"] = os.path.join(app.instance_path, "exports")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000  # 5mb
app.config["FILENAME"] = DEFAULT_FILENAME

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


os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["EXPORT_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def escape_yaml_amp_percent(data):
    if isinstance(data, str):
        return data.replace("&", r"\&").replace("%", r"\%")
    elif isinstance(data, dict):
        return {k: escape_yaml_amp_percent(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_yaml_amp_percent(item) for item in data]
    else:
        return data


def tex2pdf(tex_path):
    subprocess.run(
        [
            "latexmk",
            "-gg",
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-outdir=" + app.config["EXPORT_FOLDER"],
            tex_path,
        ],
        text=True,
        timeout=60,
    )


# TODO: check temp directory + buffer io + exception handling: refer perplexity solution
@app.route("/", methods=["GET", "POST"])
def upload_text():
    if request.method == "POST":
        # get image
        image = request.files.get("image")

        if image and image.filename != "":
            if not allowed_file(image.filename):
                return "Invalid file type. Please upload a valid image."

            imagename = secure_filename(image.filename)
            image_path = os.path.join(app.config["EXPORT_FOLDER"], imagename)
            image.save(image_path)
        else:
            imagename = None

        action = request.form.get("action")

        # get filename
        filename = request.form.get("filename", DEFAULT_FILENAME).strip()
        if not filename:
            filename = DEFAULT_FILENAME
        app.config["FILENAME"] = filename

        # set filepath
        yaml_path = os.path.join(app.config["EXPORT_FOLDER"], filename + ".yaml")
        tex_path = os.path.join(app.config["EXPORT_FOLDER"], filename + ".tex")

        # read raw data
        raw_data = request.form.get("preview", "")

        if action == "compile_tex":
            # save tex
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(raw_data)

            tex2pdf(tex_path)
            return redirect(url_for("download_pdf"))

        # save yaml
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(raw_data)

        ## download_yaml
        if action == "download_yaml":
            return redirect(url_for("download_yaml"))

        # yaml to tex
        data = yaml.safe_load(raw_data)

        # set imagename if available
        if imagename:
            data["meta"]["imagename"] = imagename

        # get template if available
        if "meta" in data and "template" in data["meta"]:
            tex_template = data["meta"]["template"] + ".tex"
        else:
            tex_template = DEFAULT_TEX_TEMPLATE + ".tex"

        escaped_data = escape_yaml_amp_percent(data)
        output = render_template(tex_template, **escaped_data)

        # save tex
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(output)

        if action == "download_tex":
            return redirect(url_for("download_tex"))

        tex2pdf(tex_path)

        if action == "download_pdf":
            return redirect(url_for("download_pdf"))

    return render_template("index.html")


@app.route("/downloads/sample")
def download_sample():
    return send_from_directory(app.template_folder, SAMPLE_YAML)


@app.route("/downloads/yaml")
def download_yaml():
    return send_from_directory(
        app.config["EXPORT_FOLDER"],
        app.config["FILENAME"] + ".yaml",
        mimetype="text/plain",
        as_attachment=False,
    )


@app.route("/downloads/tex")
def download_tex():
    return send_from_directory(
        app.config["EXPORT_FOLDER"],
        app.config["FILENAME"] + ".tex",
        as_attachment=False,
    )


@app.route("/downloads/pdf")
def download_pdf():
    return send_from_directory(
        app.config["EXPORT_FOLDER"],
        app.config["FILENAME"] + ".pdf",
        as_attachment=False,
    )


@app.route("/downloads/log")
def download_log():
    return send_from_directory(
        app.config["EXPORT_FOLDER"],
        app.config["FILENAME"] + ".log",
        mimetype="text/plain",
        as_attachment=False,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
