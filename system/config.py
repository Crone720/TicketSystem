from enum import IntEnum, Enum

# Developed by ._.tomioka
# Discord Server - https://discord.gg/TxrQS4qXbM

class BotSettings(Enum):
    token = "token", #токен бота
    prefix = "!" #префикс бота

class IntSettings(IntEnum):
    Target = 1 #айди категории где будут создаваться каналы
    SupportRole = 1 #айди роли сапортов (те кто будут помогать)
    DeveloperRole = 1 #айди роли разработчика
    LogsChannel = 1 #куда будут приходить логи