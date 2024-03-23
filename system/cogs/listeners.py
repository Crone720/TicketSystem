from disnake.ext import commands
from disnake.ext.commands.errors import MissingPermissions, CommandOnCooldown
import aiosqlite, disnake, datetime

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Channels (
                userid INTEGER,
                channelid INTEGER
            )
            """)
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                userid INTEGER PRIMARY KEY,
                reason TEXT
            )
            """)

            await db.commit()

from disnake.ext import commands
from disnake.ext.commands.errors import MissingPermissions, CommandOnCooldown
import aiosqlite, disnake, datetime

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("system/ticket.db") as db:
            cursor = await db.cursor()
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS Channels (
                userid INTEGER,
                channelid INTEGER
            )
            """)
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                userid INTEGER PRIMARY KEY,
                reason TEXT
            )
            """)

            await db.commit()

    @commands.Cog.listener()
    async def on_slash_error(self, inter, error):
        if isinstance(error, MissingPermissions):
            embedmissingpermission = disnake.Embed(title="Обращение", description="У вас недостаточно прав для использование команды")
            await inter.send(embed=embedmissingpermission, ephemeral=True)
        elif isinstance(error, CommandOnCooldown):
            time = disnake.utils.format_dt(datetime.datetime.now() + datetime.timedelta(seconds=error.retry_after), 'R')
            embedcooldown = disnake.Embed(
                title='Обращение',
                description=f'{inter.author.mention}, Вы сможете использовать эту команду '
                            f'через {time}',
                color=0x2F3136
            )
            await inter.send(embed=embedcooldown, ephemeral=True)
        elif isinstance(error, commands.MissingRole):
            embedmissingrole = disnake.Embed(title="Обращение", description="Вы не имеете необходимой роли для использования команды")
            await inter.send(embed=embedmissingrole, ephemeral=True)
def setup(bot):
    bot.add_cog(Listeners(bot))
            
def setup(bot):
    bot.add_cog(Listeners(bot))
