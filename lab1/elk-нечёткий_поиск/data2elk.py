import json
import codecs
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()

actions = []
with codecs.open('data/item_details_full.txt',encoding='utf-8') as f:
  for i,line in enumerate(f):
    rec = json.loads(line)
    action = {
    "_index": "items-index3",
    "_type": "items",
    "_id": int(rec["itemid"]),
    "_source": {"name":rec.get("attr1",""),"annotation":rec.get("attr0","")}
    }
    actions.append(action)
    if (i+1) % 100000 == 0:
      print i
      helpers.bulk(es,actions)
      actions = []
if len(actions) > 0:
  helpers.bulk(es,actions)
print i
