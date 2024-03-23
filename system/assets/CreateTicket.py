import disnake, aiosqlite, datetime
from system.config import *
from system.assets.CloseTicket import CloseButton
class CreateButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @disnake.ui.button(label="Создать Обращение", style=disnake.ButtonStyle.gray, custom_id="CreateTicketButton")
    async def CreateTicketButton(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer(ephemeral=True)
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT channelid FROM Channels WHERE userid=?", (interaction.author.id,))
            active_ticket = await cursor.fetchone()
            if active_ticket:
                activeid = active_ticket[0]
                view = disnake.ui.View(timeout=None)
                view.add_item(disnake.ui.Button(label="Перейти", style=disnake.ButtonStyle.link, url=f"https://discord.com/channels/{interaction.guild.id}/{activeid}"))
                embed = disnake.Embed(title="Обращение", description=f"У вас уже есть активный тикет")
                await interaction.send(embed=embed, ephemeral=True, view=view)
                return

            await cursor.execute("SELECT * FROM bans WHERE userid=?", (interaction.author.id,))
            ban = await cursor.fetchone()
            if ban:
                embed = disnake.Embed(title="Обращение", description="Вы Были забанены :shushing_face: :deaf_man:\nВ связись чего вы не можете создавать обращение.")
                await interaction.send(embed=embed, ephemeral=True)
                return

            category = interaction.guild.get_channel(IntSettings.Target)
            role = interaction.guild.get_role(IntSettings.SupportRole)
            if not category or not role:
                await interaction.send("Категория или роль стаффа не найдены, обратитесь к разработчику)", ephemeral=True)
                return

            channel = await category.create_text_channel(name=f"ticket-{interaction.author.name}")
            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            await channel.set_permissions(interaction.author, view_channel=True, send_messages=True)
            await channel.set_permissions(role, view_channel=True, send_messages=True)
            await cursor.execute("INSERT INTO Channels (userid, channelid) VALUES (?, ?)", (interaction.author.id, channel.id))
            await db.commit()
            lovetime = disnake.utils.format_dt(datetime.datetime.now(), style="R")
            channelembed = disnake.Embed(title="Обращение", description=f"Ожидайте ответа. Если в течени 48ч вам не ответили вы можете упомянуть Стафф.\nЗлоупотреблять Пингами запрещено!.\nДанное обращение открыто уже: {lovetime}")
            message = await channel.send(f"{interaction.author.mention} {role.mention}",embed=channelembed, view=CloseButton())
            await message.pin()
            view = disnake.ui.View(timeout=None)
            view.add_item(disnake.ui.Button(label="Перейти", style=disnake.ButtonStyle.link, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}"))
            embed = disnake.Embed(title="Обращение", description="Вы успешно создали обращение.")
            await interaction.send(embed=embed, ephemeral=True, view=view)