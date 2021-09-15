# shopify_challenge
This is a Image Repository Application that is created using ReactJS, Flask and SQLite as part of [Shopify Developer Intern Challenge Question](https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit#heading=h.n7bww7g70ipk).

## Instructions to run the Application
Here is my development environment
`npm 6.14.4`, `node 10.19.0`, `Python 3.7.6`

1. Clone the repo
```
git clone git@github.com:mzzchy/shopify_challenge.git
cd shopify_challenge
```
2. The repo is developed on `Python 3.7.6`. I recommend to use Anaconda to create virtual enironemnt with sepcific Python version. Here is the [instruction](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
3. Install backend server
```
pip install ./server
```
4. Setup Database
```
cd sql
python init_db.py
cd ..
```

5. Start the Backend Server
```
cd server
export FLASK_APP=server
export FLASK_ENV=development
flask run
``` 
To verify the backend is setup successfully, please go to `http://localhost:5000/` and make sure you see `Welcome to image repo backend`.
6. In another terminal, start the Front End
```
npm install 
npm start
```
7. Now Go check the image repo on `http://localhost:3000/`

## Structure
The frontend is writted by ReactJS and the backend is writted by Python with Flask. All Images is converted to Blob and stored in Sqlite. 


## The application Current has the following features:
1. Upload one/bulk images
2. Show uploaded images in grid
3. Delete one/bulk images (The frontend of Bulk deletion hasn't been implemented but the API is provided)

## TODO(I will try to finish these feature before the deadline):
1. Set a independent name for uploaded image. (Almost front end)
2. Search by Image Name. (archieved by front end)
3. Setup Authorization system to allow user create accounts and mark image as privated or public
4. Lazy load image.
5. Adding pyTest to backend 


## Further Thought
1. Dockerize the repo
2. Using filesystem like AWS S3 to store the images
3. Extract feature of uploaded image and store in database. For image similarity search, using approximate nearest neighbor algorithm to compute get top K similar image.