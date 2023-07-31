import discord
import os

class Link:
    def __init__(self, guild: discord.Guild) -> None:
        self.guild_id = guild.id
        try:
            if not os.path.exists("assets"):
                os.mkdir("assets")
            if not os.path.exists(os.path.join("assets", "servers")):
                os.mkdir(os.path.join("assets", "servers"))
            if not os.path.exists(os.path.join("assets", "servers", self.guild_id)):
                os.mkdir(os.path.join("assets", "servers", self.guild_id))
            if not os.path.exists(os.path.join("assets", "servers", self.guild_id, "users")):
                os.mkdir(os.path.join("assets", "servers", self.guild_id, "users"))
            with open(os.path.join("assets", "servers", self.guild_id, "blacklist.txt"), "r") as f:
                self.list = f.read().split("\n")
                self.list = self.list[0:-1]
        except:
            with open(os.path.join("assets", "servers", self.guild_id, "blacklist.txt"), "a") as f:
                self.list = []
    
    def add(self, url: str) -> None:
        self.list.append(url)
        self.save()

    def remove(self, id: int):
        self.list.remove(self.list[id])
        self.save()
    
    def save(self) -> None:
        with open(os.path.join("assets", "servers", self.guild_id, "blacklist.txt"), "w") as f:
            for i in self.list:
                f.write(f"{i}\n")

    def check(self, text: str) -> bool:
        for url in self.list:
            if url in text:
                return True
        return False