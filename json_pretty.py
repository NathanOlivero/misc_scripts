import json

with open('./user-agent-headers.txt') as f:
  data = json.load(f)
  f.close()

prettydata = json.dumps(data, indent = 4, sort_keys=True)

with open('./user-agent-headers-pretty.txt', "w") as f:
    json.dump(prettydata, f)
