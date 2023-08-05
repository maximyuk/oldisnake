import os
import keep_alive
import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
import datetime
import codecs
from disnake.ui import Select, View
import sqlite3
import io
import aiohttp
from io import BytesIO
from disnake.enums import ButtonStyle
import pymysql
import pymysql.cursors

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix=None , intents=disnake.Intents.all(), test_guilds=None, command_sync_flags=command_sync_flags )






try:
  connect = pymysql.connect(
    host='sql7.freesqldatabase.com',
    port=3306,
    user='sql7594698',
    password='1Ng5el66wJ',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)  #подключення до бд
  cursor = connect.cursor()
  try:
    cursor.execute(
      "CREATE DATABASE IF NOT EXISTS sql7594698")  #тіп створює бд
  finally:
    connect.commit()
except Exception as ex:
  print(ex)
 
 


#---------------------------------------------------цей евентс означає коли бот добавляється на сервер-------------------------------------------------------------------------------------------
@bot.event
async def on_guild_join(guild):
#----------------------------------------------------------создає таблицю узерс коли бот добавляється на сервер----------------------------------------------------------------------------------------------------
    cursor.execute(f"create table if not exists sql7594698.users(guild_name varchar(50), user_name varchar(50),guild int default null, user_id int default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from sql7594698.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into sql7594698.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')

    cursor.execute(f"UPDATE sql7594698.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
    connect.commit()


#--------------------------------------------------------------создає таблицю guilds коли бот добавляється на сервер-----------------------------------------------------------------------
    cursor.execute(f"create table if not exists sql7594698.guilds(guild_name varchar(50) , guild_id bigint default null, welcome text, cmdkick int default 3, cmdwelcome int default 5)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from sql7594698.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into sql7594698.guilds values('{member.guild.name}', {member.guild.id}, NOT NULL, NOT NULL, NOT NULL)")
                connect.commit()
            else:
                print('\u200b')
    








#-------------------------------------------------------------------------------прогрузка бота + статус бота--------------------------------------------------------------------
 
@bot.event
async def on_ready():
    await bot.change_presence(status = disnake.Status.idle, activity = disnake.Activity(name = 'Дивиться ', type = disnake.ActivityType.watching)) 
 #-------------------------------------------------------------------создає таблицю users коли бот включається-------------------------------------------------------------------
    cursor.execute(f"create table if not exists sql7594698.users(guild_name varchar(33), user_name varchar(33),guild bigint default null, user_id bigint default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from sql7594698.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into sql7594698.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')



        cursor.execute(f"UPDATE sql7594698.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
        connect.commit()
#-------------------------------------------------------------Создає таблицю guilds коли бот включається-------------------------------------------------------------------

    cursor.execute(f"create table if not exists sql7594698.guilds(guild_name varchar(50), guild_id bigint default null, welcome text default null, cmdkick int default 3, cmdwelcome int default 5)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        cursor.execute(f"select * from sql7594698.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into sql7594698.guilds(guild_name, guild_id) values('{guild.name}' , {guild.id})")
            connect.commit()
        else:
            print('\u200b')




#--------------------------------------------------------------------добавляє всю інфу в users про чела коли він заходить на сервер-----------------------------------------------------
 
@bot.event
async def on_member_join(member):
    for member in member.guild.members:
        cursor.execute(f"select guild, user_id from sql7594698.users where guild = {member.guild.id} and user_id = {member.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into sql7594698.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
            connect.commit()
        else:
            print('\u200b')

#-------------------------------------------------------------------Добававляє всю інфу в guilds коли чел заходить на сервер----------------------------------------------
    for member in member.guild.members:
        cursor.execute(f"select guild_name ,guild_id from sql7594698.guilds where guild_name = '{member.guild.name}' and guild_id = {member.guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(
                f"insert into sql7594698.guilds values({member.guild.id} ,{member.guild.id}, NOT NULL, NOT NULL, NOT NULL)")
            connect.commit()
        else:
            print('\u200b')




@bot.event
async def on_member_remove(member):
    cursor.execute(
        f"update sql7594698.users set admin = 0 where user_id = {member.id} and guild = {member.guild.id}")
    connect.commit()











@bot.slash_command(name = "setadm", description="Видати рівень адміністратора")
async def setadm(ctx, user: disnake.Member=commands.Param(description="Виберіть користувача якому хочете видати рівень адміністратора"),* , lvl:int=commands.Param(description="Рівень який хочете видати", choices=["1","2", "3", "4", "5"])): 
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{ctx.user.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <5:
        emb4 = disnake.Embed(title=" Ой лишеньки, щось пішло не так! ",  description= f'\n▹ Мені здається комусь не хватає прав для використання цієї команди ', color=0xff9900)
        await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=disnake.Embed(title=f'Ой лишеньки, щось пішло не так!', description=f'Ви не можете повисити рівень адміністратора у якого рівень більше вашого! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            if user == ctx.user:
                emb4 = disnake.Embed(title=" Ой лишеньки, щось пішло не так! ",  description= f'\n▹ Мені здається ви хочете повисити самого себе! \n Вибачте але ви не зможете цього зробити! ', color=0xff9900)
                await ctx.send(embed = emb4)
            else:
                if lvl <0:
                    emb4 = disnake.Embed(title=" Ой лишеньки, щось пішло не так! ",  description= f'\n▹ Значення не повинне бути нижче нуля ', color=0xff9900)
                    await ctx.send(embed = emb4)
                if lvl >5:
                        embed7 = disnake.Embed(title=" Ой лишеньки, щось пішло не так! ", description=f"▹ Ви вказали не правильний рівень адміністратора. Повинно бути від 0 до 5!", color=0xffff00)
                        await ctx.send(embed=embed7)

                else:
                    if _admin == 5:
                        if lvl == 0:
                            cursor.execute(f"update sql7594698.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам cняли права адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав користувач: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                                
                            embed1=disnake.Embed(title= 'Выдача прав адміністратора' , description=f'Користувач {user.mention} тепер звичайний користувач! ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 1:
                            cursor.execute(f"update sql7594698.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{count}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {count} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 2:
                            cursor.execute(f"update sql7594698.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{count}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {count} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 3:
                            cursor.execute(f"update sql7594698.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{count}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {count} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)


                        if lvl == 4:
                            cursor.execute(f"update sql7594698.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{count}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {count} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)


                        if lvl >=5:
                            embed7 = disnake.Embed(title="Ой лишеньки, щось пішло не так", description=f"▹ Максимальний рівень який ви можете видати це - 4", color=0xffff00)
                            await ctx.reply(embed=embed7)


                    if _admin == 6:
                        if lvl == 0:
                            cursor.execute(f"update sql7594698.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам cняли права адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав користувач: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                                
                            embed1=disnake.Embed(title= 'Выдача прав адміністратора' , description=f'Користувач {user.mention} тепер звичайний користувач! ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 1:
                            cursor.execute(f"update sql7594698.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{lvl}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {lvl} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 2:
                            cursor.execute(f"update sql7594698.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{lvl}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {lvl} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 3:
                            cursor.execute(f"update sql7594698.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{lvl}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {lvl} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 4:
                            cursor.execute(f"update sql7594698.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{lvl}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {lvl} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)
                        if lvl == 5:
                            cursor.execute(f"update sql7594698.users set admin = 5 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам видали `{lvl}` рівень адміністратора на сервері `{ctx.guild.name}`', description=f'Команду виконав: {ctx.user.mention}', color= 0xffff00)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права адміністратора' , description=f'Користувач {user.mention} отримав {lvl} рівень администратора ', color=0xffff00)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.user.mention}', inline=True)
                            await ctx.send(embed=embed1)







@bot.slash_command(name = "changelvl", description="Видати рівень адміністратора")
async def changelvl(ctx , cmd:str=commands.Param(description="Назва команди", choices=["kick","welcome"]), alvl:int=commands.Param(description="Рівень на який ви хочете замінити", choices=["1","2", "3", "4", "5"])): 
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{ctx.user.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <5:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        await ctx.send(embed = emb4)  
    else:
        if cmd == "kick":
            if alvl == 1:
                cursor.execute(f"update sql7594698.guilds set cmdkick = 1 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "kick":
            if alvl == 2:
                cursor.execute(f"update sql7594698.guilds set cmdkick = 2 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "kick":
            if alvl == 3:
                cursor.execute(f"update sql7594698.guilds set cmdkick = 3 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "kick":
            if alvl == 4:
                cursor.execute(f"update sql7594698.guilds set cmdkick = 4 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "kick":
            if alvl == 5:
                cursor.execute(f"update sql7594698.guilds set cmdkick = 5 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "welcome":
            if alvl == 1:
                cursor.execute(f"update sql7594698.guilds set cmdwelcome = 1 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "welcome":
            if alvl == 2:
                cursor.execute(f"update sql7594698.guilds set cmdwelcome = 2 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "welcome":
            if alvl == 3:
                cursor.execute(f"update sql7594698.guilds set cmdwelcome = 3 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "welcome":
            if alvl == 4:
                cursor.execute(f"update sql7594698.guilds set cmdwelcome = 4 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if cmd == "welcome":
            if alvl == 5:
                cursor.execute(f"update sql7594698.guilds set cmdwelcome = 5 where guild_id = '{ctx.guild.id}'")
                connect.commit()
                emb4 = disnake.Embed(title=" Успешно ",  description= f'\n заработало нахой ', color=0x008080)
                await ctx.send(embed = emb4)
        if alvl >5:
            emb4 = disnake.Embed(title=" Лишеньки, мені здається щось пішло не так! ",  description= f'\n Максимальний рівень який ви можете встановити це - `5`  ', color=0x008080)
            await ctx.send(embed = emb4)
        if alvl <1:
            emb4 = disnake.Embed(title=" Лишеньки, мені здається щось пішло не так! ",  description= f'\n Мінімальний рівень який ви можете встановити це - `1` ', color=0x008080)
            await ctx.send(embed = emb4)









@bot.slash_command(name = "welcome", description="Встановити привітання нового користувача")
async def welcome(ctx, * , text):
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{ctx.user.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <6:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        await ctx.send(embed = emb4)
    else:
        cursor.execute(f"select * from sql7594698.guilds where guild_id = '{ctx.guild.id}'")
        _welcome = cursor.fetchone()['welcome']
        if text == "get":
            emb4 = disnake.Embed(title=" Приветствие учасника ",  description= f'\n▹ {_welcome}  ', color=0x008080)
            await ctx.send(embed = emb4)
        elif text == "remove":
            cursor.execute(f"update sql7594698.guilds set welcome = Null where guild_id = '{ctx.guild.id}'")
            connect.commit()
            emb4 = disnake.Embed(title=" Успешно ",  description= f'\n▹ Приветствие нового участника удалено. ', color=0x008080)
            await ctx.send(embed = emb4)
        else:
            cursor.execute(f"update sql7594698.guilds set welcome = '{text}' where guild_id = '{ctx.guild.id}'")
            connect.commit()
            emb4 = disnake.Embed(title=" Успешно ",  description= f'\n▹ Приветствие нового участника было добавлено. ', color=0x008080)
            await ctx.send(embed = emb4)







@bot.slash_command(name = "kick", description="Встановити привітання нового користувача")
async def kick(ctx, user: disnake.Member, *, reason = None):
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{ctx.user.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    cursor.execute(f"select * from sql7594698.guilds where guild_id = '{ctx.guild.id}'")
    _kick = cursor.fetchone()['kick']
    if _admin < _kick:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=disnake.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            if not reason:
              await user.kick()
              emb4 = disnake.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
              emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.user.mention}")
              await ctx.send(embed = emb4)
            else:
              await user.kick(reason=reason)
              emb4 = disnake.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
              emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.user.mention}")
              emb4.add_field(name = " Причиной тому стало \n ", value =  f"▹ {reason}")
              await ctx.send(embed = emb4)






@bot.slash_command(name = "info", description="Інформація про користувача")
async def get(ctx, * ,member:disnake.Member):
    cursor.execute(f"select * from sql7594698.users where guild = '{ctx.guild.id}' and user_id = '{member.id}'")
    _admin = cursor.fetchone()['admin']   
    emb = disnake.Embed(title=f"Информация про користувача {member}", color=member.color)
    emb.add_field(name="Ім'я:", value=member.display_name,inline=False)
    emb.add_field(name="Айді користувача:", value=member.id,inline=False)
    emb.add_field(name="Статус:", value=member.activity,inline=False)
    emb.add_field(name="Роль на сервері:", value=f"{member.top_role.mention}",inline=False)
    emb.add_field(name="Рівень адміністратора на сервері:", value=f"{_admin} рівень",inline=False)   
    await ctx.send(embed = emb)


@bot.slash_command(name = "command", description="Інформація про команду")
async def command(ctx, cmd:str=commands.Param(description="Виберіть команду", choices=["kick","welcome"])):
    cursor.execute(f"select * from sql7594698.guilds where guild_id = '{ctx.guild.id}'")
    _kick = cursor.fetchone()['cmdkick']
    cursor.execute(f"select * from sql7594698.guilds where guild_id = '{ctx.guild.id}'")
    _welcome = cursor.fetchone()['cmdwelcome']
    if  cmd == "kick":
        emb = disnake.Embed(title=f"Інформація про команду `kick`", color=disnake.Color.blue())
        emb.add_field(name="Стандартне Значення для використання команди `kick` - `3 рівень`!", value= f"На данному сервері для використання команди `kick` потрібен - `{_kick}` рівень адміністратора",inline=False)
        await ctx.send(embed = emb)

    if cmd == "welcome":
        emb = disnake.Embed(title=f"Інформація про команду `welcome`", color=disnake.Color.blue())
        emb.add_field(name="Стандартне Значення для використання команди `welcome` - `5 рівень`!", value= f"На данному сервері для використання команди `welcome` потрібен - `{_welcome}` рівень адміністратора",inline=False)
        await ctx.send(embed = emb)













@bot.slash_command(name = "help", description="Команди бота")
async def help(ctx):
    select = Select(
        placeholder= "Виберіть тип допомоги",
        options=[
            disnake.SelectOption(label = "Інформаційні команди", description = "Команди про інформацію сервера, користувача, і тп" ,emoji="💻"),
            disnake.SelectOption(label = "Команди для модерації", description = "Різні команди для модерації діскорд сервер по типу мут, кік, бан" , emoji="⚙"),
            disnake.SelectOption(label = "Розважальні команди", description = "Рандомні фоточки котиків, собачок і тп" , emoji="😂"),
            disnake.SelectOption(label = "Всі команди", description = "Список всіх команд" ,emoji="💾")
        ]
    )

    async def call_back(intaraction):
        if intaraction.author.id == ctx.author.id:
            value = select.values[0]
            view.remove_item(select)

            information = "```/get - інформація про користувача``` ```/help - список команд``` ```/command - інформація про команду```"
            moderation = "```/kick - вигнати користувача з серверу``` ```/setadm - видати рівень адміністратора на сервері```"
            fun = ""
            others = "" 

            if value == "Інформаційні команди":
                emb = disnake.Embed(title = "Інформаційні команди:", description=information, colour = disnake.Color.blue(), timestamp = ctx.created_at)
                emb.set_footer(text = f"Петрик 2022©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
            elif value == "Команди для модерації":
                emb = disnake.Embed(title = "Модераційні команди:", description=moderation, colour = disnake.Color.blue(), timestamp = ctx.created_at)
                emb.set_footer(text = f"Петрик 2022©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
            elif value == "Розважальні команди":
                emb = disnake.Embed(title = "Розважальні команди", description=fun, colour = disnake.Color.blue(), timestamp = ctx.created_at)
                emb.set_footer(text = f"Петрик 2022©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
            elif value == "Всі команди":
                emb = disnake.Embed(title ="Всі команди:", description=f"{information}\n{moderation}\n{fun}\n{others}", colour = disnake.Color.blue(), timestamp=ctx.created_at)
                emb.set_footer(text = f"Петрик 2022©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
        else:
            await intaraction.response.send_message("Це не твоя кнопка!", ephemeral=True)  

    select.callback = call_back
    view = View()
    view.add_item(select)

    emb = disnake.Embed(title = f"Cписок команд бота", description="Виберіть тип допомоги з запропонованих нижче!", colour = disnake.Color.blue(), timestamp=ctx.created_at)
    emb.set_thumbnail(url=ctx.guild.icon)
    emb.set_footer(text = f"Петрик 2022©", icon_url=bot.user.display_avatar)

    await ctx.send(embed = emb, view = view)


    



 



bot.run(token = "")

 
























# connect = sqlite3.connect('server.db')
# cursor = connect.cursor()

# @bot.event
# async def on_guild_join(guild):

#     cursor.execute("""CREATE TABLE IF NOT exists users (
#         guild_name varchar(50),
#         user_name varchar(50),
#         guild INT default NULL,
#         user_id INT default NULL,
#         mute int default null,
#         ban INT default Null,
#         warn INT default null,
#         admin INT default null

#     )""")
#     connect.commit()



#     cursor.execute("""CREATE TABLE IF NOT exists guilds (
#         guild_name varchar(50),
#         guild_id BIGINT default NULL,
#         welcome text
#     )""")
#     connect.commit()

#     for guild in bot.guilds:
#         for member in guild.members:
#             cursor.execute(f"select * from users where guild = {guild.id} and user_id = {member.id}")
#             if cursor.fetchone() is None:
#                 cursor.execute(f"insert into users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
#                 connect.commit()
#             else:
#                 print('\u200b')
#         cursor.execute(f"UPDATE rayabot.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
#         connect.commit()


#     for guild in bot.guilds:
#         for member in guild.members:
#             cursor.execute(f"select * from guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
#             if cursor.fetchone() is None:
#                 cursor.execute(f"insert into guilds values('{member.guild.name}', {member.guild.id}, NOT NULL)")
#                 connect.commit()
#             else:
#                 print('\u200b')
 



# @bot.event
# async def on_ready():
#     cursor.execute("""CREATE TABLE IF NOT exists users (
#         guild_name varchar(50),
#         user_name varchar(50),
#         guild INT default NULL,
#         user_id INT default NULL,
#         mute int default null,
#         ban INT default Null,
#         warn INT default null,
#         admin INT default null

#     )""")
#     connect.commit()


#     cursor.execute("""CREATE TABLE IF NOT exists guilds (
#         guild_name varchar(50),
#         guild_id BIGINT default NULL,
#         welcome text
#     )""")
#     connect.commit()


#     for guild in bot.guilds:
#         for member in guild.members:
#             cursor.execute(f"select * from users where guild = {guild.id} and user_id = {member.id}")
#             if cursor.fetchone() is None:
#                 cursor.execute(f"insert into users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
#                 connect.commit()
#             else:
#                 print('\u200b')

#         cursor.execute(f"UPDATE users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
#         connect.commit()


#     for guild in bot.guilds:
#         cursor.execute(f"select * from guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
#         if cursor.fetchone() is None:
#             cursor.execute(f"insert into guilds(guild_name, guild_id) values('{guild.name}' , {guild.id})")
#             connect.commit()
#         else:
#             print('\u200b')





# @bot.event
# async def on_member_join(member):
#     for member in member.guild.members:
#         cursor.execute(f"select guild, user_id from users where guild = {member.guild.id} and user_id = {member.id}")
#         if cursor.fetchone() is None:
#             cursor.execute(f"insert into users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
#             connect.commit()
#         else:
#             print('\u200b')



#     for member in member.guild.members:
#         cursor.execute(f"select guild_name ,guild_id from guilds where guild_name = '{member.guild.name}' and guild_id = {member.guild.id}")
#         if cursor.fetchone() is None:
#             cursor.execute(
#                 f"insert into guilds values({member.guild.id} ,{member.guild.id}, NOT NULL)")
#             connect.commit()
#         else:
#             print('\u200b')



# @bot.event
# async def on_member_remove(member):
#     cursor.execute(f"update users set admin = 0 where user_id = {member.id} and guild = {member.guild.id}")
#     connect.commit()
