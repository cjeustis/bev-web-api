# SOURCE

### This is a RESTful API based on Flask and Flask-RESTPlus for use with the bev-web-app project

#### Getting set up:
 1. git clone https://github.com/cjeustis/bev-web-api.git
 2. cd bev-web-api
 3. virtualenv env
 4. source env/bin/activate
 5. pip install -r requirements.txt
 6. export PYTHONPATH=.:$PYTHONPATH
 7. python src/app.py
 8. http://localhost:8888/api/


#### Copy and past in terminal at the root of this directory to execute the commands above
 $ virtualenv env && source env/bin/activate && pip install -r requirements.txt && export PYTHONPATH=.:$PYTHONPATH
 $ python src/app.py


#### TODO:
 1. Configure authentication and authorization
 2. Temperature endpoint
 3. Recipe endpoint
 4. Data persistence