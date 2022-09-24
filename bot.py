import os
from sched import scheduler
from discord.ext import commands
from discord import option, permissions
from dotenv import load_dotenv
import zu_api
import sql
import modals
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

#Load private file including bot token and channels id
load_dotenv(dotenv_path="config")

#Init the discord bot and set command prefix
bot = commands.Bot()

#If not exist: creation of the db
sql.CreateDB()

################
# BOT COMMANDS #
################
@bot.slash_command(
    name="ping",
    description="Vérifier si le bot est actif."
)
async def ping(ctx):
    await ctx.respond("pong")

#Command used to add user to subscriber list
@bot.slash_command(
    name="sub",
    description="S'abonner aux alertes"
)
async def sub(ctx):
    #Command only available in sub-unsub channel

    if zu_api.CheckUser(str(ctx.author.name), str(ctx.author.discriminator)): #Check if user is a ZUnivers player
        if sql.AddUser(str(ctx.author.id), str(ctx.author.name), str(ctx.author.discriminator)):
            await ctx.respond(ctx.author.mention + " : Tu rejoins les élus en t'abonnant aux alertes !")
        else:
            await ctx.respond(ctx.author.mention + " : Tu es déjà abonné aux alertes.")
    else:
        await ctx.respond(ctx.author.mention + " : Tu n'es pas encore membre ZUnivers. Commence par faire un !journa dans le serveur officiel.")

#Command used to unscribe to the alerts
@bot.slash_command(
    name="unsub",
    description="Se désabonner des alertes"
)
async def unsub(ctx):
    #Command only available in sub-unsub channel

    if sql.DelUser(str(ctx.author.id)):
        await ctx.respond(ctx.author.mention + " : Tu es désabonné, tu ne peux plus compter que sur toi-même...")
    else:
        await ctx.respond(ctx.author.mention + " : Il faudrait déjà être abonné avant de se désabonner...")

############################
# ADMIN COMMANDS FOR DEBUG #
############################

#Show the list of suscribed users
@bot.slash_command(
    name="list",
    description="Affiche la liste de tous les utilisateurs."
)
async def list(ctx):
    list_users = sql.GetUsers()

    if list_users != []:
        for user in list_users:
            loot = zu_api.CheckActivity(str(user[1]), str(user[2]))
            tower = zu_api.CheckAs(str(user[1]), str(user[2]))
            await ctx.respond(str(user[1]) + "#" + str(user[2]) + " | Loot =  " + str(loot) + " | As =  " + str(tower))
    else:
        await ctx.respond("Il n'y a pas d'utilisateurs enregistrés.")

#Test private message
@bot.slash_command(
    name="mp",
    description="Test d'envoi des messages privés."
)
async def mp(ctx):
    user = await bot.fetch_user(594195299967434773)
    await user.send('Hello World')
    await ctx.respond("Message envoyé.")

#Manually send a reminder
@bot.slash_command(
    name="check",
    description="Enovoyer tous les rappels manuellement."
)
async def check(ctx):
    await SendJournaReminder()
    await SendAsReminder()
    await ctx.respond("Rappels envoyés.")

#Send message from bot to a specific channel
@bot.slash_command(
    name="send",
    description="Envoyer un message depuis le bot"
)
@option(
    "channel",
    description="Channel où envoyer le message",
    choices=["General", "Sub-Unsub", "Admin"]
)
@option(
    "tags",
    description="Tags à jouter au début du message",
    required=False
)
async def send(ctx, channel, tags):
    if channel == "General":
        channel_id = bot.get_channel(int(os.getenv("GENERAL_CHANNEL")))
    if channel == "Admin":
        channel_id = bot.get_channel(int(os.getenv("ADMIN_CHANNEL")))
    if channel == "Sub-Unsub":
        channel_id = bot.get_channel(int(os.getenv("SUB_UNSUB_CHANNEL")))

    modal = modals.Send_Modal(title="Envoyer message", channel_id=channel_id, tags=str(tags))
    await ctx.send_modal(modal)

#Print local time
@bot.slash_command(
    name="time",
    description="Afficher l'heure du serveur."
)
async def time(ctx):
    await ctx.respond(str(datetime.now()))

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

bot.run(token=os.getenv("TOKEN"))
