import discord, json, copy, os
from discord import Embed, ui, ButtonStyle
from discord.ext import commands

async def get_ent_data():
    with open("entreprise.json", "r") as f:
        data = json.load(f)
    return data

async def get_free_ent_slot():
    data = await get_ent_data()
    freespot = []
    for ent in data:
        slots = data[ent]["slots"]
        if slots :
            for i in range(len(slots)) :
                if (slots[i]["freespot"] > 0):
                    freetimeslot = slots[i]["value"]
                    freespot.append({"ent": ent, "slot": freetimeslot})
    return freespot

async def reserve_std_slot(stdlog, timeslot, ent):
    with open("studentdata.json", "r") as f:
        data = json.load(f)
        slots = data[stdlog]["slots"]
        for i in range(len(slots)):
            if (slots[i]["value"] == timeslot):
                slots[i]["usage"] = ent
    with open("studentdata.json", "w") as f:
        json.dump(data, f, indent=4)

async def reserve_ent_slot(stdlog, timeslot, ent):
    with open("entreprise.json", "r") as f:
        data = json.load(f)
        slots = data[ent]["slots"]
        for i in range(len(slots)):
            if (slots[i]["value"] == timeslot):
                slots[i]["freespot"] -= 1
                for j in range(len(slots[i]["logins"])):
                    if (slots[i]["logins"][j] == "None"):
                        slots[i]["logins"][j] = stdlog
                        break

    with open("entreprise.json", "w") as f:
        json.dump(data, f, indent=4)

async def get_student_data(stdlog):
    with open("studentdata.json", "r") as f:
        data = json.load(f)
        return data[stdlog]

async def freespot_std_from_data(data):
    freespots = []
    slots = data["slots"]
    for i in range(len(slots)):
        if (slots[i]["usage"] == "None"):
            freespots.append(slots[i]["value"])
    return freespots

async def check_student_file(stdlog):
    with open("studentdata.json", "r") as f:
        data = json.load(f)
        keys = data.keys()
        if stdlog in keys:
            return True
        else:
            return False

async def create_student_file(stdlog, name, surname):
    with open("studentdata.json", "r") as f:
        data = json.load(f)
        newstudent = copy.deepcopy(data["Default"])
    data[stdlog] = newstudent
    data[stdlog]["name"] = name
    data[stdlog]["surname"] = surname
    with open("studentdata.json", "w") as f:
        json.dump(data, f, indent=4)

async def update_data(stdlog, datatype, data):
    with open("studentdata.json", "r") as f:
        openeddata = json.load(f)
        openeddata[stdlog][datatype] = data
    with open("studentdata.json", "w") as f:
        json.dump(openeddata, f, indent=4)

async def make_new_ent_json(new_json):
    json_object = json.loads(new_json)
    with open("entreprise.json", "w") as f:
        json.dump(json_object, f, indent=4)