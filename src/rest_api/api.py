# Let's write your code here!

from flask import Flask
from flask import request
from flask import abort
from flask import render_template
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import math
import pymysql
import json
import os

app = Flask(__name__)

app.config.from_file("flask_config.json", load=json.load)
app.config['BASIC_AUTH_FORCE'] = True

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/openapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)

auth = BasicAuth(app)

@app.route("/")
def home_page():
	return render_template('home_page.html')

def remove_null_fields(obj):
	return {k:v for k, v in obj.items() if v is not None}

@app.route("/languages-infos")
def spoken_languages_info():

	include_details = int(request.args.get('include_details', 0))

	db_conn = pymysql.connect(host="localhost", user="root",
			password=os.getenv("MySQLpwd"), database="languages",
			cursorclass=pymysql.cursors.DictCursor)

	with db_conn.cursor() as cursor:
		cursor.execute("""SELECT s.language,
					s.info_id as id,
					s.`l1 (in million)`,
					s.`l2 (in million)`,
					s.`total_speakers (in million)`
				FROM spoken_language_info s 
		""")
		infos = cursor.fetchall()
	
	infos = [remove_null_fields(i) for i in infos]
	
	if include_details == 1:
		with db_conn.cursor() as cursor:
			cursor.execute("""SELECT s.language,
						s.info_id as id,
						f.family_name as family,
						b.branch_name as branch
					FROM spoken_language_info s 
					JOIN branch b on b.branch_id = s.branch_id
					JOIN family f on f.family_id = s.family_id 
			""")
			infos = cursor.fetchall()
		
		infos = [remove_null_fields(i) for i in infos]
	db_conn.close()
	return {
		'infos': infos,
		'details': f'/languages-infos?include_details={include_details}',
	}

@app.route("/languages-infos/<int:info_id>")
def spoken_language_info(info_id):
	db_conn = pymysql.connect(host="localhost", user="root",
			password=os.getenv("MySQLpwd"), database="languages",
			cursorclass=pymysql.cursors.DictCursor)

	with db_conn.cursor() as cursor:
		cursor.execute("""SELECT s.language,
					s.info_id as id,
					s.`l1 (in million)`,
					s.`l2 (in million)`,
					s.`total_speakers (in million)`,
					f.family_name as family,
					b.branch_name as branch
				FROM spoken_language_info s
				JOIN branch b on b.branch_id = s.branch_id
				JOIN family f on f.family_id = s.family_id 
				WHERE s.info_id=%s
		""", (info_id, ))
		infos = cursor.fetchall()
	
	infos = [remove_null_fields(i) for i in infos]
	db_conn.close()

	return {
		'infos': infos
	}

@app.route("/languages-audios")
def spoken_language_audio():	
	language_code = request.args.get('language_code')
	
	db_conn = pymysql.connect(host="localhost", user="root",
			password=os.getenv("MySQLpwd"), database="languages",
			cursorclass=pymysql.cursors.DictCursor)

	if language_code:
		with db_conn.cursor() as cursor:
			cursor.execute("""SELECT audio_path
					FROM language_audio a
					JOIN language l on l.language_id = a.language_id
					WHERE l.language_name=%s
			""", language_code)
			audios = cursor.fetchall()
	else:
		with db_conn.cursor() as cursor:
			cursor.execute("""SELECT a.audio_path, l.language_name
					FROM language_audio a
					JOIN language l on l.language_id = a.language_id
			""",)
			audios = cursor.fetchall()
		
	db_conn.close()
	return [{'audios': audios, 'language': language_code} if audios else {'language_code available' : 'es, en, de'}]

