# -*- coding: utf-8 -*-

from wikibase_api import Wikibase
import requests
import os
import pywikibot

wb = Wikibase("https://data.nonbinary.wiki/w/api.php")

def writearticle(text):
    site = pywikibot.Site("en", "nbw")
    page = pywikibot.Page(site, u"User:BinaryBot/List of NBDb items")
    page.text = text
    page.save(u"Bot: updating list.")

def generate():
    content = u"""This page is a list of all items in the NBDb, sorted by type. The list is automatically updated every day.

<small>Please, don't modify this page. It won't break the bot, but everything is overwritten daily, so any changes you make will be lost! Contact [[User:Ondo|Ondo]] to request any changes.</small>

== Pronouns ==
=== Standard pronouns ===
{0}

=== Nounself pronouns ===
{1}
    
=== Other neopronouns ===
{2}

== Gender identities ==
{3}

== Other items ==
{4}

== Unsorted items ==
I don't know where to sort the following items. Please, add a statement to their NBDb page with the property P1 ("instance of") and the proper value —they'll be correctly sorted the next time this page is generated!
{5}
    """

    lists = {
        "identities.txt": [],
        "standard_pronouns.txt": [],
        "neopronouns.txt": [],
        "nounpronouns.txt": [],
        "other.txt": [],
        "unknown.txt": []
    }

    for f in lists:
        try:
            file = open(f, "r", encoding='utf-8').read()
        except FileNotFoundError:
            print("File {0} doesn't exist. Skipping!".format(f))
            continue
        ids = file.split(",")
        for i in ids:
            if i.startswith("Q"): #sometimes there are "empty" items or other weirdnesses
                print(i)
                item = wb.entity.get(i)["entities"][i]
                #print(str(item))
                try:
                    label = item["labels"]["en"]["value"]
                except KeyError:
                    label = "??"
                try:
                    desc = item["descriptions"]["en"]["value"]
                except KeyError:
                    desc = "No description defined in English."
                line = "* [[nbdb:Item:{2}|{0}]] ({1})".format(label, desc, i)
                lists[f].append(line)
        
    print(str(lists))

    wikitext = content.format("\n".join(lists["standard_pronouns.txt"]), "\n".join(lists["nounpronouns.txt"]), "\n".join(lists["neopronouns.txt"]), "\n".join(lists["identities.txt"]), "\n".join(lists["other.txt"]), "\n".join(lists["unknown.txt"]))
    
    with open("wikitext.txt", "w", encoding='utf-8') as final:
        final.write(wikitext)

    writearticle(wikitext)

generate()
