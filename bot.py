import os
from sched import scheduler
from discord.ext import commands
import discord
from dotenv import load_dotenv
import zu_api
import sql
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
            await ctx.channel.send(str(user[1]) + "#" + str(user[2]) + " |--> Loot =  " + str(loot))
    else:
        await ctx.channel.send("Il n'y a pas d'utilisateurs enregistrés.")

#Manually send a reminder
@bot.command(name="check")
@commands.has_role('admin')
async def check(ctx):
    await SendReminder()

#Send message from bot to a specific channel
@bot.command(name="send")
@commands.has_role('admin')
async def send(ctx, channelID, message, end=None):
    if end is None:
        channel = bot.get_channel(int(channelID))
        await channel.send(str(message))
    else:
        await ctx.channel.send("Tu as entré trop d'arguments")

####################
# COMMON FUNCTIONS #
####################

#Send the reminder
async def SendReminder():
    list_users = sql.GetUsers()
    nbRemind = 0
    message = ""

    channel = bot.get_channel(int(os.getenv("REMIND_CHANNEL")))

    if list_users != []:
        for user in list_users:
            loot = zu_api.CheckActivity(str(user[1]), str(user[2]))
            if loot == False:
                message += "<@" + str(user[0]) + ">\n"
                nbRemind += 1
            else:
                pass

        if nbRemind == 0:
            message += "Tout le monde a fait son !journa aujourd'hui."
        elif nbRemind == 1:
            message += "Tu n'as pas fait ton !journa... Gros nul !"
        elif nbRemind > 1:
            message += "Vous n'avez pas fait votre !journa bande de nazes !"

        await channel.send(str(message))

    else:
        await channel.send("Il n'y a pas d'utilisateurs enregistrés.")

#############
# SCHEDULER #
#############

scheduler = AsyncIOScheduler()
scheduler.add_job(SendReminder, 'cron', hour='20', minute='00')
scheduler.start()

#############
# START BOT #
#############

bot.run(os.getenv("TOKEN"))
