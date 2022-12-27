import discord
import sql

class Send_Modal(discord.ui.Modal):
    def __init__(self, channel_id, tags, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.channel_id = channel_id
        self.tags = tags
        self.add_item(discord.ui.InputText(label="Message", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        print("tags value :")
        print(self.tags)
        if self.tags == "None":
            await self.channel_id.send(str(self.children[0].value))
        else:
            await self.channel_id.send(self.tags + str("\n") + str(self.children[0].value))

        await interaction.response.send_message("Message envoyé.")
        
class Unsub_Buttons(discord.ui.View):

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        
        await self.message.edit(view=self, content="Trop long.")
    @discord.ui.button(label="Toutes les alertes", row=0, style=discord.ButtonStyle.danger)
    async def all_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self, content=str(interaction.user.id))
    @discord.ui.button(label="Alertes quotidiennes !journa", row=1, style=discord.ButtonStyle.primary)
    async def journa_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self, content="Vous êtes désabonné des alertes !journa.")