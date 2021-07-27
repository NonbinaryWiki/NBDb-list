from wikibase_api import Wikibase
import requests
import os

wb = Wikibase("https://data.nonbinary.wiki/w/api.php")

def cleanup():
    files = os.listdir(".")
    for f in files:
        if f.endswith(".txt"):
            os.remove(f)

def get_instance(id):
    iteminfo = wb.entity.get(id)
    try:
        instanceof = iteminfo["entities"][id]["claims"]["P1"][0]["mainsnak"]["datavalue"]["value"]["id"]
        if instanceof == "Q3": # Q3 = Standard personal pronoun
            print("{0} is   a STANDARD PRONOUN".format(id))
            return "sp"
        elif instanceof == "Q15": # Q15 = Neopronoun
            print("{0} is a NEOPRONOUN".format(id))
            return "neop"
        elif instanceof == "Q68": # Q68 = Nounself pronoun
            print("{0} is a NOUNSELF NEOPRONOUN".format(id))
            return "nounp"
        elif instanceof == "Q7":
            print("{0} is a GENDER IDENTITY".format(id))
            return "id"
        else:
            print("{0} is NOT a pronoun nor a gender identity".format(id))
            return "other"
    except KeyError:
        print("{0} doesn't have P1".format(id))
        return "unknown"

def write_items():
    cleanup() # reset the lists

    itemlist = "https://data.nonbinary.wiki/w/api.php?action=query&list=allpages&apnamespace=860&aplimit=500&format=json"

    files = {
        "id": "identities.txt",
        "sp": "standard_pronouns.txt",
        "neop": "neopronouns.txt",
        "nounp": "nounpronouns.txt",
        "other": "other.txt",
        "unknown": "unknown.txt"
    }

    data_json = requests.get(itemlist).json()
    cleanitems = data_json["query"]["allpages"]
    #print(cleanitems)

    for item in cleanitems:
        id = item["title"].replace("Item:", "")
        type = get_instance(id)
        f = open(files[type], "a")
        f.write("{0},".format(id))
        f.close()

write_items()
