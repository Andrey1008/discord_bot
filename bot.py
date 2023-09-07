import discord
from discord import Embed, user, ui, utils, app_commands
from quart import Quart, render_template, request, redirect, url_for, make_response, send_from_directory, session
from quart_uploads import UploadSet, configure_uploads, ALL
from quart_discord import DiscordOAuth2Session, Unauthorized
from discord.ext import commands
from datetime import datetime
from ast import literal_eval
from pytz import timezone
from PIL import Image
from dotenv import load_dotenv
import requests
import json
import os
import sqlite3
import re
import asyncio
import time
import math
import secrets
import string

load_dotenv()
TOKEN = os.getenv('TOKEN')

DOMAIN = 'www.gpbot.site'

connect = sqlite3.connect("acces.db")
cursor = connect.cursor()
app = Quart(__name__)
photos = UploadSet('photos', ALL)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['DISCORD_CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "https://www.gpbot.site/callback"
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/data'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
configure_uploads(app, photos)

discord_o = DiscordOAuth2Session(app)


class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synced = False
        
    async def setup_hook(self) -> None:
        self.add_view(send())
        self.add_view(controls())
        self.loop.create_task(app.run_task(host='0.0.0.0', port=25573))

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name="vk.com/gulai_pole┃/help", status=discord.Status.do_not_disturb))
        await self.tree.sync()
        print("synced")
        self.synced = True
        print(f"logged as {self.user}")


intents = discord.Intents.all()
intents.message_content = True

my_bot = MyBot(command_prefix=">", intents=intents)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.errorhandler(404)
def error_handler(error):
    return "Вы куда то нажали и все пропало", 404


@app.route("/")
async def home():
    return await render_template("index.html", authorized=await discord_o.authorized)


@app.route('/favicon.ico')
async def favicon():
    return await send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/android-chrome-192x192.png')
async def android_chrome_192():
    return await send_from_directory(os.path.join(app.root_path, 'static'), 'android-chrome-192x192.png', mimetype='image/vnd.microsoft.icon')


@app.route('/android-chrome-512x512.png')
async def android_chrome_512():
    return await send_from_directory(os.path.join(app.root_path, 'static'), 'android-chrome-512x512.png', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
async def robots():
    return await send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')


@app.route('/.well-known/discord')
async def discordfile():
    return await send_from_directory(os.path.join(app.root_path, 'static'), 'discord')


@app.route("/login")
async def login():
    return await discord_o.create_session()


@app.route("/callback")
async def callback():
    try:
        await discord_o.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


async def check_perms(user_id, guild_id):
    res1 = cursor.execute("SELECT id FROM ids")
    ids = [f[0] for f in res1]
    res2 = cursor.execute(f"SELECT guild_id FROM ids WHERE id=(?)", [str(user_id)])
    guild_ids = [f[0] for f in res2]
    if str(user_id) in ids and str(guild_id) in guild_ids:
        return True
    return False


async def control(guild_id):
    for guild in await discord_o.fetch_guilds():
        if guild.permissions.administrator and guild.id == guild_id:
            return True
    return False


@app.route("/dashboard")
async def dashboard():
    try:
        if not await discord_o.authorized:
            return redirect(url_for("login"))

        async def get_guild_ids():
            final = []
            for guild in my_bot.guilds:
                final.append(guild.id)
            return final

        guild_count = len(my_bot.guilds)
        guild_ids = await get_guild_ids()
        user_guilds = await discord_o.fetch_guilds()
        guilds = []
        for guild in user_guilds:
            if guild.permissions.administrator or await check_perms((await discord_o.fetch_user()).id, guild.id):
                guild.class_color = "green-border" if guild.id in guild_ids else "red-border"
                if guild.id in guild_ids or guild.permissions.administrator:
                    guilds.append(guild)

        def member_count(guild_id):
            try:
                return (my_bot.get_guild(guild_id)).member_count
            except:
                pass

        guilds.sort(key=lambda x: x.class_color == "red-border")
        user = await discord_o.fetch_user()
        name = user.name
        avatar = user.avatar_url
        return await render_template("dashboard.html", username=name, guild_count=guild_count, guilds=guilds, member_count=member_count, avatar_url=avatar)
    except Unauthorized:
        return redirect(url_for("login"))


async def send_embed(
        channel,
        title,
        description,
        guild,
        user_id,
        name1,
        desc1,
        name2,
        desc2,
        name3,
        desc3,
        name4,
        desc4,
        name5,
        desc5,
        name6,
        desc6,
        name7,
        desc7,
        name8,
        desc8,
        name9,
        desc9,
        name10,
        desc10,
        color,
        role_id,
        pic_url,
        include_pic,
    ):
    if color is None:
        color = 0
    try:
        colour=int(hex(literal_eval((str('0x')+str(color)).translate({ord("#"): None}))), 0)
    except:
        colour = 0x000000
    embed = discord.Embed(title=title, description=description, color=colour)
    guild_ = await my_bot.fetch_guild(guild)
    user = await guild_.fetch_member(user_id)
    embed.set_author(name=user.display_name, url=f"https://discordapp.com/users/{user_id}", icon_url=user.display_avatar.url)
    def check(embed_c, name_c, desc_c):
        if name_c is not None and desc_c is not None:
            return embed_c.add_field(name=name_c, value=desc_c, inline=False)
        elif name_c is not None and desc_c is None:
            return embed_c.add_field(name=name_c, inline=False)
        else:
            pass
    check(embed, name1, desc1)
    check(embed, name2, desc2)
    check(embed, name3, desc3)
    check(embed, name4, desc4)
    check(embed, name5, desc5)
    check(embed, name6, desc6)
    check(embed, name7, desc7)
    check(embed, name8, desc8)
    check(embed, name9, desc9)
    check(embed, name10, desc10)
    try:
        if pic_url != None:
            if os.path.splitext(pic_url)[1] != '.png' and os.path.splitext(pic_url)[1] != '.jpg' and os.path.splitext(pic_url)[1] != '.gif':
                im1 = Image.open(f"{os.getcwd()}/static/data/{pic_url}")
                filename = os.path.splitext(pic_url)[0]
                quality = 100
                if os.path.getsize(f"{os.getcwd()}/static/data/{pic_url}") > 10000000:
                    print(quality)
                    quality = int(1000000000/os.path.getsize(f"{os.getcwd()}/static/data/{pic_url}"))-5
                im1.save(f'{os.getcwd()}/static/data/{filename}.png', quality=quality)
                os.remove(f"{os.getcwd()}/static/data/{pic_url}")
                url = f"https://{DOMAIN}/static/data/{filename}.png"
                embed.set_image(url=url)
            else:
                url = f"https://{DOMAIN}/static/data/{pic_url}"
                embed.set_image(url=url)
    except Exception as e:
        print(e)
        pass
    if include_pic == 'on':
        utctime = datetime.now(timezone('Europe/Moscow'))
        time_footer = utctime.replace(microsecond=0, tzinfo=None)
        embed.set_footer(text=f'МСК: {time_footer}')
    if channel is not None:
        channel_ = await guild_.fetch_channel(channel)
        if role_id == 'no-ping':
            message = await channel_.send(embed=embed)
            log_list = [(await discord_o.fetch_user()).id, guild, 3, f"https://discord.com/channels/{guild}/{channel}/{message.id}", round(time.time())]
            cursor.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?, ?)", log_list)
            connect.commit()
        else:
            message = await channel_.send(f'<@&{role_id}>', embed=embed)
            log_list = [(await discord_o.fetch_user()).id, guild, 3, f"https://discord.com/channels/{guild}/{channel}/{message.id}", round(time.time())]
            cursor.execute(f"INSERT INTO logs VALUES (?, ?, ?, ?, ?)", log_list)
            connect.commit()
    

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    user = await discord_o.fetch_user()
    if await check_perms(user.id, guild_id) or await control(guild_id):
        if not await discord_o.authorized:
            return redirect(url_for("login"))
        return redirect(url_for("send", guild_id=guild_id))
    else:
        return redirect(url_for("dashboard"))


