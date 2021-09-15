# shopify_challenge
This is a Image Repository Application that is created using ReactJS, Flask and SQLite as part of [Shopify Developer Intern Challenge Question](https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit#heading=h.n7bww7g70ipk).

## Instructions to run the Application
1. Clone the repo
```
git clone git@github.com:mzzchy/shopify_challenge.git
cd shopify_challenge
```
2. The repo is developed on `Python 3.7.6`. I recommend to use Anaconda to create virtual enironemnt with sepcific Python version. Here is the [instruction](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
3. Install backend server
```
pip install /server
```
4. Setup Database
```
cd sql
python init_db.py
```

5. Start the Backend Server
```
cd server
export FLASK_APP=server
export FLASK_ENV=development
flask run
cd ..
``` 
To verify the backend is setup successfully, please go to `http://localhost:5000/` and make sure you see `Welcome to image repo backend`.
6. Start the Front End
```
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
1. Authentication feature for the application
2. Display images based on their visibility (can be either public/private)
3. Image deletion feature (accessible to respective Image owners)

## Further Thought