import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file
from werkzeug.utils import secure_filename
from redis import Redis
import rq
import math
import time

UPLOAD_FOLDER = 'uploaded'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '5UC3M35C0U17735'

def split_this_song(song_path):
	os.system("spleeter separate -i " + UPLOAD_FOLDER + '/' + song_path + " -p spleeter:2stems -o output")

def redirect_done(job_id):
	return redirect(url_for('dir_listing', req_path='output'))

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

@app.route('/<path:req_path>')
def dir_listing(req_path):
	BASE_DIR = '.'
	abs_path = os.path.join(BASE_DIR, req_path)
	if os.path.isfile(abs_path):
		return send_file(abs_path)
	passed_info = []
	files = os.listdir(abs_path)
	for f in files:
		info = {}
		info['name'] = f[:-4]
		info['ext'] = f[-4:]
		info['size'] = convert_size(os.stat(abs_path + '/' + f).st_size)
		info['action'] = abs_path + '/' + f
		info['action'] = info['action'][9:]
		passed_info.append(info)
	print(passed_info)
	return render_template('result.html', files=passed_info)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			queue = rq.Queue('split', connection=Redis.from_url('redis://'))
			split_job = queue.enqueue(split_this_song, filename)
			os.mkdir('./output/'+filename[:-4])
			return redirect(url_for('dir_listing', req_path='output/'+filename[:-4]))
	return render_template('index.html')