# ZUnivers : Rappel de !journa

Ce projet communautaire en lien avec [ZUnivers](https://zunivers.zerator.com/) n'est pas affilié à ZeratoR ou les équipes du ZUnivers.

## Description
L'objectif de ce code est de fournir un bot permettant de recevoir une notification discord quotidienne en cas d'oubli d'utilisation  de la commande `!journa`.

Vous pouvez directement rejoindre le serveur présenté ci-dessous pour utiliser le bot, ou cloner le repo pour développer le vôtre.

## Serveur discord
![Discord Banner](https://discord.com/api/guilds/994632493254836237/widget.png?style=banner2)

Rejoindre le serveur : [discord.gg/87tCbHAwma](https://discord.gg/87tCbHAwma)

|Commande|Effet|
|:--:|:--|
|`!sub`|Permet de s'abonner aux alertes quotidiennes
|`!unsub`|Permet de se désabonner des alertes quotidiennes. Supprime toutes les données personnelles de la base de données.

Les commandes doivent être entrées dans le channel `#sub-unsub`  
Les alertes sont envoyées tous les jours à **20h00** dans le channel `#daily-reminder` avec une mention pour les utilisateurs concernés, pensez à activer les notifications.

## Licence
Ce projet est fourni sous licence MIT.

## Contribuer
### Sur discord
Vous pouvez soumettre des propositions d'amélioration sur le serveur discord dans le channel `#discussion-features`.

### Sur GitHub
Vous pouvez également soumettre vos propositions en créant une nouvelle issue.  
(Les pull-request sont également acceptées)

## Développer
### Docker
```bash
git clone https://github.com/enzopicas/zunivers-reminder
cd zunivers-reminder
vim config #See 'config file' part bellow
mkdir data #DB will be saved here
docker-compose up -d
```

config file :
```
TOKEN= #discord bot token
REMIND_CHANNEL= #channel to send reminder ID
SUB_UNSUB_CHANNEL= #channel to accept commands ID
```
