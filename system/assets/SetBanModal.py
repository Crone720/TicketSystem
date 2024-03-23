import disnake, aiosqlite
from disnake import TextInputStyle
class MyModal(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        components = [
            disnake.ui.TextInput(
                label="Причина Блокировки",
                placeholder="<3",
                custom_id="reason",
                style=TextInputStyle.short,
                max_length=100,
            )
        ]
        super().__init__(
            title="Выдача блокировки",
            custom_id="banticket",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        async with aiosqlite.connect("system/ticket.db") as db:
            reason = inter.text_values["reason"]
            cursor = await db.cursor()
            await cursor.execute("INSERT INTO bans (userid, reason) VALUES (?, ?)", (self.member.id, reason))
            await db.commit()
            embed = disnake.Embed(title="Управление Блокировкой (Тикеты)", description=f"Вы Успешно заблокировали {self.member.mention} в тикетах. Причина:\n```{reason}```")
            await inter.send(embed=embed)