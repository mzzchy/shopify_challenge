import io
import json
from flask.wrappers import Response



def test_health(app):
    with app.test_client() as c:
        response = c.get('/')
        response_json = response.get_json()  

        assert response_json["message"] == "welcome to image repo backend"


def test_insert_fetch_delete(app):
    with open("./locals/image1.jpg", "rb") as imageFile:
        image1 = io.BytesIO(imageFile.read())
    with open("./locals/image1.jpg", "rb") as imageFile:
        image2 = io.BytesIO(imageFile.read())
    with open("./locals/image1.jpg", "rb") as imageFile:
        image3 = io.BytesIO(imageFile.read())
    
    with app.test_client() as c:
        response = c.post(
            '/upload', 
            data={'images': [(image1, 'image1.jpg'), (image2, 'image2.jpg'), (image3, 'image3.jpg')]}, 
            content_type='multipart/form-data',
            )
        response_json = response.get_json()
        ## Test Upload
        assert response_json['image_ids'] == [1,2,3]

        response = c.get( '/fetch')
        response_json = response.get_json()
        ## Test fetch. Todo: Check fetched image instead just checking count
        assert len(response_json['images']) == 3

        response = c.post( 
            '/delete', 
            data=json.dumps({'ids': [1,2]}),
            content_type='application/json',
            follow_redirects=True
            )
            
        response = c.get( '/fetch')
        response_json = response.get_json()
        ## Test detele. Todo: Check fetched image instead just checking count
        assert len(response_json['images']) == 1




   
