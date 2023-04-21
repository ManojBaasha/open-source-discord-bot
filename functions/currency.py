import json
import os
import discord

def add_score(member: discord.Member, amount: int):
    if os.path.isfile("currency.json"):
        with open("currency.json", "r") as fp:
            data = json.load(fp)
        try:
            data[f"{member.id}"]["score"] += amount
        except KeyError:  # if the user isn't in the file, do the following
            # add other things you want to store
            data[f"{member.id}"] = {"score": amount}
    else:
        data = {f"{member.id}": {"score": amount}}
    # saving the file outside of the if statements saves us having to write it twice
    with open("currency.json", "w+") as fp:
        # kwargs for beautification
        json.dump(data, fp, sort_keys=True, indent=4)
   # you can also return the new/updated score here if you want


def user_balance(member: discord.Member):
    with open("currency.json", "r") as fp:
        data = json.load(fp)
        try:
            amount = data[f"{member.id}"]["score"]
        except KeyError:  # if the user isn't in the file, do the following
            # add other things you want to store
            data[f"{member.id}"] = {"score": 500}
    return data[f"{member.id}"]["score"]

def subtract_score(member: discord.Member, amount: int):
    if os.path.isfile("currency.json"):
        with open("currency.json", "r") as fp:
            data = json.load(fp)
        try:
            data[f"{member.id}"]["score"] -= amount
        except KeyError:  # if the user isn't in the file, do the following
            # add other things you want to store
            data[f"{member.id}"] = {"score": amount}
    else:
        data = {f"{member.id}": {"score": amount}}
    # saving the file outside of the if statements saves us having to write it twice
    with open("currency.json", "w+") as fp:
        # kwargs for beautification
        json.dump(data, fp, sort_keys=True, indent=4)
   # you can also return the new/updated score here if you want