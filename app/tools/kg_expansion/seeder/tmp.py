import json
with open('tg_initial.json') as f:
  data = json.load(f)

for index,e in enumerate(data):
  if e["type"] == "node":


    s_labels = e["labels"]
    if len(s_labels) == 1:
      s_labels.append("http://www.nv_ontology.org/Synonym")

    data[index]["labels"] = s_labels
    
with open('tg_initial.json', 'w') as outfile:
    json.dump(data, outfile)