@app.route("/dashboard/<int:guild_id>/send", methods=['POST', 'GET'])
async def send(guild_id):
    try:
        user = await discord_o.fetch_user()
        if await check_perms(user.id, guild_id) or await control(guild_id):
            if not await discord_o.authorized:
                return redirect(url_for("login"))
            async def get_guild(guild_id):
                guild = my_bot.get_guild(guild_id)
                if guild is None:
                    return None
                roles_ = await guild.fetch_roles()
                roles_dict = {
                    "role_id": [],
                    "role_name": []
                }
                for role in roles_:
                    roles_dict['role_id'].append(role.id)
                    roles_dict['role_name'].append(role.name)

                text_channel_list = {
                    'channel_name': [],
                    'channel_id': []
                }
                for channel in guild.channels:
                    if str(channel.type) == 'text':
                        text_channel_list["channel_name"].append(channel.name)
                        text_channel_list["channel_id"].append(channel.id)
                guild_data = {
                    "name": guild.name,
                    "id": guild.id,
                    "guild_chan": text_channel_list,
                    "prefix": "?",
                    "guild_roles": roles_dict
                    }

                return guild_data

            guild = await get_guild(guild_id)
            user_name = None
            try:
                user_name = ((my_bot.get_guild(guild_id)).get_member(user.id)).display_name
            except:
                user_name = user.name
            if guild is None:
                return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
            channels = guild["guild_chan"]
            roles = guild["guild_roles"]
            user_id = (await discord_o.fetch_user()).id
            if request.method == "POST":
                try:
                    pic = await photos.save((await request.files)['file'], name=f"{''.join((secrets.choice(string.ascii_letters) for i in range(12)))}.")
                except Exception as e:
                    print(e)
                    pic = None
                await send_embed(
                    (await request.form).get('channels'),
                    (await request.form).get('title'),
                    (await request.form).get('desc'),
                    guild["id"],
                    user_id,
                    (await request.form).get('title1'),
                    (await request.form).get('desc1'),
                    (await request.form).get('title2'),
                    (await request.form).get('desc2'),
                    (await request.form).get('title3'),
                    (await request.form).get('desc3'),
                    (await request.form).get('title4'),
                    (await request.form).get('desc4'),
                    (await request.form).get('title5'),
                    (await request.form).get('desc5'),
                    (await request.form).get('title6'),
                    (await request.form).get('desc6'),
                    (await request.form).get('title7'),
                    (await request.form).get('desc7'),
                    (await request.form).get('title8'),
                    (await request.form).get('desc8'),
                    (await request.form).get('title9'),
                    (await request.form).get('desc9'),
                    (await request.form).get('title10'),
                    (await request.form).get('desc10'),
                    (await request.form).get('color'),
                    (await request.form).get('role'),
                    pic,
                    (await request.form).get('date')
                )
            embed_builder_data = [user_name,
                                  ((my_bot.get_guild(guild_id)).get_member(user_id)).display_avatar.url,
                                  my_bot.user.display_name,
                                  my_bot.user.display_avatar.url
                                  ]
            return await render_template("guild.html", domain=DOMAIN, guild_name=guild['name'], length=len(channels['channel_name']), channels=channels, length_role=len(roles['role_name']), roles=roles, guild_id=guild_id, embed_builder_data=embed_builder_data)
        else:
            return redirect(url_for("dashboard"))
    except Unauthorized:
        return redirect(url_for("login"))


