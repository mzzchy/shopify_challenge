import os
import json

from flask import Flask, request, Response
from flask_cors import CORS

from server.db import init_app, bulk_insert, bulk_delete, fetch_all

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "server.sqlite"),
    )

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def health():
        return Response(
                response=json.dumps({'message': "welcome to image repo backend"}),
                status=200,
                content_type='application/json'
            )

        
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

    # Init the Database
    init_app(app)

    return app