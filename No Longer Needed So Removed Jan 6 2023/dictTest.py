import json

keys = []
values = []
for ind in range(0,5):
	keys.append("key" + str(ind))
	values.append("value" + str(ind))
print(keys)
print(values)

myDictList = []

for ind  in range(len(keys)):
	myDictList.append(dict(code = keys[ind],value = values[ind]))


print(json.dumps(myDictList,indent = 4))


