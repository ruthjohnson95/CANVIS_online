import os
from flask import Flask, request, flash, redirect, url_for, render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
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
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    post = TextField('Name:', validators=[validators.required()])
    LD = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    annot = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_file(locus_fname, ld_fname, annotations_fname):
    plot_url = run_canvis(locus_fname, ld_fname, annotations_fname)
    return render_template('contact.html', plot_url=plot_url)
    
#@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        post=request.form['post']
        LD=request.form['LD']
        annot=request.form['annot']
        print post, " ", LD, " ", annot
 
        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + post)
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('plot.html', form=form)


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

        file = request.files['post']
        file2 = request.files['LD']
        file3 = request.files['annot']

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