@app.route('/dashboard/<int:guild_id>/logs')
async def logs(guild_id):
    try:
        user = await discord_o.fetch_user()
        if await check_perms(user.id, guild_id) or await control(guild_id):
            if not await discord_o.authorized:
                return redirect(url_for("login"))
            log = {
                "user_id": [],
                "guild_id": [],
                "action": [],
                "link": [],
                "time": []
            }
            res1 = cursor.execute(f"SELECT user_id FROM logs WHERE guild_id={str(guild_id)} ORDER BY time DESC")
            user_ids = res1.fetchall()
            res2 = cursor.execute(f"SELECT guild_id FROM logs WHERE guild_id={str(guild_id)} ORDER BY time DESC")
            guilds = res2.fetchall()
            res3 = cursor.execute(f"SELECT action FROM logs WHERE guild_id={str(guild_id)} ORDER BY time DESC")
            actions = res3.fetchall()
            res4 = cursor.execute(f"SELECT link FROM logs WHERE guild_id={str(guild_id)} ORDER BY time DESC")
            links = res4.fetchall()
            res5 = cursor.execute(f"SELECT time FROM logs WHERE guild_id={str(guild_id)} ORDER BY time DESC")
            times = res5.fetchall()
            length = len(user_ids)
            async def name(guild_id, user_id):
                try:
                    guild = await my_bot.fetch_guild(guild_id)
                    username = (await guild.fetch_member(user_id)).display_name
                    return username
                except:
                    username = user_id
                    return username
            page_no = 1
            logs_per_page = 5
            if request.args.get('page') is not None:
                page_no = int(request.args.get('page'))
            if (page_no*5) > length:
                logs_per_page = logs_per_page - (page_no*5 - length)
                if logs_per_page != 0:
                    page_no = length/logs_per_page
            for i in range(int(page_no*logs_per_page)-logs_per_page, int(page_no*logs_per_page)):
                if str(guild_id) == re.sub("[()',]", "", str(guilds[i])):
                    log['user_id'].append(re.sub("[()',]", "", str(user_ids[i])))
                    log['guild_id'].append(re.sub("[()',]", "", str(guilds[i])))
                    log['action'].append(re.sub("[()',]", "", str(actions[i])))
                    log['link'].append(re.sub("[()',]", "", str(links[i])))
                    log['time'].append(re.sub("[()',]", "", str(times[i])))
            def get_timestamp(t):
                try:
                    return datetime.fromtimestamp(int(t), timezone('Europe/Moscow')).replace(microsecond=0, tzinfo=None)
                except:
                    return datetime.fromtimestamp(int(0), timezone('Europe/Moscow')).replace(microsecond=0, tzinfo=None)
            current_page = 1
            if request.args.get('page') is not None:
                current_page = int(request.args.get('page'))
            return await render_template("logs.html", domain=DOMAIN, guild_id=guild_id, name=name, logs=log, length=logs_per_page, time=get_timestamp, pages_no=math.ceil(length/5), current_page=current_page)
        else:
            return redirect(url_for("dashboard"))
    except Unauthorized:
        return redirect(url_for("login"))


