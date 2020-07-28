from discord.ext import commands
from discord import Member
from time import sleep
from discord.utils import get
from random import choice
from datetime import *
import discord, asyncio, json

DebugMode = False # True - Если он будет теститься НЕ на Основном сервере
admin = 454570874410893322 # Администратор бота 
maxnotice = 10 # Кол-во Предупреждений
pwd = '/root/cosmicbot/'

if DebugMode:
    guildid = 519087912445411368 # Айди сервера на котором он работает
    banid = 724953077668511755 # Айди роли - Бан Комнат
    mutevid = 721670097504305186 # Айди роли - Мут Войса
    mutecid = 721670108111699968 # Айди роли - Мут Чата
    systemchat = 718022274581790770 # Айди чата, где будет выводиться вся инфа бота
    privat = 712712509798481973 # Айди войса для создания приватки
    voices = [696475355933835304, 712672745032515676] # Список войс, где будет начисляться sXp
    modroles = [726743481749602336, 726743370126458921, 726743317873688586] # Zevs, Совет Helperov, Helper
else:
    guildid = 451479499096326144 # Айди сервера на котором он работает
    banid = 713467836005351474 # Айди роли - Бан Комнат
    mutevid = 700453147180531792 # Айди роли - Мут Войса
    mutecid = 700817777975361577 # Айди роли - Мут Чата
    systemchat = 728563290191429643 # Айди чата, где будет выводиться вся инфа бота
    privat = 731613881050595389 # Айди войса для создания приватки
    comXp = 731790615590993960 # Айди чата для команды info
    ruleV = [703642096665362523, 731790615590993960, 480336775571832832, 504756818640240651, 708733435329511434, 512696170515267612] # Чаты, где нужно удалять ссылки
    modchat = [728678422603235419, 451495119317762050, 706984082868928562, 703299442752618677, 700825032695218300, 451495022437859338, 728678960522723448] # Айди чатов, где можно использовать команды модерации
    xpchat = [703642096665362523, 708733435329511434, 703642995689390190, 504756818640240651, 504756818640240651, 480336775571832832] # Айди чатов, где будет начисляться xp
    voices = [728678685732896841, 728678766141898765, 728678852871716864, 451495514031259648, 700446251220467753, 713140675645800448, 526824208395927562, 526824693861187597, 526824423492157460, 526824787046301696, 700814082537947147, 700814103807131709, 700814121674735616, 700814143946752010, 700814225366450288, 700814245847236798, 723822514454790164] # Список войс, где будет начисляться sXp
    modroles = [451796620942770187, 700431066472644768, 700441104763322398] # Zevs, Совет Helperov, Helper

prefixCustom = "-"
block = {
    "penalty":{
        "user": False,
        "low": True,
        "medium": True,
        "high": True
    },
    "surprise":{
        "user": False,
        "low": False,
        "medium": True,
        "high": True
    },
    "get":{
        "user": False,
        "low": True,
        "medium": True,
        "high": True
    },
    "sxp":{
        "user": False,
        "low": True,
        "medium": True,
        "high": True
    },
    "link":{
        "user": False,
        "low": False,
        "medium": True,
        "high": True
    },
    "mod":{
        "user": False,
        "low": False,
        "medium": False,
        "high": False
    }
    
}

pattern = {
    "code": {
        "ver": "2.0",
        "verjson": "2.0"
    },
    "main": {
        "id": 0,
        "sXp": 0, # кол-во серверного опыта
        "nm": 0, # кол-во сообщений
        "timeVoice": 0,
        "timeBorn": None
    },
    "moderation": {
        "notice": 0, # кол-во предупреждений
        "note": "", # заметки
        "banroom": { # тип наказания
            "user": 0, # айди модератора
            "hasIt": False, # статус этого типа наказания
            "text": "", # причина наказания
            "time": { # время окончания
                "day": 0, # день
                "month": 0, # месяц
                "year": 0, # год
                "hour": 0, # час
                "minute": 0, # минута
                "second": 0 # секунда
            }
        },
        "mutevoice": {
            "user": 0, 
            "hasIt": False,
            "text": "", 
            "time": { 
                "day": 0,
                "month": 0,
                "year": 0,
                "hour": 0,
                "minute": 0,
                "second": 0
            }
        },
        "mutechat": {
            "user": 0,
            "hasIt": False,
            "text": "",
            "time": {
                "day": 0,
                "month": 0,
                "year": 0,
                "hour": 0,
                "minute": 0,
                "second": 0
            }
        }
    }
}

