import sqlite3
import base64
import json

from flask import Flask, abort, request, Response, send_file
from flask.helpers import make_response
from werkzeug.datastructures import FileStorage
from flask_cors import CORS, cross_origin
from PIL import Image

app = Flask(__name__)
CORS(app)


def get_db_connection():
    conn = sqlite3.connect('../sql/image.db')
    conn.row_factory = sqlite3.Row
    return conn


def bulk_insert(imageList):
    ids = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_insert_image_query = '''INSERT INTO images(userid, image_type, image_name, image_blob) VALUES(?, ?, ?,?)'''
        for image in imageList:
            cur.execute(sql_insert_image_query, (1, image.content_type , image.filename, image.read(),))
            ids.append(cur.lastrowid)
        conn.commit()
    except Exception as e:
        if conn:
            conn.close()
        raise e
    if conn:
        conn.close()

    return ids


def bulk_delete(image_ids):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_delete_image_query = '''DELETE FROM images WHERE id=?'''
        for id in image_ids:
            cur.execute(sql_delete_image_query, (id, )) 
        conn.commit()
    except Exception as e:
        if conn:
            conn.close()
        raise e
    if conn:
        conn.close()


def fetch_all():
    images_file = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_fetch_blob_query = """SELECT * from images"""
        cur.execute(sql_fetch_blob_query)
        record = cur.fetchall()
        for row in record:
            images_file.append({'id':row[0], 'image_name':row[3] ,'image_type':row[4] , 'image_base64':base64.encodebytes(row[5]).decode('ascii')})
        cur.close()
    except sqlite3.Error as e:
        if conn:
            conn.close()
        raise e

    if conn:
        conn.close()

    return images_file


@app.route('/')
def hello():
    return 'Welcome to image repo backend'


@app.route('/fetch')
def fecth():
    try:
        files = fetch_all()
        return Response(
            response=json.dumps({'images': files}),
            status=200,
            mimetype='application/json'
        )
    except Exception as exc:
        return Response(
            status=500,
            content_type='application/json'
        )

@app.route('/upload', methods=(['POST']))
def upload():
    images = request.files.getlist('images')
    try:
        ids = bulk_insert(images)

        return Response(
            response=json.dumps({'image_ids': ids}),
            status=200,
            content_type='application/json'
        )
    except Exception as exc:
        return Response(
            status=500,
            content_type='application/json'
        )

@app.route('/delete', methods=(['POST']))
def delete():
    ids = request.json['ids']
    try:
        bulk_delete(ids)
        return Response(
            status=200,
            content_type='application/json'
        )
    except Exception as exc:
        return Response(
            status=500,
            content_type='application/json'
        )