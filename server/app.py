import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file
from werkzeug.utils import secure_filename
from redis import Redis
import rq

UPLOAD_FOLDER = 'uploaded'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '5UC3M35C0U17735'

def split_this_song(song_path):
	os.system("spleeter separate -i " + UPLOAD_FOLDER + '/' + song_path + " -p spleeter:2stems -o output")

def redirect_done(job_id):
	# job = Job.fetch(job_id)
	# while job.is_finished == False:
	# print(job.get_status())
	return redirect(url_for('dir_listing', req_path='output'))

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<path:req_path>')
def dir_listing(req_path):
	BASE_DIR = '.'
	abs_path = os.path.join(BASE_DIR, req_path)
	if os.path.isfile(abs_path):
		return send_file(abs_path)
	files = os.listdir(abs_path)
	return render_template('index.html', files=files)

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
			return redirect(url_for('dir_listing', req_path='output'))
			# return redirect(url_for('uploaded_file', filename=filename))
	return render_template('index.html')