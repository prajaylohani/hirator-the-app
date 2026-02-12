import os
import shutil
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


ALLOWED_EXTENSIONS = {'yaml', 'yml', 'tex'}
TEX_TEMPLATE = 'cv-jinja.tex'
SAMPLE_YAML = 'cv-sample.yaml'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
app.config['EXPORT_FOLDER'] = os.path.join(app.instance_path, 'exports')
app.config['MAX_CONTENT_LENGTH'] = 0.1 * 1000 * 1000  # max file size : 0.1mb

app.jinja_options = {
    'block_start_string': '<BLOCK>',
    'block_end_string': '</BLOCK>',
    'variable_start_string': '<VAR>',
    'variable_end_string': '</VAR>',
    'comment_start_string': '<COMM>',
    'comment_end_string': '</COMM>',
    'trim_blocks': True,
    'lstrip_blocks': True,
    'autoescape': False,
}


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def escape_yaml_amp_percent(data):
    if isinstance(data, str):
        return data.replace('&', r'\&').replace('%', r'\%')
    elif isinstance(data, dict):
        return {k: escape_yaml_amp_percent(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_yaml_amp_percent(item) for item in data]
    else:
        return data


# TODO: check temp directory + buffer io + exception handling: refer perplex solution
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            name, ext = os.path.splitext(filename)
            tex_path = os.path.join(app.config['UPLOAD_FOLDER'], name+'.tex')

            if ext in ['.yaml', '.yml']:

                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                escaped_data = escape_yaml_amp_percent(data)

                output = render_template(TEX_TEMPLATE, **escaped_data)

                with open(tex_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                # make tex files available for download from url
                shutil.copy2(tex_path, app.config['EXPORT_FOLDER'])
                # make yaml files available for download from url
                # doesnt make sense bc yaml is the input
                # shutil.copy2(file_path, app.config['EXPORT_FOLDER'])

            subprocess.run(
                ['xelatex',
                 '-interaction=nonstopmode',
                 '-halt-on-error',
                 '-output-directory='+app.config['EXPORT_FOLDER'],
                 tex_path],
                text=True,
                timeout=60,
            )

            return redirect(url_for('download_file', name=name+'.pdf'))

    return render_template('index.html')

    # '''
    # <!doctype html>
    # <title>Upload new file</title>
    # <h1>Upload tex or yaml file</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''


@app.route('/downloads/<name>')
def download_file(name):
    return send_from_directory(app.config['EXPORT_FOLDER'], name)


@app.route('/downloads/sample-yaml')
def download_sample():
    return send_from_directory(app.template_folder, SAMPLE_YAML)


# expose on lan
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
