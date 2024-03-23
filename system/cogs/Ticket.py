import disnake, aiosqlite
from disnake.ext import commands
from system.config import *
from system.assets.CreateTicket import CreateButton
from system.assets.SetBanModal import MyModal
class CommandExecute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ticket")
    @commands.has_permissions(manage_channels=True)
    async def ticket(self, interaction):
        ...
    @ticket.sub_command(name="setup", description="Установить Тикеты")
    async def ticketsub(self, interaction: disnake.AppCommandInteraction):
        embed = disnake.Embed()
        embed.set_image(url="https://cdn.discordapp.com/attachments/1220061907285840007/1221077535463571576/ticket.png?ex=66114412&is=65fecf12&hm=f157bd595194dad0041806089d90fdd96627b77665a2008aa69ffab3f4feb82d&")
        await interaction.send("Вы успешно отправили Embed о создание тикета", ephemeral=True)
        await interaction.channel.send(embed=embed, view=CreateButton())

    @commands.slash_command(name="tickеt")
    @commands.cooldown(1, 180, commands.BucketType.user)
    @commands.has_role(IntSettings.SupportRole)
    async def ticketban(self, interaction):
        ...
    @ticketban.sub_command(name="ban", description="Выдать Блокировку")
    async def ticketbansub(self, interaction: disnake.AppCommandInteraction, member: disnake.Member):
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()

            await cursor.execute("SELECT * FROM bans WHERE userid=?", (member.id,))
            ban_entry = await cursor.fetchone()
            if ban_entry:
                embedban = disnake.Embed(title="Управление Участниками (Обращения)", description=f"{member.mention} Уже находится в блокировке.")
                await interaction.send(embed=embedban, ephemeral=True)
                return
        await interaction.response.send_modal(modal=MyModal(member))

    @commands.slash_command(name="tiсket")
    @commands.cooldown(1, 180, commands.BucketType.user)
    @commands.has_role(IntSettings.SupportRole)
    async def ticketunban(self, interaction):
        ...
    @ticketban.sub_command(name="unban", description="Снять Блокировку")
    async def ticketunbansub(self, interaction: disnake.AppCommandInteraction, member: disnake.Member):
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM bans WHERE userid=?", (member.id,))
            ban_entry = await cursor.fetchone()
            if not ban_entry:
                embednoban = disnake.Embed(title="Обращения", description=f"{member.mention} В данный момент не находится в блокировке")
                await interaction.send(embed=embednoban, ephemeral=True)
                return
            await cursor.execute("DELETE FROM bans WHERE userid=?", (member.id,))
            await db.commit()
            embedsecunban = disnake.Embed(title="Обращения", description=f"{member.mention} Был успешно разбанен в системе тикетов.")
            embedsecunban.set_footer(text="Теперь он может создавать обращения")
            await interaction.send(embed=embedsecunban)

def setup(bot):
    bot.add_cog(CommandExecute(bot))