import discord
import random
import time
from discord.ext import commands
from link_classe import Link
from client import User

client = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())


@client.command()
@commands.has_permissions(administrator=True)
async def add_link(ctx, url):
    if not ctx.author.bot:
        link = Link(guild=ctx.guild)
        link.add(url)
        embed = discord.Embed(title="Validation", description="Le lien a bien été ajouté à la liste.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def remove_link(ctx, id: int):
    if not ctx.author.bot:
        link = Link(guild=ctx.guild)
        link.remove(id)
        embed = discord.Embed(title="Validation", description=f"Le lien possédent l'id {id} à bien été supprimé.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def link_list(ctx):
    if not ctx.author.bot:
        link = Link(guild=ctx.guild)
        nmb = 0
        url_list = ""
        for url in link.list:
            url_list += f"[{nmb}] {url}\n"
            nmb += 1
        embed = discord.Embed(title="Liste des liens:", description=f"{url_list}", color=discord.Color.green())
        await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    if not ctx.author.bot:
        embed = discord.Embed(title='Mon prefix est "!".', description='''Liste des commandes:
!help (Vous informe sur toutes les commandes de Pylo.)
!clear (Permet de supprimer le nombre de message que vous voulez.)
!kick (Permet d'expulser une personne de votre serveur.)
!ban (Permet de bannir une personne de votre serveur.)
!unban (Permet de débannir une personne de votre serveur.)
!rank (Affiche l'xp de l'utilisateur en question.)
!reset_xp (Réinitialise l'xp de la personne en questions.)
!add_link (Ajoute un lien qui sera autoriser sur votre serveur.)
!remove_link (Supprime un des liens qui étais autoriser sur votre serveur.)
!link_list (Affiche tout les liens autoriser sur votre serveur.)
    ''', color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Pylo.gg"))


@client.command()
@commands.has_permissions(administrator=True)
async def reset_xp(ctx, member: discord.Member):
    if not ctx.author.bot:
        user = User(user=member, guild=ctx.guild)
        user.info['lvl'] = 0
        user.info['xp'] = 0
        user.info['xp_max'] = 500
        user.save()
    await ctx.send(embed=discord.Embed(title="Validation", description=f"{member} a été reinitialiser.",
                                       color=discord.Color.red()))


@client.command()
async def rank(ctx, member: discord.Member = None):
    if not ctx.author.bot:
        if member is None:
            member = ctx.author
        user = User(user=member, guild=ctx.guild)
        embed = discord.Embed(title=f"{member} (Niveau {user.info['lvl']})",
                              description=f"{user.info['xp']}/{user.info['xp_max']}xp", color=discord.Color.blue())
        embed.set_author(name=str(member), icon_url=member.avatar)
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, nmb: int):
    if not ctx.author.bot:
        await ctx.channel.purge(limit=nmb+1)


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.bot:
        await member.send("bonjour")
        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(title="Validation",
                                           description=f"Le membre {member} vien d'être bannis.\nRaison: {reason}",
                                           color=discord.Color.red()))


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
    if not ctx.message.author.bot:
        await ctx.guild.kick(member)
        await ctx.send(embed=discord.Embed(title="Validation", description=f"Le membre {member} vien d'être expulser.",
                                           color=discord.Color.red()))


@client.event
async def on_message(message):
    time.sleep(0.1)
    link = Link(guild=message.guild)
    if "discord.gg" in message.content or link.check(text=message.content):
        await message.delete()

    if not message.author.bot:
        user = User(user=message.author, guild=message.guild)
        user.info['xp'] = int(user.info['xp'])
        user.info['xp_max'] = int(user.info['xp_max'])
        user.info['lvl'] = int(user.info['lvl'])
        user.info['xp'] += random.randint(5, 15)

        if user.info['xp'] >= user.info['xp_max']:
            user.info['xp'] -= user.info['xp_max']
            user.info['lvl'] += 1
            user.info['xp_max'] = round(user.info['xp_max'] * 1.5)
            await message.channel.send(embed=discord.Embed(title=f":tada: Niveau {user.info['lvl']} :tada: ", description=f"GG {message.author} tu viens de monter d'un niveau.", color=discord.Color.green()))
        user.save()

    await client.process_commands(message)

client.run("MTE0NTA5MjM5NjA0NTA2MjIyOA.GQhmgC.aSx1lWO0zG5gJx4SR96dOPGAXNtnw04qTXoGsI")
