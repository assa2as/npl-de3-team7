#!flask/bin/python
from flask import Flask
from clickhouse_driver import Client
from datetime import datetime, timedelta
import time

cl = Client('35.195.166.173',port='9001')
def getTsHourBack():
    dt = datetime.now() - timedelta(hours=1)
    return int(time.mktime(dt.timetuple())*1000)

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
        ' group by id_item;'
    return getJson(cl.execute(q),['url','id_item','price','count'],ts)
def getUsers(ts=None):
    if ts == None:
        ts = getTsHourBack()
    else:
        try:
            ts = int(ts)
        except:
            ts = 0
    """
    q = 'select a.location, a.id_item, sum(a.total) as count, avg(b.total) as deep'+\
        ' from (select location, id_item, sessionId, count(*) as total from view_users group by location, id_item, sessionId) a'+\
        ' ANY LEFT JOIN (select sessionId, count(*) as total from view_users group by sessionId) b USING sessionId'+\
        ' where a.timestamp >= '+str(ts)+\
        ' group by a.location, a.id_item;'
    """
    q = ('select z.location, z.id_item, y.total, z.deep from'+
        ' (select x.location, x.id_item, avg(x.deep) as deep from ('+
        ' select a.location, a.id_item, a.sessionId, count(*) as deep'+
        ' from (select location,id_item,sessionId,min(timestamp) as ts1 from view_users group by location, id_item, sessionId) a'+
        ' all left join view_users b USING sessionId'+
        ' where b.timestamp <= a.ts1'+
        ' group by a.location, a.id_item, a.sessionId) x'+
        ' group by x.location, x.id_item) z'+
        ' all left join (select location, count(*) as total from view_users where timestamp >= {} group by location) y'+
        ' USING location'+
        ' order by z.location;').format(ts)
        
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