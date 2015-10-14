import os
from flask import render_template, request , redirect, url_for, make_response
from app import app



import datetime
import time

import string
import random

from flask import Markup
from functools import wraps

UPLOAD_FOLDER = '/opt/configtool/uploads'
CONFIG_FOLDER = '/opt/configtool/config'
BUILDS_FOLDER = '/opt/configtool/app/static/builds'

ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ret_f_kb = ""
ret_f_mb = ""
ret_f_gb = ""

for i in range (0,1024):
	ret_f_kb += random.choice(string.letters)

for i in range (0,1024):
	ret_f_mb += ret_f_kb

for i in range (0,1024):
	ret_f_gb += ret_f_mb


@app.route('/', methods=['GET'])
def download():
	
	if request.method == 'GET':
		file_size = request.args.get('size', '')
		unit = request.args.get('unit', '')
		if file_size and unit in ["b", "k", "m", "g"]:
			
			ret_f = ""
			ret_f_x = ""

			if unit == "k":
				ret_f_x = ret_f_kb
			elif unit == "m":
				ret_f_x = ret_f_mb
			elif unit == "g":
				ret_f_x = ret_f_gb
			
			if unit == "b":
				for i in range (0,int(file_size)):
					ret_f += random.choice(string.letters)
			else:
				for i in range (0,int(file_size)):
					ret_f += ret_f_x


			
			
			response = make_response(ret_f)
			timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d%H%M%S')
			file_name = "%s%s-%s-%s" %(file_size, unit, timestamp, random.choice(string.letters))
			response.headers["Content-Disposition"] = "attachment; filename=%s" %(file_name)
			return response
		else:
			ret = """
			Bandwidth Server Ver 1.0<br>
			<hr>
			Syntax : %sbandwidth?size=<file size in>&unit=[b:byte, k:kilibyte, m:megabyte, g: gigabyte] <br>
			<br>
			Example : <a href='%sbandwidth?size=100&unit=kb'>%sbandwidth?size=100&unit=k</a>
			<hr>
			All rights reserved by Birdstep Technology AB.
			""" %(request.base_url, request.base_url , request.base_url)
			return ret
	

@app.context_processor
def sub_options():
	
	def find_sub_options(items):	

		return Markup(lib.make_ret_html_for_editor(items))

	return dict(find_sub_options=find_sub_options)

@app.route('/ping')
def ping():
	ret = "pong..."
	return ret
	