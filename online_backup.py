import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import base64

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = ''
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_file(filename):
    img = StringIO.StringIO()
    file = filename
    data = pd.read_csv(file)
    data = data.as_matrix()
    data = data[:,:2]
    plt.plot(data[:,0], data[:,1])
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    return render_template('contat.html', plot_url=plot_url)
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return process_file(filename)
            #return redirect(url_for('uploaded_file',
            #                       filename=filename))
    return render_template('plot.html')

# redirect to other pages
@app.route('/plot')
def plot():
    # show the form, it wasn't submitted
    return render_template('plot.html')

@app.route('/home')
def home():
    # show the form, it wasn't submitted
    return render_template('index.html')

@app.route('/docs')
def docs():
    # show the form, it wasn't submitted
    return render_template('docs.html')

@app.route('/contact')
def contact():
    # show the form, it wasn't submitted
    return render_template('contact.html')            

    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p>
      <input type=file name=file>
      <input type=file name=file2>
      <input type=file name=file3>

        <input type=submit value=Upload>
    </form>
    '''
 
if __name__ == "__main__":
    app.run()