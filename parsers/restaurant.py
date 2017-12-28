import json
from pprint import pprint

data = json.load(open('foodyo_output.json'))


def traverse(data):
    print ('--' * traverse.level + "> " + data['name'])
    for kid in data['children']:
        traverse.level += 1
        traverse(kid)
        traverse.level -= 1


traverse.level = 1

for restaurant in data["body"]["Recommendations"]:
    print(restaurant["RestaurantName"])
    for menuitem in restaurant["menu"]:
        if menuitem.get("type") == "sectionheader":
            for child_menuitem in menuitem["children"]:
                if child_menuitem.get("type") == "item" and child_menuitem["selected"] == 1:
                    traverse(child_menuitem)
