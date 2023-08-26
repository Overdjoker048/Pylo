import json
import os
import discord

class User:
    def __init__(self, user: discord.Member, guild: discord.Guild) -> None:
        self.id = str(user.id)
        self.guild_id = str(guild.id)
        self.info = {
            "name": user.name,
            "xp": 0,
            "xp_max": 500,
            "lvl": 0
        }
        if not os.path.exists("assets"):
            os.mkdir("assets")
        if not os.path.exists(os.path.join("assets", "servers")):
            os.mkdir(os.path.join("assets", "servers"))
        if not os.path.exists(os.path.join("assets", "servers", self.guild_id)):
            os.mkdir(os.path.join("assets", "servers", self.guild_id))
        if not os.path.exists(os.path.join("assets", "servers", self.guild_id, "users")):
            os.mkdir(os.path.join("assets", "servers", self.guild_id, "users"))
        try:
            with open(os.path.join("assets", "servers", self.guild_id, "users", f"{self.id}.json"), "r+") as file:
                self.info = json.load(fp=file)
        except:
            with open(os.path.join("assets", "servers", self.guild_id, "users", f"{self.id}.json"), "w+") as file:
                json.dump(self.info, file, indent=2)

    def save(self) -> None:
        with open(os.path.join("assets", "servers", self.guild_id, "users", f"{self.id}.json"), "w+") as file:
            json.dump(self.info, file, indent=2)