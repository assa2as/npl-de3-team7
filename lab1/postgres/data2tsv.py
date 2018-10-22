import json
import codecs
from tqdm import tqdm

ids, j = set(), 0
fw = codecs.open("data/items.tsv","w",encoding="utf-8")
with codecs.open('data/item_details_full.txt',encoding='utf-8') as f:
  for i,line in enumerate(f):
    rec = json.loads(line)
    id_ = rec["itemid"]
    if int(id_) not in ids:
      s = "\t".join((id_,
                     rec.get("attr1","").replace('\t',' ').replace('\n','<p>'),
                     rec.get("attr0","").replace('\t',' ').replace('\n','<p>')))
      fw.write(s+'\n')
      if (i+1) % 100000 == 0:
        print i+1,j
      ids.add(int(id_))
    else:
      j += 1
print i+1,j