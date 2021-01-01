# Fullstack RecSys Project
This repository is a toy project integrating machine learning with database, front-end and back-end. 
We aim to build a small web service to provide top-K movie recommendation from user profile. 
To do this, we implement back-end and database server with Flask, front-end with React and recommedation API with PyTorch and Numpy.

# Setups
## **Stacks**
<img src="img/flask.png" width="130">
<img src="img/react.png" width="130">
<img src="img/semantic_ui.png" width="80">
<img src="img/pytorch.svg" width="150">
<img src="img/numpy.svg" width="150">

## **Requirements**
This project requires packages such as Flask, PyTorch and numpy. Please check detailed list in `requirements.txt`. 
On your own environment, install required packages by `pip install -r requirements.txt`


## Back-end
First, we build a minimal back-end server with [Flask](https://flask.palletsprojects.com/en/1.1.x/). 
Back-end server 1) initializes database so that API server can load data and train recommender models, 2) handles requests from front-end by communicating with API server and database.

Here, we initialize database with ML-100k, which is small but popular dataset with 100k from 1,000 users and 1,700 items. 
We provide pre-built database (`app.db`), however, if you want to build your own database, please follow the code below.

1. Initialize DB model by following scripts.

```bash
flask db init && 
flask db migrate &&
flask db upgrade
```
2. Initialize ML-100k into database.
```bash
cd backend && python initialize_ml100k_db.py
```

## Front-end
Front-end is built with [react](https://reactjs.org/) and [semantic-ui-react](https://react.semantic-ui.com/). 
You need npm to build and run react. 

To build front-end, run `npm install`.

## Recommendation API server
In this project, we aim to build recommender taht can provide recommendation to new users with their profile (Unseen in training but not cold-start). 
API server 1) trains a recommender model offline with database and save, 2) responds to the recommendation request from back-end server.

For now, we provide simple non-neural similarity and nearest neighbor models, EASE and ItemKNN.
* **EASE**: Harald Steck, Embarrassingly Shallow Autoencoders for Sparse Data. *WWW* 2019. [Link](https://arxiv.org/pdf/1905.03375)
* **ItemKNN**: Jun Wang et al., Unifying user-based and item-based collaborative filtering approaches by similarity fusion. *SIGIR* 2006. [Link](http://web4.cs.ucl.ac.uk/staff/jun.wang/papers/2006-sigir06-unifycf.pdf)

To train and save recommender offline, run
```
cd ./api && 
python fit_offline.py --model MODEL_NAME --save_dir PATH_TO_SAVE_MODEL
```
* model: name of a model to train (currently, EASE & ItemKNN are available.)
* save_dir: path to save model checkpoint

# Run
To make the all components work together, we have to run **API**, **back-end**, **front-end** servers. 

## API Server
To run API server, 
```bash
cd ./api && python api.py
```
By default, API server is run on `0.0.0.0:8000`.

## Back-end
To run back-end server,
```bash
cd ./backend && flask run
```
By default, back-end server is run on `127.0.0.1:5000`.

## Front-end
To run front-end,
```bash
cd ./react-front && npm start
```
You can specify host and port in `react-front/.env`. By default, front-end server is run on `127.0.0.1:5052`.

## Bind back-end & front-end
You can run front-end and back-end script together using `concurrently`, which helps you run scripts parallel.

You can install `concurrently` by `npm install -g concurrently`. 
In `react-front/package.json`, add binding script (e.g. `"start-all": "concurrently \"react-scripts start\" \"cd ../backend && flask run\""`).

Now, `npm start-all` runs both back-end and front-end.

# TODO
- [ ] Show movie metadata on click.
- [ ] Add SOTA neural and non-neural recommenders.
- [ ] Fancier front-end (Header, Footer, etc.)


# Reference
1. [How To Create a React + Flask Project](https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project)
2. [Image Recommendations with PyTorch + Flask + PostgreSQL + Heroku deployment](https://towardsdatascience.com/image-recommendations-with-pytorch-flask-postgresql-heroku-deployment-206682d06c6b)
3. [Build a fully production ready machine learning app with Python Django, React, and Docker](https://towardsdatascience.com/build-a-fully-production-ready-machine-learning-app-with-python-django-react-and-docker-c4d938c251e5)
4. [tfrs-movierec-serving](https://github.com/hojinYang/tfrs-movierec-serving)