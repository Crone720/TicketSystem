import disnake, aiosqlite
from system.config import *

class DeleteButton(disnake.ui.View):
    def __init__(self, channel: disnake.TextChannel):
        self.channel = channel
        super().__init__(timeout=None)

    @disnake.ui.button(label="Удалить Обращение", style=disnake.ButtonStyle.gray, custom_id="DeleteTicketButton")
    async def DeleteTicketButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer()
        if self.channel:
            await self.channel.delete(reason="Обращение Закрыто // https://github.com/Crone720")

class CloseButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Закрыть Обращение", style=disnake.ButtonStyle.gray, custom_id="CloseTicketButton")
    async def CloseTicketButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()

            await cursor.execute("SELECT * FROM Channels WHERE channelid=?", (interaction.channel_id,))
            target = await cursor.fetchone()
            if target:
                user_id = target[0]

                channel = interaction.guild.get_channel(interaction.channel_id)
                member = interaction.guild.get_member(user_id)
                if channel:
                    await cursor.execute("DELETE FROM Channels WHERE channelid=?", (interaction.channel_id,))
                    await cursor.execute("DELETE FROM bans WHERE userid=?", (user_id,))

                    await channel.set_permissions(member, view_channel=False)
                
                embed1 = disnake.Embed(description=f"Обращение Закрыто.\nЗакрыл {interaction.author.mention}")
                button.disabled = True
                await interaction.message.edit(view=self)
                await interaction.followup.send(embed=embed1, view=DeleteButton(channel))
            else:
                await interaction.followup.send(content="Канал не найден в базе данных.\nВероятно тикет уже закрыт или произошла ошибка в работе Базы Данных")
            await db.commit()