import os
from sched import scheduler
from discord.ext import commands
import discord
from dotenv import load_dotenv
import zu_api
import sql
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

#Load private file including bot token and channels id
load_dotenv(dotenv_path="config")

#Init the discord bot and set command prefix
bot = commands.Bot(command_prefix="!")

#If not exist: creation of the db
sql.CreateDB()

################
# BOT COMMANDS #
################

#Test command used to ckeck if bot is alive
@bot.command(name="ping")
async def ping(ctx, end=None):
    if end is None:
        await ctx.channel.send("pong")
    else:
        await ctx.channel.send("Tu as entré trop d'arguments")

#Command used to add user to subscriber list
@bot.command(name="sub")
async def sub(ctx, end=None):
    #Command only available in sub-unsub channel
    if int(ctx.channel.id) != int(os.getenv("SUB_UNSUB_CHANNEL")):
        print (ctx.channel.id)
        return

    if end is None:
        if zu_api.CheckUser(str(ctx.message.author.name), str(ctx.message.author.discriminator)): #Check if user is a ZUnivers player
            if sql.AddUser(str(ctx.message.author.id), str(ctx.message.author.name), str(ctx.message.author.discriminator)):
                sub_role = discord.utils.get(ctx.message.guild.roles, name="sub")
                not_sub_role = discord.utils.get(ctx.message.guild.roles, name="not-sub")

                await ctx.message.author.add_roles(sub_role)
                await ctx.message.author.remove_roles(not_sub_role)
                await ctx.channel.send(ctx.message.author.mention + " : Tu rejoins les élus en t'abonnant aux alertes !")
            else:
                await ctx.channel.send(ctx.message.author.mention + " : Tu es déjà abonné aux alertes.")
        else:
            await ctx.channel.send(ctx.message.author.mention + " : Tu n'es pas encore membre ZUnivers. Commence par faire un !journa dans le serveur officiel.")
    else:
        await ctx.channel.send("Tu as entré trop d'arguments")

#Command used to unscribe to the alerts
@bot.command(name="unsub")
async def unsub(ctx, end=None):
    #Command only available in sub-unsub channel
    if int(ctx.channel.id) != int(os.getenv("SUB_UNSUB_CHANNEL")):
        print (ctx.channel.id)
        return

    if end is None:
        if sql.DelUser(str(ctx.message.author.id)):
            sub_role = discord.utils.get(ctx.message.guild.roles, name="sub")
            not_sub_role = discord.utils.get(ctx.message.guild.roles, name="not-sub")

            await ctx.message.author.add_roles(not_sub_role)
            await ctx.message.author.remove_roles(sub_role)
            await ctx.channel.send(ctx.message.author.mention + " : Tu es désabonné, tu ne peux plus compter que sur toi-même...")
        else:
            await ctx.channel.send(ctx.message.author.mention + " : Il faudrait déjà être abonné avant de se désabonner...")
    else:
        await ctx.channel.send("Tu as entré trop d'arguments")

############################
# ADMIN COMMANDS FOR DEBUG #
############################

#Show the list of suscribed users
@bot.command(name="list")
@commands.has_role('admin')
async def list(ctx):
    list_users = sql.GetUsers()

    if list_users != []:
        for user in list_users:
            loot = zu_api.CheckActivity(str(user[1]), str(user[2]))
            tower = zu_api.CheckAs(str(user[1]), str(user[2]))
            await ctx.channel.send(str(user[1]) + "#" + str(user[2]) + " | Loot =  " + str(loot) + " | As =  " + str(tower))
    else:
        await ctx.channel.send("Il n'y a pas d'utilisateurs enregistrés.")

#Test private message
@bot.command(name="mp")
@commands.has_role('admin')
async def mp(ctx):
    user = await bot.fetch_user(594195299967434773)
    await user.send('Hello World')

#Manually send a reminder
@bot.command(name="check")
@commands.has_role('admin')
async def check(ctx):
    await SendJournaReminder()
    await SendAsReminder()

#Send message from bot to a specific channel
@bot.command(name="send")
@commands.has_role('admin')
async def send(ctx, channelID, message, end=None):
    if end is None:
        channel = bot.get_channel(int(channelID))
        await channel.send(str(message))
    else:
        await ctx.channel.send("Tu as entré trop d'arguments")

@bot.command(name="time")
@commands.has_role('admin')
async def time(ctx):
    await ctx.channel.send(str(datetime.now()))

####################
# COMMON FUNCTIONS #
####################

#Send the !journa reminder
async def SendJournaReminder():
    list_users = sql.GetUsers()

    channel = bot.get_channel(int(os.getenv("ADMIN_CHANNEL")))

    if list_users != []:
        for user in list_users:
            loot = zu_api.CheckActivity(str(user[1]), str(user[2]))
            if loot == False:
                user_mention = await bot.fetch_user(user[0])
                await user_mention.send("Tu n'a pas fait ton !journa !")
            else:
                pass

    else:
        await channel.send("Il n'y a pas d'utilisateurs enregistrés.")

#Send the !as reminder
async def SendAsReminder():
    list_users = sql.GetUsers()

    channel = bot.get_channel(int(os.getenv("ADMIN_CHANNEL")))

    if list_users != []:
        for user in list_users:
            tower = zu_api.CheckAs(str(user[1]), str(user[2]))
            if tower == False:
                user_mention = await bot.fetch_user(user[0])
                await user_mention.send("Tu as 2 !as disponibles !")
            else:
                pass

    else:
        await channel.send("Il n'y a pas d'utilisateurs enregistrés.")

#############
# SCHEDULER #
#############

scheduler = AsyncIOScheduler()
scheduler.add_job(SendJournaReminder, 'cron', hour='20', minute='00')
scheduler.add_job(SendAsReminder, 'cron', hour='12', minute='00')
scheduler.start()

#############
# START BOT #
#############

bot.run(os.getenv("TOKEN"))
