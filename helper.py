import json

user_json = {}
filter_json = {}

with open("temlate_params2.json", 'r') as file:
    user_json = json.load(file)
with open("filter_template.json", 'r') as file2:
    filter_json = json.load(file2)

for filter_prm in user_json:
    for item in  user_json.get(filter_prm):
        if user_json.get(filter_prm).get(item)[1]:
            filter_json[filter_prm].append(int(user_json.get(filter_prm).get(item)[0]))

for region in user_json.get("regions"):
    if region[1]:
        for district in user_json.get("districts"):
            if int(region[0]) in user_json.get("districts").get(district).get("regions"):
                filter_json["districts"].append(user_json("districts").get(district).get(code)) 

if user_data.get("start_price").get("from"):
    filter_data["start_price"]["from"] = user_data.get("start_price").get("from") 

if user_data.get("start_price").get("to"):
    filter_data["start_price"]["to"] = user_data.get("start_price").get("to") 

if user_data.get("current_price").get("from"):
    filter_data["current__price"]["from"] = user_data.get("current_price").get("from") 

if user_data.get("current_price").get("to"):
    filter_data["current__price"]["to"] = user_data.get("current_price").get("to") 

