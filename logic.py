import flask
from flask import request
import psycopg2
import collections
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def connectToDatabase():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        print('PostgreSQL database connected with Python')
        # create a cursor
        return conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.route("/", methods=['GET'])
def homepage():
    print("HOMEPAGE")
    return "<h2>Welcome to My HomePage</h2>"

@app.route("/login", methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    cur = connectToDatabase()
    cur.execute("select username, name, age, address from user_login ul inner join user_details ud on ul.id = ud.f_id where ul.username = '" + username + "' and ul.\"password\" = '" + password + "'")
    user = cur.fetchall()
    cur.close()
    userAsJson = getAsJson(user)
    resultCount = len(userAsJson)
    if resultCount < 1:
        return "<h2>USER NOT FOUND</h2>"
    else:
        return "<h2>I'M LOGGED IN</h2><br><br><h2>%s</h2>"  %(userAsJson[0])


def getAsJson(user):
    objects_list = []
    for row in user:
        columns = collections.OrderedDict()
        columns["username"] = row[0]
        columns["name"] = row[1]
        columns["age"] = row[2]
        columns["address"] = row[3]
        objects_list.append(columns)
    return json.loads(json.dumps(objects_list))

app.run()