@app.route("/dashboard/<int:guild_id>/settings", methods=['POST', 'GET'])
async def settings(guild_id):
    try:
        user = await discord_o.fetch_user()
        if await check_perms(user.id, guild_id) or await control(guild_id):
            if not await discord_o.authorized:
                return redirect(url_for("login"))
            if request.args.get("setting") == "commands":
                cursor.execute("CREATE TABLE IF NOT EXISTS command_perms(role_id, guild_id, command_name, state)")

                async def get_roles(guild_id):
                    guild = my_bot.get_guild(guild_id)
                    if guild is None:
                        return None
                    roles_ = await guild.fetch_roles()
                    roles_dict = {
                        "role_id": [],
                        "role_name": []
                    }
                    for role in roles_:
                        roles_dict['role_id'].append(role.id)
                        roles_dict['role_name'].append(role.name)
                    return roles_dict

                async def get_commands(guild_id):
                    guild = await my_bot.fetch_guild(guild_id)
                    if guild is None:
                        return None
                    commands_dict = {
                        "command": [],
                        "command_name": []
                    }
                    for command in my_bot.tree.get_commands():
                        commands_dict['command'].append(command.name)
                        commands_dict['command_name'].append(command.name)
                    return commands_dict

                bot_commands = await get_commands(guild_id)
                roles = await get_roles(guild_id)
                if (await request.form).get('role') is not None and (await request.form).get('command') is not None:
                    perms_list = [(await request.form).get('role'), guild_id, (await request.form).get('command'), True]
                    cursor.execute("INSERT INTO command_perms VALUES (?, ?, ?, ?)", perms_list)
                    connect.commit()
                res1 = cursor.execute(f"SELECT role_id FROM command_perms WHERE guild_id={str(guild_id)}")
                role_ids = res1.fetchall()
                res2 = cursor.execute(f"SELECT command_name FROM command_perms WHERE guild_id={str(guild_id)}")
                command_names = res2.fetchall()
                res3 = cursor.execute(f"SELECT state FROM command_perms WHERE guild_id={str(guild_id)}")
                states = res3.fetchall()
                roles_dict = {
                    "role_id": [],
                    "command_name": [],
                    "state": []
                }
                if (await request.form).get('role_remove') is not None and (await request.form).get(
                        'command_remove') is not None:
                    remove_list = [(await request.form).get('role_remove'), guild_id,
                                   (await request.form).get('command_remove')]
                    cursor.execute("DELETE FROM command_perms WHERE role_id=(?) AND guild_id=(?) AND command_name=(?)",
                                   remove_list)
                    connect.commit()

                async def get_role_name(role_id, guild_id):
                    guild = await my_bot.fetch_guild(guild_id)
                    if role_id is not None:
                        return (guild.get_role(int(role_id))).name

                for i in range(0, len(states)):
                    if re.sub("[()',]", "", str(role_ids[i])) not in roles_dict["role_id"]:
                        roles_dict["role_id"].append(re.sub("[()',]", "", str(role_ids[i])))
                        roles_dict["command_name"].append(re.sub("[()',]", "", str(command_names[i])))
                        roles_dict["state"].append(re.sub("[()',]", "", str(states[i])))

                def length(a):
                    return len(a)

                def get_role_commands(role_id):
                    role = str(role_id)
                    result = (cursor.execute(f"SELECT command_name FROM command_perms WHERE role_id=(?) AND state=(?)",
                                             [role, 1])).fetchall()
                    final_list = []
                    for k in range(0, len(result)):
                        final_list.append(re.sub("[()',]", "", str(result[k])))
                    return final_list

                return await render_template("settings.html",
                                             domain=DOMAIN,
                                             guild_id=guild_id,
                                             length_role=len(roles['role_name']),
                                             roles=roles,
                                             length_commands=len(bot_commands['command']),
                                             bot_commands=bot_commands,
                                             role_name=get_role_name,
                                             roles_perms=roles_dict,
                                             role_commands=get_role_commands,
                                             len=length
                                             )
            elif request.args.get("setting") == "tickets":
                cursor.execute("CREATE TABLE IF NOT EXISTS ticket_perms(role_id, guild_id)")
                cursor.execute("CREATE TABLE IF NOT EXISTS ticket_settings(setting, guild_id, value)")
                cursor.execute("CREATE TABLE IF NOT EXISTS modal_settings(guild_id, field_no, text, placeholder, type, max_length, required)")
                cursor.execute("CREATE TABLE IF NOT EXISTS additional_modal_settings(guild_id, form_title, ticket_message_title, ticket_message_desc, ticket_footer_text, name_field)")
                async def get_roles(guild_id):
                    guild = my_bot.get_guild(guild_id)
                    if guild is None:
                        return None
                    roles_ = await guild.fetch_roles()
                    roles_dict = {
                        "role_id": [],
                        "role_name": []
                    }
                    for role in roles_:
                        roles_dict['role_id'].append(role.id)
                        roles_dict['role_name'].append(role.name)
                    return roles_dict

                async def get_channels(guild_id):
                    guild = my_bot.get_guild(guild_id)
                    if guild is None:
                        return None
                    channel_dict = {
                        'channel_name': [],
                        'channel_id': []
                    }
                    for channel in guild.channels:
                        if str(channel.type) == 'text':
                            channel_dict["channel_name"].append(channel.name)
                            channel_dict["channel_id"].append(channel.id)
                    return channel_dict
                async def get_post_many(names):
                    final_list = []
                    for i in range(0, len(names)):
                        final_list.append((await request.form).get(names[i]))
                        control_list = []
                        control_list.append(None)
                        if final_list == control_list:
                            return None
                    else:
                        return final_list
                def save_modal_sets(data):
                    if data[2] != '' and data[2] is not None:
                        cursor.execute("INSERT INTO modal_settings VALUES (?, ?, ?, ?, ?, ?, ?)", data)
                        connect.commit()
                    else:
                        cursor.execute("DELETE FROM modal_settings WHERE guild_id=(?) AND field_no=(?) AND text=(?) AND placeholder=(?) AND type=(?) AND max_length=(?) AND required=(?)", data)
                        connect.commit()
                def save_form_sets(data):
                    if (data[1] != '' and data[1] is not None) or data[2] != '0' or (data[3] != '' and data[3] is not None) or (data[4] != '' and data[4] is not None) or (data[5] != '' and data[5] is not None):
                        cursor.execute("INSERT INTO additional_modal_settings VALUES (?, ?, ?, ?, ?, ?)", data)
                        connect.commit()
                    else:
                        cursor.execute("DELETE FROM additional_modal_settings WHERE guild_id=(?) AND form_title=(?) AND ticket_message_title=(?) AND ticket_message_desc=(?) AND ticket_footer_text=(?) AND name_field=(?)", data)
                        connect.commit()
                questions = [f[0] for f in (cursor.execute("SELECT text FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
                placeholders = [f[0] for f in (cursor.execute("SELECT placeholder FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
                types = [f[0] for f in (cursor.execute("SELECT type FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
                lengths = [f[0] for f in (cursor.execute("SELECT max_length FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
                require = [f[0] for f in (cursor.execute("SELECT required FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
                additional_modal_settings = (cursor.execute("SELECT * FROM additional_modal_settings WHERE guild_id=(?)", [guild_id])).fetchone()
                if additional_modal_settings is None:
                    additional_modal_settings = ['', '', '', '', '', '']
                else:
                    additional_modal_settings = list(additional_modal_settings)
                channels = await get_channels(guild_id)
                roles = await get_roles(guild_id)
                if (await request.form).get('role') is not None:
                    perms_list = [(await request.form).get('role'), guild_id]
                    cursor.execute("INSERT INTO ticket_perms VALUES (?, ?)", perms_list)
                    connect.commit()
                modal_sets = await get_post_many(['fields',
                                                  'field1_q', 'field1_ph', 'field1_t', 'field1_ml', 'field1_r',
                                                  'field2_q', 'field2_ph', 'field2_t', 'field2_ml', 'field2_r',
                                                  'field3_q', 'field3_ph', 'field3_t', 'field3_ml', 'field3_r',
                                                  'field4_q', 'field4_ph', 'field4_t', 'field4_ml', 'field4_r',
                                                  'field5_q', 'field5_ph', 'field5_t', 'field5_ml', 'field5_r',
                                                  ])
                form_sets = await get_post_many(['form_title', 'ticket_message_title', 'ticket_message_desc', 'ticket_footer', 'name_field'])
                if form_sets is not None:
                    cursor.execute(f"DELETE FROM additional_modal_settings WHERE guild_id=(?)", [guild_id])
                    connect.commit()
                    save_form_sets([guild_id, form_sets[0], form_sets[1], form_sets[2], form_sets[3], form_sets[4]])

                if modal_sets is not None:
                    cursor.execute(f"DELETE FROM modal_settings WHERE guild_id=(?)", [guild_id])
                    connect.commit()
                    for i in range(0, int(modal_sets[0])):
                        required = 'off'
                        if modal_sets[5*i+5] == 'on':
                            required = 'on'
                        save_modal_sets([guild_id, i+1, modal_sets[5*i+1], modal_sets[5*i+2], modal_sets[5*i+3], modal_sets[5*i+4], required])
                fields_val = len(questions)
                if fields_val == 0:
                    fields_val = 1
                if (await request.form).get('recruit_role') is not None or (await request.form).get(
                        'pvt_role') is not None or (await request.form).get('message') is not None or (
                await request.form).get('log_channel') is not None:
                    cursor.execute(f"DELETE FROM ticket_settings WHERE guild_id=(?)", [str(guild_id)])
                    connect.commit()
                    if (await request.form).get('recruit_role') is not None:
                        settings_list = ["recruit_role", str(guild_id), (await request.form).get('recruit_role')]
                        cursor.execute("INSERT INTO ticket_settings VALUES (?, ?, ?)", settings_list)
                        connect.commit()
                    if (await request.form).get('pvt_role') is not None:
                        settings_list = ["pvt_role", str(guild_id), (await request.form).get('pvt_role')]
                        cursor.execute("INSERT INTO ticket_settings VALUES (?, ?, ?)", settings_list)
                        connect.commit()
                    if (await request.form).get('log_channel') is not None:
                        settings_list = ["log_channel", str(guild_id), (await request.form).get('log_channel')]
                        cursor.execute("INSERT INTO ticket_settings VALUES (?, ?, ?)", settings_list)
                        connect.commit()
                    if (await request.form).get('message') is not None:
                        settings_list = ["message", str(guild_id), (await request.form).get('message')]
                        cursor.execute("INSERT INTO ticket_settings VALUES (?, ?, ?)", settings_list)
                        connect.commit()

                res1 = cursor.execute(f"SELECT role_id FROM ticket_perms WHERE guild_id={str(guild_id)}")
                role_ids = res1.fetchall()
                roles_dict = {
                    "role_id": [],
                }
                if (await request.form).get('role_remove') is not None:
                    remove_list = [(await request.form).get('role_remove'), guild_id]
                    cursor.execute("DELETE FROM ticket_perms WHERE role_id=(?) AND guild_id=(?)", remove_list)
                    connect.commit()

                async def get_role_name(role_id, guild_id):
                    guild = await my_bot.fetch_guild(guild_id)
                    if role_id is not None:
                        return (guild.get_role(int(role_id))).name

                def length(a):
                    return len(a)

                def string(a):
                    return str(a)

                for i in range(0, len(role_ids)):
                    if re.sub("[()',]", "", str(role_ids[i])) not in roles_dict["role_id"]:
                        roles_dict["role_id"].append(re.sub("[()',]", "", str(role_ids[i])))
                recruit_id = None
                pvt_id = None
                message = None
                log_channel = None
                try:
                    recruit_id = re.sub("[)(',]", "", str(cursor.execute(
                        "SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='recruit_role'",
                        [str(guild_id)]).fetchone()[0]))
                    pvt_id = re.sub("[)(',]", "", str(
                        cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='pvt_role'",
                                       [str(guild_id)]).fetchone()[0]))
                    log_channel = re.sub("[)(',]", "", str(
                        cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='log_channel'",
                                       [str(guild_id)]).fetchone()[0]))
                    message = re.sub("[()',]", "", str(
                        cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='message'",
                                       [str(guild_id)]).fetchone()[0]))
                except:
                    pass
                return await render_template("tickets.html",
                                             domain=DOMAIN,
                                             guild_id=guild_id,
                                             roles=roles,
                                             role_name=get_role_name,
                                             roles_dict=roles_dict,
                                             channels=channels,
                                             len=length,
                                             recruit_id=recruit_id,
                                             pvt_id=pvt_id,
                                             log_channel=log_channel,
                                             message=message,
                                             str=string,
                                             fields_val=fields_val,
                                             questions=questions,
                                             placeholders=placeholders,
                                             types=types,
                                             lengths=lengths,
                                             require=require,
                                             int=int,
                                             modal_sets=additional_modal_settings
                                             )
            else:
                user_id = (await request.form).get('user_id')
                guild = await my_bot.fetch_guild(guild_id)
                if user_id is not None:
                    try:
                        name = (await guild.fetch_member(user_id)).display_name
                    except:
                        name = user_id
                    user_list = [user_id, guild_id, name]
                    log_list = [(await discord_o.fetch_user()).id, guild_id, 1, user_id, round(time.time())]
                    cursor.execute(f"INSERT INTO ids (id, guild_id, name) VALUES (?, ?, ?)", user_list)
                    connect.commit()
                    cursor.execute(f"INSERT INTO logs (user_id, guild_id, action, link, time) VALUES (?, ?, ?, ?, ?)",
                                   log_list)
                    connect.commit()
                length = len((cursor.execute(f"SELECT id FROM ids")).fetchall())
                length_for = len((cursor.execute(f"SELECT id FROM ids WHERE guild_id='{guild_id}'")).fetchall())
                users = {
                    "id": [],
                    "guild": [],
                    "name": []
                }
                res1 = cursor.execute("SELECT id FROM ids")
                ids = res1.fetchall()
                res2 = cursor.execute("SELECT guild_id FROM ids")
                guilds = res2.fetchall()
                res3 = cursor.execute("SELECT name FROM ids")
                names = res3.fetchall()
                for i in range(0, length):
                    if str(guild_id) == re.sub("[()',]", "", str(guilds[i])):
                        users['id'].append(re.sub("[()',]", "", str(ids[i])))
                        users['guild'].append(re.sub("[()',]", "", str(guilds[i])))
                        users['name'].append(re.sub("[()',]", "", str(names[i])))
                user_form = (await request.form).get('user')
                if user_form is not None:
                    log_list = [(await discord_o.fetch_user()).id, guild_id, 2, user_form, round(time.time())]
                    cursor.execute(f"DELETE FROM ids WHERE id='{user_form}' AND guild_id='{guild_id}'")
                    connect.commit()
                    cursor.execute(f"INSERT INTO logs (user_id, guild_id, action, link, time) VALUES (?, ?, ?, ?, ?)",
                                   log_list)
                    connect.commit()

                return await render_template("perms.html", length=length_for, users=users, guild_id=guild_id,
                                             domain=DOMAIN)
        else:
            return redirect(url_for("dashboard"))
    except Unauthorized:
        return redirect(url_for("login"))

async def check_command_perm(interaction: discord.Interaction):
    command = interaction.command
    guild_id = str(interaction.guild.id)
    res1 = cursor.execute(f"SELECT role_id FROM command_perms WHERE guild_id={guild_id}")
    role_ids = res1.fetchall()
    res2 = cursor.execute(f"SELECT guild_id FROM command_perms WHERE guild_id={guild_id}")
    guilds = res2.fetchall()
    res3 = cursor.execute(f"SELECT command_name FROM command_perms WHERE guild_id={guild_id}")
    command_names = res3.fetchall()
    res4 = cursor.execute(f"SELECT state FROM command_perms WHERE guild_id={guild_id}",)
    states = res4.fetchall()
    perms_dict = {
        "role_id": [],
        "guild_ids": [],
        "command_names": [],
        "states": []
    }
    guild = interaction.guild
    if role_ids != []:
        for i in range(0, len(states)):
            perms_dict["role_id"].append(re.sub("[()',]", "", str(role_ids[i])))
            perms_dict["guild_ids"].append(re.sub("[()',]", "", str(guilds[i])))
            perms_dict["command_names"].append(re.sub("[()',]", "", str(command_names[i])))
            perms_dict["states"].append(re.sub("[()',]", "", str(states[i])))
        for k in range(0, len(states)):
            if guild.get_role(int(perms_dict["role_id"][k])) in interaction.user.roles and perms_dict["states"][k] == '1' and command.name == perms_dict["command_names"][k]:
                return True
            elif interaction.user.guild_permissions.administrator:
                return True
    else:
        return False


class send(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Подать заявку", style=discord.ButtonStyle.gray, custom_id='persistent_view:send', emoji='📨')
    async def action(self, interaction : discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_modal(form(interaction))


class controls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=" Принять", style=discord.ButtonStyle.success, custom_id='persistent:accept', emoji='✅')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        recruit_id = guild.default_role.id
        pvt_id = guild.default_role.id
        try:
            recruit_id = re.sub("[)(',]", "", str(cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='recruit_role'",[str(guild.id)]).fetchone()[0]))
            pvt_id = re.sub("[)(',]", "", str(cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='pvt_role'",[str(guild.id)]).fetchone()[0]))
        except:
            pass
        role_list = []
        try:
            role_list = (cursor.execute("SELECT role_id FROM ticket_perms WHERE guild_id=(?)", [guild.id])).fetchall()
        except:
            pass
        final_list = []
        for i in range(0, len(role_list)):
            final_list.append(re.sub("[)(',]", "", str(role_list[i])))
        for role in interaction.user.roles:
            if str(role.id) in final_list or role.permissions.administrator or interaction.user.guild_permissions.administrator:
                log_channel = guild.channels[0].id
                try:
                    log_channel = int(re.sub("[)(',]", "", str(cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='log_channel'",[str(guild.id)]).fetchone()[0])))
                except:
                    pass
                channel_log = await guild.fetch_channel(log_channel)
                messages = [message async for message in interaction.channel.history(limit=1, oldest_first=True)]
                await channel_log.send("# ✅Принят", embed=messages[0].embeds[0].copy())
                role_rec = guild.get_role(int(recruit_id))
                for member in role_rec.members:
                    if member in interaction.channel.members:
                        await member.remove_roles(guild.get_role(int(recruit_id)))
                        await member.add_roles(guild.get_role(int(pvt_id)))
                return await interaction.channel.delete()

    @discord.ui.button(label=" Отклонить", style=discord.ButtonStyle.red, custom_id='persistent:decline', emoji='⛔')
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        recruit_id = guild.default_role.id
        try:
            recruit_id = re.sub("[)(',]", "", str(cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='recruit_role'",[str(guild.id)]).fetchone()[0]))
        except:
            pass
        role_list = []
        try:
            role_list = (cursor.execute("SELECT role_id FROM ticket_perms WHERE guild_id=(?)", [guild.id])).fetchall()
        except:
            pass
        final_list = []
        for i in range(0, len(role_list)):
            final_list.append(re.sub("[)(',]", "", str(role_list[i])))
        for role in interaction.user.roles:
            if str(role.id) in final_list or role.permissions.administrator or interaction.user.guild_permissions.administrator:
                log_channel = guild.channels[0].id
                try:
                    log_channel = int(re.sub("[)(',]", "", str(cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='log_channel'",[str(guild.id)]).fetchone()[0])))
                except:
                    pass
                channel_log = await guild.fetch_channel(log_channel)
                messages = [message async for message in interaction.channel.history(limit=1, oldest_first=True)]
                await channel_log.send("# ⛔Отклонен", embed=messages[0].embeds[0].copy())
                role_rec = guild.get_role(int(recruit_id))
                for member in role_rec.members:
                    if member in interaction.channel.members:
                        await member.remove_roles(guild.get_role(int(recruit_id)))
                return await interaction.channel.delete()


class form(discord.ui.Modal):
    def __init__(self, interaction: discord.Interaction):
        title = (cursor.execute("SELECT * FROM additional_modal_settings WHERE guild_id=(?)", [interaction.guild.id])).fetchone()
        if title is None:
            title = 'Форма'
        else:
            title = (list(title))[1]
        super().__init__(title=title)
        guild_id = interaction.guild.id
        questions = [f[0] for f in (cursor.execute("SELECT text FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
        placeholders = [f[0] for f in (cursor.execute("SELECT placeholder FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
        types = [f[0] for f in (cursor.execute("SELECT type FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
        lengths = [f[0] for f in (cursor.execute("SELECT max_length FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]
        require = [f[0] for f in (cursor.execute("SELECT required FROM modal_settings WHERE guild_id=(?)", [guild_id])).fetchall()]

        for i in range(0, len(questions)):
            style = discord.TextStyle.short
            if types[i] == "long":
                style = discord.TextStyle.long
            required = False
            if require[i] == 'on':
                required = True
            length = lengths[i]
            if lengths[i] == '':
                length = '2000'
            item = ui.TextInput(
                label=questions[i],
                style=style,
                placeholder=placeholders[i],
                required=required,
                max_length=int(length)
            )
            self.add_item(item)
        if len(questions) == 0:
            item = ui.TextInput(label='Пожалуйста, настройте тикет в панели')
            self.add_item(item)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            guild = interaction.guild
            member = interaction.user
            username = interaction.user.name
            result = ''.join(re.findall('[a-z]', username))
            if result == "": result = "0"
            ticket = utils.get(interaction.guild.text_channels, name=f"ticket-{result}")
            if ticket is not None:
                await interaction.response.send_message(f"Вы уже открывали тикет: {ticket.mention}", ephemeral=True)
            else:
                channel = await guild.create_text_channel(
                    f"ticket-{result}"
                )
                role_list = (
                    cursor.execute("SELECT role_id FROM ticket_perms WHERE guild_id=(?)", [guild.id])).fetchall()
                final_list = []
                for i in range(0, len(role_list)):
                    final_list.append(re.sub("[)(',]", "", str(role_list[i])))
                await channel.set_permissions(guild.roles[0], read_messages=False)
                await channel.set_permissions(member, read_messages=True)
                for i in range(0, len(final_list)):
                    await channel.set_permissions(guild.get_role(int(final_list[i])), read_messages=True)
                await interaction.response.send_message(f"Тикет открыт!", ephemeral=True)
                embed = discord.Embed(title="Результаты заполнения анкеты", color=discord.Color.blue())
                for i in range(0, len(self.children)):
                    if self.children[i].value != '' and self.children[i].value is not None:
                        embed.add_field(name=f"{self.children[i].label}", value=f"```{self.children[i].value}```", inline=False)
                embed.set_author(name=member.display_name, icon_url=interaction.user.display_avatar.url)
                message = (cursor.execute("SELECT value FROM ticket_settings WHERE guild_id=(?) AND setting='message'", [str(guild.id)])).fetchone()
                if message is None:
                    message = ''
                else:
                    message = list(message)[0]
                await channel.send(f"{message}", embed=embed, view=controls())
                try:
                    additional_modal_settings = (cursor.execute("SELECT * FROM additional_modal_settings WHERE guild_id=(?)",[guild.id])).fetchone()
                    if additional_modal_settings is None:
                        additional_modal_settings = ['', '', '', '', '', '0']
                    else:
                        additional_modal_settings = list(additional_modal_settings)
                    if additional_modal_settings[5] != '0' and additional_modal_settings[5] != '':
                        nick = f"{self.children[int(additional_modal_settings[5])].value}"
                        await member.edit(nick=nick)
                except discord.errors.Forbidden:
                    pass
        except discord.errors.NotFound:
            pass



@my_bot.tree.command(name="help", description="Список комманд бота")
async def help(interaction: discord.Interaction):
    member = interaction.user
    embed_ticket = Embed(
        title="/ticket",
        description='Комманда, отправляющая в канал в котором была использована сообщение для открытия тикета на всупление. Комманда с огрниченным использованием, доступ только у роли "Техник"'
    )
    embed_ticket.set_image(url='https://cdn.discordapp.com/attachments/879360204448362496/1123712002829852832/image.png')
    embed_farm = Embed(
        title='/farm┃x:"?"┃y:"?"┃ z:"?"┃title:"Название фермы"┃desc:"Описание фермы"┃pic:"Ссылка на картинку -',
        description='Комманда для создание поста про ферму. Комманда с огрниченным использованием, доступ только у роли "Комиссар снабжения"'
    )
    embed_farm.set_image(url='https://cdn.discordapp.com/attachments/879360204448362496/1123712888373260391/image.png')
    embed_next = Embed(
        title='/next',
        description='Комманда для отправки условий второго этапа отборо в градострой. Комманда с огрниченным использованием, доступ только у роли "Комиссар градостроя"'
    )
    embed_film = Embed(
        title='/film┃name:"Название фильма"┃time:"Время(указывайте время по мск в формате XX:XX)"┃link:"Ссылка на комнату совместного просмотра"',
        description='Вам нужно указать название фильма для поиска, после этого вам будет предложено 5 вариантов фильмов из которых вы можете выбрать нужный вам. Вся остальная информация по типу рейтинга описания и времени, будет добавлена автоматически. Доступ к комманде имеют все комиссары и роли выше\nПример, как это выглядит:'
    )
    embed_film.set_image(url='https://cdn.discordapp.com/attachments/879360204448362496/1123750701915455518/image.png')
    embed_ping = Embed(
        title='/пинг',
        description='Комманда, с помощью которой можно узнать доступен ли бот'
    )
    await interaction.response.send_message('Список комманд отправлен вам в ЛС', ephemeral=True)
    await member.send(embeds=(embed_ping, embed_film, embed_next, embed_farm, embed_ticket))


@my_bot.tree.command(name="пинг", description="Комманда проверки доступности бота")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Бот доступен', ephemeral=True)


@my_bot.tree.command(name="ticket", description="Создание сообщения для открытия тикета на вступление")
@app_commands.check(check_command_perm)
async def ticket(interaction: discord.Interaction):
    additional_modal_settings = (cursor.execute("SELECT * FROM additional_modal_settings WHERE guild_id=(?)", [interaction.guild.id])).fetchone()
    if additional_modal_settings is None:
        additional_modal_settings = ['', '', '', '', '', '']
    else:
        additional_modal_settings = list(additional_modal_settings)
    title = additional_modal_settings[2]
    if title == '' or title is None:
        title = 'Открыть тикет'
    desc = additional_modal_settings[3]
    if desc == '' or desc is None:
        desc = 'Вы можете открыть тикет нажав кнопку ниже'
    embed = discord.Embed(
        title=title,
        description=desc,
        color=discord.Color.blue()
    )
    footer = additional_modal_settings[4]
    if footer == '' or footer is None:
        embed.set_footer(icon_url=my_bot.user.display_avatar.url, text='Гуляй Поле - Бот')
    else:
        embed.set_footer(icon_url=my_bot.user.display_avatar.url, text=footer)
    await interaction.response.send_message('отправлено', ephemeral=True)
    await interaction.channel.send(embed=embed, view=send())


@ticket.error
async def ticket_error(interaction: discord.Interaction, error):
    print(f"{interaction.user.display_name} лезет куда не надо на сервере {interaction.guild.name} используя {interaction.command.name}")
    await interaction.response.send_message("Нет доступа", ephemeral=True)


@my_bot.tree.command(name="farm", description="Комманда для создания постов о фермах")
@app_commands.check(check_command_perm)
async def farm(
        interaction: discord.Interaction,
        x: int,
        y: int,
        z: int,
        title: str = None,
        desc: str = None,
        pic: str = None
):
    class accept(discord.ui.View):

        @discord.ui.button(label="Отправить", style=discord.ButtonStyle.success)
        async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!" , ephemeral=True)
            await interaction.channel.send(embed=embed)
    view = accept()
    guild = interaction.guild
    member = interaction.user
    embed = discord.Embed(title=title, color=discord.Color.blue())
    embed.set_author(name=member.display_name, icon_url=interaction.user.display_avatar.url)
    if desc is None:
        desc = ""
    embed.add_field(name=f"Координаты: {x}, {y}, {z}.", value=desc, inline=False)
    embed.set_image(url=pic)

    await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


@farm.error
async def farm_error(interaction: discord.Interaction, error):
    print(f"{interaction.user.display_name} лезет куда не надо на сервере {interaction.guild.name} используя {interaction.command.name}")
    await interaction.response.send_message("Нет доступа", ephemeral=True)


@my_bot.tree.command(name="next", description="Комманда, отправляющая второй этап отбора в градострой")
@app_commands.check(check_command_perm)
async def next(interaction: discord.Interaction):
    text = """<@&1110678038938648747>
Поздравляю с прохождением первого этапа! Далее у нас - второй, пожалуй самый интригующий: проверка навыков. 
Задание: построить 3 здания в креативе. Они не обязаны быть большого размера, но должны быть хоть как-то детализированы. Мир используем плоский.
Стилистика зданий: 
1. Пустынное (актуально, как стиль будущего города)
2. Средневековое
3. Свободный стиль. Просто нужно что-то от себя, как тебе удобно и нравится. 
Правила: 
1. на постройку дается 6 дней (то есть, 2 дня на каждое здание. Можешь присылать мне в лс по мере готовности, а можешь и под конец дедлайна всем скопом)
2. Запрещено использование Лайтматики и других строительных модов со схемами. Все делаем с нуля. 
3. Запрещено копировать здания по фотографиям. Я разрешаю подсмотреть примеры зданий нужной стилистики, но только для того, чтобы легче было придумать свое не отходя от канонов.
4. Запрещено строить по видео-туториалам. Найду - выкину из градостроения за фальсификацию. Разрешено смотреть туториалы декора, типо крыши или пола, но не самих зданий. 
5. Работать только в одиночном мире. Просить помощи у друзей, знакомых, других участников отбора, людей из других кланов - запрещено. 

Критерии отбора не настолько строгие, как кажется. главное - делай все сам и не пытайся схитрить. 

(Готовые здания отправляй скриншотами со всех сторон. Также, стоит украсить здание изнутри. Если хочешь более детально показать свои работы, мы можем договориться о звонке с демонстрацией экрана.)"""
    await interaction.response.send_message(text)


@next.error
async def next_error(interaction: discord.Interaction, error):
    print(f"{interaction.user.display_name} лезет куда не надо на сервере {interaction.guild.name} используя {interaction.command.name}")
    await interaction.response.send_message("Нет доступа", ephemeral=True)


@my_bot.tree.command(name="film", description="Комманда для создания поста о фильме")
@app_commands.check(check_command_perm)
async def film(interaction: discord.Interaction, name: str, time: str, link: str):

    async def embed_send(num : int, interaction: discord.Interaction, data):
        title = data["docs"][num]['names'][0]
        embed = discord.Embed(title=f'Смотрим фильм {title} в {time} по МСК!', color=discord.Color.blue())
        embed.add_field(name=data["docs"][num]['names'][0], value=data["docs"][num]['description'], inline=False)
        embed.set_thumbnail(url=data["docs"][num]['poster'])
        n = data["docs"][num]['movieLength']
        rate = round(data["docs"][num]['rating'], 1)
        hours = n // 60
        minutes = n % 60
        length = "%02d:%02d:00" % (hours, minutes)
        embed.set_footer(text=f'Длительность: {length}, Рейтинг: {rate}')
        embed.set_author(name=member.display_name, icon_url=interaction.user.display_avatar.url)
        return await interaction.channel.send(f'<@&1118974579625435149>\n# {link}', embed=embed)

    class accept(discord.ui.View):

        @discord.ui.button(label="1", style=discord.ButtonStyle.success)
        async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!", ephemeral=True)
            num = 0
            await embed_send(num, interaction, data)

        @discord.ui.button(label="2", style=discord.ButtonStyle.success)
        async def send1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!", ephemeral=True)
            num = 1
            await embed_send(num, interaction, data)

        @discord.ui.button(label="3", style=discord.ButtonStyle.success)
        async def send2(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!", ephemeral=True)
            num = 2
            await embed_send(num, interaction, data)

        @discord.ui.button(label="4", style=discord.ButtonStyle.success)
        async def send3(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!", ephemeral=True)
            num = 3
            await embed_send(num, interaction, data)

        @discord.ui.button(label="5", style=discord.ButtonStyle.success)
        async def send4(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Опубликовано!", ephemeral=True)
            num = 4
            await embed_send(num, interaction, data)

    view = accept()
    api = os.getenv('API_KEY')
    url = f"https://api.kinopoisk.dev/v1.2/movie/search?page=1&limit=5&query={name}&token={api}"
    member = interaction.user

    response = requests.get(url)
    data = json.loads(response.text)
    msg = f""""""
    for i in range(0, 5):
        desc = data["docs"][i]['names'][0]
        year = data['docs'][i]['year']
        id = data['docs'][i]['id']
        msg += f"{i}. {desc}({year}) id:{id}\n"

    await interaction.response.send_message(msg, ephemeral=True, view=view)


@film.error
async def film_error(interaction: discord.Interaction, error):
    print(f"{interaction.user.display_name} лезет куда не надо на сервере {interaction.guild.name} используя {interaction.command.name}")
    await interaction.response.send_message("Нет доступа", ephemeral=True)

for guild in my_bot.guilds:
    my_bot.tree.copy_global_to(guild=discord.Object(id=guild.id))

my_bot.run(TOKEN)
