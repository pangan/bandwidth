from flask import request , make_response
from app import app

import datetime
import time
import string
import random

APP_VER = '1.0'

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
			random_extention = random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)
			file_name = "%s%s-%s.%s" %(file_size, unit, timestamp, random_extention)
			response.headers["Content-Disposition"] = "attachment; filename=%s" %(file_name)
			return response
		else:
			ret = """
			Bandwidth Server Ver %s<br>
			<hr>
			Syntax : %sbandwidth?size=<file size in>&unit=[b:byte, k:kilibyte, m:megabyte, g: gigabyte] <br>
			<br>
			Example : <a href='%sbandwidth?size=100&unit=k'>%sbandwidth?size=100&unit=k</a>
			<hr>
			All rights reserved by Birdstep Technology AB.
			""" %(APP_VER, request.base_url, request.base_url , request.base_url)
			return ret
	
