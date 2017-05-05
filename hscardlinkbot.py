"""
**someredditusername by /u/distinctvagueness**
*Inspired by people on /r/hearthstone*
"""
import praw
import re
import json
import difflib
"""REQUIRES AllSets.json source file from http://hearthstonejson.com/"""
with open('AllSets.json') as f:
    data = f.read()
    jsondata = json.loads(data) 
"""Get card images from the following website"""
imglinkbase = "(http://wow.zamimg.com/images/hearthstone/cards/enus/original/" 
png = ".png)"

r = praw.Reddit('Hearthstone Card Linker 1.2 by u/distinctvagueness')
r.login('USERNAME','PASSWORD)')

already_done = set()
regexp = re.compile(r'\[\[(.+?)]]')

for comment in praw.helpers.comment_stream(r, "bottest"):
    if comment.id not in already_done:    
        try:
            found = []
            maybe = []
            s = regexp.finditer(comment.body)
            for m in s:
                find = m.group(1)
                if(find == "help"): 
                     continue
                got = False
                for cardSet in jsondata:
                    if cardSet in ["Credits", "System", "Debug", "Missions"]:
                        continue
                    for card in jsondata[cardSet]:
                        if card["type"]== "Hero" or card["type"]== "Enchantment":
                            continue
                        low = card["name"]
                        if find < low:
                            break
                        if find == low:
                            card["set"] = cardSet
                            found.append(card)
                            got = True
                            break
                    if(got):
                        break
                if(got):
                    got = False
                    continue
                find = re.sub('[-"\'\.]', '', m.group(1))
                for cardSet in jsondata:
                    if cardSet in ["Credits", "System", "Debug", "Missions"]:
                        continue
                    for card in jsondata[cardSet]:
                        if card["type"]== "Hero" or card["type"] == "Enchantment":
                            continue
                        low = re.sub('[-"\'\.]', '', card["name"].lower())
                        mat = difflib.SequenceMatcher(None, find, low)
                        if(mat.ratio()>0.58):
                            card["set"] = cardSet
                            maybe.append(card)
                if(len(maybe)== 1):
                    found.append(maybe[0])
                maybe = []
            if(found):
                words = "It looks like you are mentioning Hearthstone cards using this bot's mockup. Here are the cards:  \n"
                for card in found:
                    words += "["+card["name"]+"]"+ imglinkbase + card["id"] + png  +"  \n"   
                    if "type" in card:   
                        words += "Type: " +card["type"]
                    if "playerClass" in card:
                        words += ", Class: " +str(card["playerClass"])
                    if "cost" in card:            
                        words += "  \nCost: " +str(card["cost"])   
                    if(card["type"] == "Minion"):                       
                        words += ", Attack: " +str(card["attack"])+ ", Health: " +str(card["health"])
                    elif(card["type"] == "Weapon"): 
                        words += ", Attack: " +str(card["attack"])+", Durabilty: " +str(card["durability"])
                    words += "  \nSet: " +card["set"]
                    if "rarity" in card:
                        words += ", Rarity: " +card["rarity"]   
                    if "race" in card:
                        words += ", Race: " +card["race"]
                    if "text" in card:
                        words += "  \nText: " +re.sub("<[^>]*>",'**',card["text"].encode('ascii', 'ignore'))
                    words += "  \n\n"
                comment.reply(words.encode('ascii', 'ignore'))
                already_done.add(comment.id)  
        except Exception as inst:
            f = open("exceptions.txt","a+")
            f.write(str(inst))
            f.close()
