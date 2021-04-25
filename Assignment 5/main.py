import os
from flask import Flask, render_template, url_for, request, session, redirect, flash
from pymongo import MongoClient
from flask import send_from_directory
from werkzeug.utils import secure_filename

omar = MongoClient('localhost', 27017)  #mango port 
db = omar.users # database name 

app = Flask(__name__)


app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static/upload/')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set([ 'jpg', 'jpeg', 'gif','txt', 'pdf', 'png']) # file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    users = db.users.find({})
    return render_template("index.html")    #index , login page


@app.route('/', methods=['POST'])
def lndex2():
    users = db.users.find({})
    password = request.form['pass']
    login_user = db.users.find_one({'name' : request.form['username']})

    if login_user and password:
        if request.form['pass']  == login_user['password']:
            return render_template('data.html')
    else:
          return render_template('index.html')

@app.route('/cabinet')
def upload_form():
    return render_template('data.html')  # data.html is page where we upload data

@app.route('/cabinet', methods=['POST'])        #upload section
def login():
    if 'file' not in request.files:
        flash('Please input data by clicking on the choose file!')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(' Yahoo! Image is uploaded and displayed successfully')
        return render_template('data.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/register', methods=['POST', 'GET']) # registration section
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = db.users.find_one({'name' : request.form['username']})

        if existing_user is None:
            db.users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')  # register.html is the page where user register

@app.route('/upload/<filename>')
def display_image(filename):
    return send_from_directory('static/upload', filename)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

