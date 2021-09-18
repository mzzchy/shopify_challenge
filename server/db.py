import sqlite3

import click
import base64
from flask import current_app, g
from flask.cli import with_appcontext


def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db_connection(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db_connection()

    with current_app.open_resource("image_schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db_connection)
    app.cli.add_command(init_db_command)


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
        conn.rollback()
        close_db_connection()
        raise e

    close_db_connection()
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
        conn.rollback()
        close_db_connection()
        raise e
    close_db_connection()


def fetch_all():
    try:
        images_file = []
        conn = get_db_connection()
        cur = conn.cursor()
        sql_fetch_blob_query = """SELECT * from images"""
        cur.execute(sql_fetch_blob_query)
        record = cur.fetchall()
        for row in record:
            images_file.append({'id':row[0], 'image_name':row[3] ,'image_type':row[4] , 'image_base64':base64.encodebytes(row[5]).decode('ascii')})
        cur.close()
    except Exception as e:
        conn.rollback()
        close_db_connection()
        raise e
    close_db_connection()

    return images_file