client = commands.Bot(command_prefix=prefixCustom)
client.remove_command('help')

async def editjson(ctx, id, time: int, tt, type, pen, text):
    mutec = client.get_guild(guildid).get_role(mutecid)
    mutev = client.get_guild(guildid).get_role(mutevid)
    ban = client.get_guild(guildid).get_role(banid)
    try:
        jr = json.loads(readStorage(f'DB/sXp/{id}'))
        list = json.loads(readStorage(f'DB/penalty/list'))
        copy = jr
        gg = list
        time = int(time)
        if type == "br":
            if not ban in ctx.guild.get_member(id).roles:
                await ctx.guild.get_member(id).add_roles(ban, reason=text)
            if not id in gg['banroom']:
                gg['banroom'].append(id)
                with open(f"{pwd}DB/penalty/list", "w") as write_file:
                    json.dump(gg, write_file)
            type = 'banroom'
            copy['moderation'][type]['hasIt'] = True
            copy['moderation'][type]['text'] = text
            if tt == 'd':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'mon':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'y':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'h':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'min':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 's':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
        elif type == "mv":
            if not ban in ctx.guild.get_member(id).roles:
                await ctx.guild.get_member(id).add_roles(mutev, reason=text)
            if not id in gg['mutevoice']:
                gg['mutevoice'].append(id)
                with open(f"{pwd}DB/penalty/list", "w") as write_file:
                    json.dump(gg, write_file)
            type = 'mutevoice'
            copy['moderation'][type]['hasIt'] = True
            copy['moderation'][type]['text'] = text
            if tt == 'd':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'mon':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'y':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'h':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'min':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 's':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
        elif type == "mc":
            if not ban in ctx.guild.get_member(id).roles:
                await ctx.guild.get_member(id).add_roles(mutec, reason=text)
            if not id in gg['mutechat']:
                gg['mutechat'].append(id)
                with open(f"{pwd}DB/penalty/list", "w") as write_file:
                    json.dump(gg, write_file)
            type = 'mutechat'
            copy['moderation'][type]['hasIt'] = True
            copy['moderation'][type]['text'] = text
            if tt == 'd':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'mon':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 30)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'y':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(days = time * 365)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'h':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(hours = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 'min':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(minutes = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            elif tt == 's':
                if pen == 'write':
                    today = date.today()
                    moment = datetime.now().time()
                    now = datetime.combine(today, moment)
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'add':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now + timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
                elif pen == 'remove':
                    now = datetime(year = copy['moderation'][type]['time']['year'],
                         month = copy['moderation'][type]['time']['month'],
                         day = copy['moderation'][type]['time']['day'],
                         hour = copy['moderation'][type]['time']['hour'],
                         minute = copy['moderation'][type]['time']['minute'],
                         second = copy['moderation'][type]['time']['second'])
                    deadline = now - timedelta(seconds = time)
                    copy['moderation'][type]['time']['day'] = deadline.day
                    copy['moderation'][type]['time']['month'] = deadline.month
                    copy['moderation'][type]['time']['year'] = deadline.year
                    copy['moderation'][type]['time']['hour'] = deadline.hour
                    copy['moderation'][type]['time']['minute'] = deadline.minute
                    copy['moderation'][type]['time']['second'] = deadline.second
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
    except FileNotFoundError:
        copy = pattern
        with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
            json.dump(copy, write_file)
        jr = json.loads(readStorage(f'DB/sXp/{id}'))
        await editjson(ctx, id, time, tt, type, pen, text)

def writeStorage(name, set):
    f = open(pwd + name, 'w')
    f.write(set)
    f.close()

def readStorage(name):
    f = open(pwd + name, 'r')
    set = f.read()
    f.close()
    return set

def lenStorage(name, set):
    f = open(pwd + name, 'r')
    all = f.readlines()
    f.close()
    try:
        return all[int(set)]
    except Exception as e:
        print(f'problem - {e}')

def god(user, level):
    if user.guild.id == guildid:
        lvl = ''
        if client.get_guild(guildid).get_role(modroles[0]) in user.roles:
            lvl = 'high'
        elif client.get_guild(guildid).get_role(modroles[1]) in user.roles:
            lvl = 'medium'
        elif client.get_guild(guildid).get_role(modroles[2]) in user.roles:
            lvl = 'low'
        else:
            lvl = 'user'
        if level[lvl] or user.id == admin:
            return True
        else:
            return False
    else:
        return False

def secure(ctx, chat, type):
    if type == 'mod':
        if chat.id in modchat:
            return True
        elif ctx.author.id == admin:
            return True
        else:
            return False
    elif type == 'info':
        if chat.id == comXp:
            return True
        elif ctx.author.id == admin:
            return True
        else:
            return False
    elif type == 'xp':
        if chat.id in xpchat or ctx.author.id == admin:
            return True
        else:
            return False

def check(id, type, td):
    try:
        jr = json.loads(readStorage(f'DB/sXp/{id}'))
        if type == 'banroom':
            if td == 'hasIt':
                return jr['moderation'][type]['hasIt']
            elif td == 'date':
                return datetime(year = jr['moderation'][type]['time']['year'],
                             month = jr['moderation'][type]['time']['month'],
                             day = jr['moderation'][type]['time']['day'],
                             hour = jr['moderation'][type]['time']['hour'],
                             minute = jr['moderation'][type]['time']['minute'],
                             second = jr['moderation'][type]['time']['second'])
        elif type == 'mutevoice':
            if td == 'hasIt':
                return jr['moderation'][type]['hasIt']
            elif td == 'date':
                return datetime(year = jr['moderation'][type]['time']['year'],
                             month = jr['moderation'][type]['time']['month'],
                             day = jr['moderation'][type]['time']['day'],
                             hour = jr['moderation'][type]['time']['hour'],
                             minute = jr['moderation'][type]['time']['minute'],
                             second = jr['moderation'][type]['time']['second'])
        elif type == 'mutechat':
            if td == 'hasIt':
                return jr['moderation'][type]['hasIt']
            elif td == 'date':
                return datetime(year = jr['moderation'][type]['time']['year'],
                             month = jr['moderation'][type]['time']['month'],
                             day = jr['moderation'][type]['time']['day'],
                             hour = jr['moderation'][type]['time']['hour'],
                             minute = jr['moderation'][type]['time']['minute'],
                             second = jr['moderation'][type]['time']['second'])
        elif type == 'voice': 
            try:
                member = client.get_guild(guildid).get_member(id)
                if td == 'status':
                    if member.voice.channel != None and member.voice.channel.id in voices:
                        return True
                    elif member.voice.channel != None and not member.voice.channel.id in voices:
                        return False
            except Exception as e:
                print(f'problem - {e}')
                return False
            
    except FileNotFoundError:
        copy = pattern
        with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
            json.dump(copy, write_file)
        jr = json.loads(readStorage(f'DB/sXp/{id}'))
        return check(id, type, id)

async def loop():
    print('start loop!')
    while True:
        mutec = client.get_guild(guildid).get_role(mutecid)
        mutev = client.get_guild(guildid).get_role(mutevid)
        ban = client.get_guild(guildid).get_role(banid)
        list = json.loads(readStorage(f'DB/penalty/list'))
        gg = list
        for i in gg['banroom']:
            if check(i, 'banroom', 'hasIt'):
                today = date.today()
                moment = datetime.now().time()
                now = datetime.combine(today, moment)
                deadline = check(i, 'banroom', 'date')
                if now > deadline:
                    try:
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    except FileNotFoundError:
                        copy = pattern
                        with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                            json.dump(copy, write_file)
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    copy = jr
                    copy["moderation"]["banroom"]["hasIt"] = False
                    with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                        json.dump(copy, write_file)
                    gg['banroom'].remove(i)
                    with open(f"{pwd}DB/penalty/list", "w") as write_file:
                        json.dump(gg, write_file)
                    ban = client.get_guild(guildid).get_role(banid)
                    ch = client.get_guild(guildid).get_member(i)
                    await ch.remove_roles(ban)
        for i in gg['mutevoice']:
            if check(i, 'mutevoice', 'hasIt'):
                today = date.today()
                moment = datetime.now().time()
                now = datetime.combine(today, moment)
                deadline = check(i, 'mutevoice', 'date')
                if now > deadline:
                    try:
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    except FileNotFoundError:
                        copy = pattern
                        with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                            json.dump(copy, write_file)
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    copy = jr
                    print(f'1. mv({i} - {copy["moderation"]["mutevoice"]["hasIt"]}')
                    copy["moderation"]["mutevoice"]["hasIt"] = False
                    print(f'2. mv({i} - {copy["moderation"]["mutevoice"]["hasIt"]}')
                    with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                        json.dump(copy, write_file)
                    copy = json.loads(readStorage(f'DB/sXp/{i}'))
                    print(f'3. mv({i} - {copy["moderation"]["mutevoice"]["hasIt"]}')
                    gg['mutevoice'].remove(i)
                    with open(f"{pwd}DB/penalty/list", "w") as write_file:
                        json.dump(gg, write_file)
                    ban = client.get_guild(guildid).get_role(mutevid)
                    ch = client.get_guild(guildid).get_member(i)
                    # if mutev in ch.roles:
                    await ch.remove_roles(mutev)
        for i in gg['mutechat']:
            if check(i, 'mutechat', 'hasIt'):
                today = date.today()
                moment = datetime.now().time()
                now = datetime.combine(today, moment)
                deadline = check(i, 'mutechat', 'date')
                if now > deadline:
                    try:
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    except FileNotFoundError:
                        copy = pattern
                        with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                            json.dump(copy, write_file)
                        jr = json.loads(readStorage(f'DB/sXp/{i}'))
                    copy = jr
                    copy["moderation"]["mutechat"]["hasIt"] = False
                    with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                        json.dump(copy, write_file)
                    gg['mutechat'].remove(i)
                    with open(f"{pwd}DB/penalty/list", "w") as write_file:
                        json.dump(gg, write_file)
                    ban = client.get_guild(guildid).get_role(mutecid)
                    ch = client.get_guild(guildid).get_member(i)
                    # if mutec in ch.roles:
                    await ch.remove_roles(mutec)
        for i in gg['voiceSXP']:
            if check(i,'voice', 'status'):
                try:
                    jr = json.loads(readStorage(f'DB/sXp/{i}'))
                except FileNotFoundError:
                    copy = pattern
                    with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                        json.dump(copy, write_file)
                    jr = json.loads(readStorage(f'DB/sXp/{i}'))
                copy = jr
                copy["main"]["timeVoice"] = copy["main"]["timeVoice"] + 30
                copy["main"]["sXp"] = copy["main"]["sXp"] + 1
                with open(f"{pwd}DB/sXp/{i}", "w") as write_file:
                    json.dump(copy, write_file)
            else:
                gg['voiceSXP'].remove(i)
                with open(f"{pwd}DB/penalty/list", "w") as write_file:
                    json.dump(gg, write_file)
        await asyncio.sleep(30)

token = open(f'{pwd}token', 'r').readline()

@client.event
async def on_ready():
    print('on')
    ch = client.get_channel(systemchat)
    await ch.send('Рафшан прибыл')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Космячем сервер!'))
    await loop()

@client.event
async def on_voice_state_update(member, before, after):
    try:
        bef = before.channel.id
    except:
        bef = 0
    try:
        aft = after.channel.id
    except:
        aft = 0
    if bef != aft and aft in voices and aft != 0:
        list = json.loads(readStorage(f'DB/penalty/list'))
        gg = list
        gg['voiceSXP'].append(member.id)
        with open(f"{pwd}DB/penalty/list", "w") as write_file:
            json.dump(gg, write_file)
    if bef != aft and aft == privat and aft != 0:
        channel = await after.channel.guild.create_voice_channel(name=f'Channel For {str(member.name)}', type=discord.ChannelType.voice, category=after.channel.category)
        await channel.set_permissions(member, manage_channels=True, stream=True, connect=True)
        await member.move_to(channel)

@client.event
async def on_message(message):
    await client.process_commands(message)
    id = message.author.id
    if not message.author.bot and message.guild.id == guildid:
        if ('http://' in message.content or 'https://' in message.content) and message.channel.id in ruleV and god(message.author, block['link']):
            try:
                jr = json.loads(readStorage(f'DB/sXp/{id}'))
                if not jr['moderation']['notice'] > 5:
                    await message.delete()
                    jr = json.loads(readStorage(f'DB/sXp/{id}'))
                    copy = jr
                    copy['moderation']['notice'] = copy['moderation']['notice'] + 1
                    with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                        json.dump(copy, write_file)
                    alert = await message.channel.send(embed = discord.Embed(title = 'Нарушение правил', description = f'Внимание пользователь ``{message.author.name}`` !\nВы нарушили правила сервера о отправки ссылок в чатах!\nЕсли будет у вас не меньше 5 предупреждений, то вы получаете навсегда мут чата!', color = discord.Colour.dark_red()))
                    msg = await message.author.send(embed = discord.Embed(title = 'Нарушение правил', description = f'Пользователь ``{message.author.name}`` !\n**У вас `{jr["moderation"]["notice"]}` предупреждений.**\nЕсли будет у вас не меньше 5 предупреждений, то вы получаете навсегда мут чата!', color = discord.Colour.dark_red()))
                    await asyncio.sleep(15)
                    await alert.delete()
                    await msg.delete()
                elif jr['moderation']['notice'] > 5:
                    await message.author.add_roles(client.get_guild(guildid).get_role(mutecid))
            except FileNotFoundError:
                copy = pattern
                with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                    json.dump(copy, write_file)
                jr = json.loads(readStorage(f'DB/sXp/{id}'))
                if not jr['moderation']['notice'] > 5:
                    await message.delete()
                    jr = json.loads(readStorage(f'DB/sXp/{id}'))
                    copy = jr
                    copy['moderation']['notice'] = copy['moderation']['notice'] + 1
                    with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                        json.dump(copy, write_file)
                    alert = await message.channel.send(embed = discord.Embed(title = 'Нарушение правил', description = f'Внимание пользователь ``{message.author.name}`` !\nВы нарушили правила сервера о отправки ссылок в чатах!\nЕсли будет у вас не меньше 5 предупреждений, то вы получаете навсегда мут чата!', color = discord.Colour.dark_red()))
                    msg = await message.author.send(embed = discord.Embed(title = 'Нарушение правил', description = f'Пользователь ``{message.author.name}`` !\n**У вас `{jr["moderation"]["notice"]}` предупреждений.**\nЕсли будет у вас не меньше 5 предупреждений, то вы получаете навсегда мут чата!', color = discord.Colour.dark_red()))
                    await asyncio.sleep(15)
                    await alert.delete()
                    await msg.delete()
                elif jr['moderation']['notice'] > 5:
                    await message.author.add_roles(client.get_guild(guildid).get_role(mutecid))
        if secure(message, message.channel, 'xp'):
            try:
                jr = json.loads(readStorage(f'DB/sXp/{id}'))
                jr = json.loads(readStorage(f'DB/sXp/{id}'))
                copy = jr
                copy["main"]["sXp"] = copy["main"]["sXp"] + 1
                copy["main"]["nm"] = copy["main"]["nm"] + 1
                with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                    json.dump(copy, write_file)
                jr = json.loads(readStorage(f'DB/sXp/{id}'))
            except:
                copy = pattern
                copy["main"]["sXp"] = copy["main"]["sXp"] + 1
                copy["main"]["nm"] = copy["main"]["nm"] + 1
                with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                    json.dump(copy, write_file)
                jr = json.loads(readStorage(f'DB/sXp/{id}'))

@client.command(pass_context=True)  
async def sxp(ctx, ping: discord.Member, type, number):
    if god(ctx.author, block['sxp']) and secure(ctx, ctx.channel, 'mod'):
        id = ping.id
        try:
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            copy = jr
            if type == "add":
                copy["main"]["sXp"] = copy["main"]["sXp"] + int(number)
            elif type == "del":
                copy["main"]["sXp"] = copy["main"]["sXp"] - int(number)
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            await ctx.send(':expressionless: Команда принята!')
        except:
            copy = pattern
            if type == "add":
                copy["main"]["sXp"] = copy["main"]["sXp"] + int(number)
            elif type == "del":
                copy["main"]["sXp"] = copy["main"]["sXp"] - int(number)
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
    else:
        try:
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
            if jr['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
        except FileNotFoundError:
            copy = pattern
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
        await ctx.message.delete()
        embed = discord.Embed(title = 'Нарушение', description = f"**Внимание!**\nВы использовали высокоуровневую команду... \nВам выдаётся предупреждение.\n**Кол-во предупреждений: **`{jr['moderation']['notice']}`", color = ctx.author.color)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        alert = await ctx.author.send(embed = embed)

@client.command(pass_context=True)  
async def notice(ctx, ping: discord.Member, type, number):
    if god(ctx.author, block['sxp']) and secure(ctx, ctx.channel, 'mod'):
        id = ping.id
        try:
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            copy = jr
            if type == "add":
                copy["moderation"]["notice"] = copy["moderation"]["notice"] + int(number)
            elif type == "del":
                copy["moderation"]["notice"] = copy["moderation"]["notice"] - int(number)
            if copy['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            await ctx.send(':expressionless: Команда принята!')
        except:
            copy = pattern
            if type == "add":
                copy["moderation"]["notice"] = copy["moderation"]["notice"] + int(number)
            elif type == "del":
                copy["moderation"]["notice"] = copy["moderation"]["notice"] - int(number)
            if copy['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
            with open(f"{pwd}DB/sXp/{id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            await ctx.send(':expressionless: Команда принята!')
    else:
        try:
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
            if jr['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
        except FileNotFoundError:
            copy = pattern
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
        await ctx.message.delete()
        embed = discord.Embed(title = 'Нарушение', description = f"**Внимание!**\nВы использовали высокоуровневую команду... \nВам выдаётся предупреждение.\n**Кол-во предупреждений: **`{jr['moderation']['notice']}`", color = ctx.author.color)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        alert = await ctx.author.send(embed = embed)

@client.command(pass_context=True)  
async def get(ctx, type):
    if god(ctx.author, block['get']) and secure(ctx, ctx.channel, 'mod'):
        if type == 'list':
            list = json.loads(readStorage(f'DB/penalty/list'))
            brl = len(list['banroom'])
            mvl = len(list['mutevoice'])
            mcl = len(list['mutechat'])
            embed = discord.Embed(title='Список людей в ')
            embed.add_field(name='Бан Комнат: ', value=brl, inline=True)
            embed.add_field(name='Мут Войса: ', value=mvl, inline=True)
            embed.add_field(name='Мут Чата: ', value=mcl, inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif type == 'banroom':
            list = json.loads(readStorage(f'DB/penalty/list'))
            brl = len(list['banroom'])
            gg = list['banroom']
            ids = ''
            embed = discord.Embed(title='Список людей в `Бан Комнат`:')
            nub = 0
            for i in gg:
                i += 1
                ids = ids + str(i) + '\n'
                embed.add_field(name=str(num) + '. ', value=i, inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif type == 'mutevoice':
            list = json.loads(readStorage(f'DB/penalty/list'))
            brl = len(list['mutevoice'])
            gg = list['mutevoice']
            ids = ''
            embed = discord.Embed(title='Список людей в `Мут Войса`:')
            nub = 0
            for i in gg:
                i += 1
                ids = ids + str(i) + '\n'
                embed.add_field(name=str(num) + '. ', value=i, inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif type == 'mutechat':
            list = json.loads(readStorage(f'DB/penalty/list'))
            brl = len(list['mutechat'])
            gg = list['mutechat']
            ids = ''
            embed = discord.Embed(title='Список людей в `Мут Чата`:')
            nub = 0
            for i in gg:
                i += 1
                ids = ids + str(i) + '\n'
                embed.add_field(name=str(num) + '. ', value=i, inline=True)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                jr = json.loads(readStorage(f'DB/sXp/{type}'))
                gg = type
                text = f"```ini\nСтатистика на сервере\n[sXp]: {jr['main']['sXp']},\n[Кол-во сообщений]: {jr['main']['nm']},\n[Кол-во секунд в Войсе]: {jr['main']['timeVoice']}```"
                await ctx.send(f'Информация о `{gg}`:' + text)
                text = f"```ini\nИнформация Модерации\n[Кол-во Системных Предупреждений]: {jr['moderation']['notice']},\n[Заметки]: {jr['moderation']['note']}```"
                await ctx.send(f'Информация о `{gg}`:' + text)
                if jr['moderation']['banroom']['hasIt']:
                    type = 'banroom'
                    text = f"```ini\nБан Комнат:\n[Имеет ли]: {jr['moderation'][type]['hasIt']},\n[Выдал]: {jr['moderation'][type]['user']},\n[Причина]: {jr['moderation'][type]['text']},\n[Дата окончания]: {jr['moderation'][type]['time']['day']}.{jr['moderation'][type]['time']['month']}.{jr['moderation'][type]['time']['year']} {jr['moderation'][type]['time']['hour']}:{jr['moderation'][type]['time']['minute']}:{jr['moderation'][type]['time']['second']}```"
                    await ctx.send(f'Информация о `{gg}`:' + text)
                if jr['moderation']['mutevoice']['hasIt']:
                    type = 'mutevoice'
                    text = f"```ini\nМут Войса:\n[Имеет ли]: {jr['moderation'][type]['hasIt']},\n[Выдал]: {jr['moderation'][type]['user']},\n[Причина]: {jr['moderation'][type]['text']},\n[Дата окончания]: {jr['moderation'][type]['time']['day']}.{jr['moderation'][type]['time']['month']}.{jr['moderation'][type]['time']['year']} {jr['moderation'][type]['time']['hour']}:{jr['moderation'][type]['time']['minute']}:{jr['moderation'][type]['time']['second']}```"
                    await ctx.send(f'Информация о `{gg}`:' + text)
                if jr['moderation']['mutechat']['hasIt']:
                    type = 'mutechat'
                    text = f"```ini\nМут Чата:\n[Имеет ли]: {jr['moderation'][type]['hasIt']},\n[Выдал]: {jr['moderation'][type]['user']},\n[Причина]: {jr['moderation'][type]['text']},\n[Дата окончания]: {jr['moderation'][type]['time']['day']}.{jr['moderation'][type]['time']['month']}.{jr['moderation'][type]['time']['year']} {jr['moderation'][type]['time']['hour']}:{jr['moderation'][type]['time']['minute']}:{jr['moderation'][type]['time']['second']}```"
                    await ctx.send(f'Информация о `{gg}`:' + text)
            except FileNotFoundError:
                await ctx.send(f'<:Pikoh:710418168690245683> Что-то его, `{type}`, не существует в моей базе')
    else:
        try:
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
            if jr['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
        except FileNotFoundError:
            copy = pattern
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
        await ctx.message.delete()
        embed = discord.Embed(title = 'Нарушение', description = f"**Внимание!**\nВы использовали высокоуровневую команду... \nВам выдаётся предупреждение.\n**Кол-во предупреждений: **`{jr['moderation']['notice']}`", color = ctx.author.color)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        alert = await ctx.author.send(embed = embed)
    
@client.command(pass_context=True)  
async def surprise(ctx, time, smile, *, name: str):
    if god(ctx.author, block['surprise']):
        author = ctx.message.author
        message = await ctx.send(f"Объявлен розыгрыш `{name}` через 5 секунд, который продлится `{time}` секунд") 
        autm = ctx.message
        await autm.delete()
        await asyncio.sleep(5)
        await message.add_reaction(smile)
        for i in range(int(time)):
            await message.edit(content=f"Жми {smile}, чтобы участвовать в розыгрыше в {name}.\nПрошло {i} секунд из {time}.")
            await asyncio.sleep(1)
        message = await message.channel.fetch_message(message.id)
        reaction = message.reactions[0]
        users = []
        auf = reaction.users() # Ауф! выкатываем со дворов...
        async for user in auf:
            if user.id != client.user.id:
                users.append(user)
        winner = choice(users)
        await author.send(f"Выиграл <@{winner.id}> в {name}")
        await message.edit(content=f"Выиграл <@{winner.id}> в {name}")
        await message.clear_reaction(smile)
        await asyncio.sleep(20)
        await message.delete()

@client.command(pass_context=True)  
async def penalty(ctx, prob: discord.Member, time, tt, type, pen, *, text: str):
    if god(ctx.author, block['penalty']) and secure(ctx, ctx.channel, 'mod'):
        await editjson(ctx, prob.id, time, tt, type, pen, text)
        await ctx.send(':expressionless: Команда принята!')
    else:
        try:
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
            if jr['moderation']['notice'] > maxnotice:
                await editjson(ctx, ctx.penalty.id, 9, 'y', 'mc', 'add', 'Большое кол-во предупреждений системы!')
        except FileNotFoundError:
            copy = pattern
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(copy, write_file)
            jr = json.loads(readStorage(f'DB/sXp/{ctx.author.id}'))
            jr['moderation']['notice'] = jr['moderation']['notice'] + 1
            with open(f"{pwd}DB/sXp/{ctx.author.id}", "w") as write_file:
                json.dump(jr, write_file)
        await ctx.message.delete()
        embed = discord.Embed(title = 'Нарушение', description = f"**Внимание!**\nВы использовали высокоуровневую команду... \nВам выдаётся предупреждение.\n**Кол-во предупреждений: **`{jr['moderation']['notice']}`", color = ctx.author.color)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        alert = await ctx.author.send(embed = embed)

@client.command(pass_context=True)
async def kick(ctx, pin: discord.Member):
    user=ctx.message.author
    channel=user.voice.channel
    perm = channel.permissions_for(user)
    perm = channel.permissions_for(pin)
    if channel.permissions_for(user).manage_channels and pin.voice.channel.id == channel.id and not pin.id == user.id:
        await channel.set_permissions(pin, connect=False)
        await pin.move_to(None)
    elif pin.id == user.id:
        await ctx.send(f"<@{pin.id}>, Ты пытаешься себя кикнуть?! \n Ну это... *кхм* дурка *кхм*")
    else:
        await ctx.send(f"<@{pin.id}>, Это не ваша приватка!")

@client.command(pass_context=True)  
async def info(ctx):
    if secure(ctx, ctx.channel, 'info'):
        id = ctx.author.id
        try:
            jr = json.loads(readStorage(f'DB/sXp/{id}'))
            embed = discord.Embed(description = f"**Ваш sXp(серверный опыт) :** `{jr['main']['sXp']}`\n**Кол-во сообщений :** `{jr['main']['nm']}`\n**Кол-во секунд проведённых в Voice чатах :** `{jr['main']['timeVoice']}`", color = ctx.author.color)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            alert = await ctx.send(embed = embed)
            await asyncio.sleep(15)
            await alert.delete()
        except:
            sXp = 0
            nm = 0
            embed = discord.Embed(title = 'Информация', description = f"**Ваш sXp(серверный опыт) :** `{sXp}`\n**Кол-во сообщений :** `{nm}`\n**Кол-во секунд проведённых в Voice чатах :** `0`", color = ctx.author.color)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            alert = await ctx.send(embed = embed)
            await asyncio.sleep(15)
            await alert.delete()

client.run(token)
