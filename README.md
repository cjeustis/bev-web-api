# SOURCE

### This is a RESTful API based on Flask and Flask-RESTPlus for use with the bev-web-app project

#### Getting set up:
 1. git clone https://github.com/cjeustis/bev-web-api.git
 2. cd bev-web-api
 3. virtualenv env
 4. source env/bin/activate
 5. pip install -r requirements.txt
 6. export PYTHONPATH=.:$PYTHONPATH
 7. python bev-web-api/app.py
 8. http://localhost:8888/api/


#### TODO:
 1. Configure authentication and authorization
 2. Temperature endpoint
 3. Recipe endpoint
 4. Data persistence