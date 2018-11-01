#!flask/bin/python
from flask import Flask
from clickhouse_driver import Client
from datetime import datetime, timedelta
import time

cl = Client('35.195.166.173',port='9001')
def getTsHourBack():
    dt = datetime.now() - timedelta(hours=1)
    return int(time.mktime(dt.timetuple()))

def getJson(recs,cols,ts):
    lst = []
    for rec in recs:
        d = {}
        for i,col in enumerate(cols):
            d[col] = rec[i]
        lst.append(d)
    return str({"timestamp": ts,"contents": lst,"check": True})

def getOrders(ts=None):
    if ts == None:
        ts = getTsHourBack()
    else:
        try:
            ts = int(ts)
        except:
            ts = 0
    q = 'select max(location) as url, id_item, sum(total_price_product) as price, sum(item_count) as count'+\
        ' from view_orders'+\
        ' where timestamp > '+str(ts)+\
        ' group by id_item FORMAT JSONEachRow;'
    return getJson(cl.execute(q),['url','id_item','price','count'],ts)
def getUsers(ts=None):
    if ts == None:
        ts = getTsHourBack()
    else:
        try:
            ts = int(ts)
        except:
            ts = 0
    q = 'select max(a.location) as url, a.id_item, count(*) as count, avg(b.deep) as deep'+\
        ' from view_users a'+\
        ' ANY LEFT JOIN (select sessionId, count(*) as deep from view_users group by sessionId) b USING sessionId'+\
        ' where a.timestamp >= '+str(ts)+\
        ' group by a.id_item FORMAT JSONEachRow;'
    return getJson(cl.execute(q),['url','id_item','count','deep'],ts)

app = Flask(__name__)

@app.route('/')
def index():
    return "Это API для чекера"

@app.route('/api/v1.0/users/')
def users1():
    return getUsers()

@app.route('/api/v1.0/users/<ts>')
def users2(ts):
    return getUsers(ts)

@app.route('/api/v1.0/orders/')
def orders1():
    return getOrders()

@app.route('/api/v1.0/orders/<ts>')
def orders2(ts):
    return getOrders(ts)

if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0", port=5001)