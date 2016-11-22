import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import StringIO
import base64
from graph import run_canvis

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])
UPLOAD_FOLDER = ''
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_file(locus_fname, ld_fname, annotations_fname):
    #img = StringIO.StringIO()
    #file = filename

    
    #data = pd.read_csv(file)
    #data = data.as_matrix()
    #data = data[:,:2]
    #plt.plot(data[:,0], data[:,1])

    # needs to return a plt
    # call run_canvis

    #plt.savefig(img, format='png')
    #img.seek(0)
    #plot_url = base64.b64encode(img.getvalue())
    plot_url = run_canvis(locus_fname, ld_fname, annotations_fname)
    return render_template('contact.html', plot_url=plot_url)
    

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
        file2 = request.files['file2']
        file3 = request.files['file3']

        if file:
            locus_fname = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], locus_fname))
            
            ld_fname = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], ld_fname))

            annotations_fname= secure_filename(file3.filename)
            file3.save(os.path.join(app.config['UPLOAD_FOLDER'], annotations_fname))
            
            return process_file(locus_fname, ld_fname, annotations_fname)
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
       
 
if __name__ == "__main__":
    app.run()