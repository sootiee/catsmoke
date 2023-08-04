import discord
from discord.ext import commands
import re
import json
import os


token = os.environ['TOKEN']
owner_id = os.environ['OWNER']
prefix = "%%"
color_regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'



if not os.path.isfile("db.json"):
    with open('db.json', 'w') as json_file:
        init = {"colors": []}
        json.dump(init, json_file)

with open('db.json') as json_file:
  parsed = json.load(json_file)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


def is_color(color):
    reg = re.compile(color_regex)
    check = reg.fullmatch(color)
    return check

def write_json():
    with open("db.json", "w") as json_file:
        json.dump(parsed, json_file)

class ColorFlags(commands.FlagConverter):
    color: str = commands.flag(description="Color you wish to have as a role")

@bot.event
async def on_message(message):
    if message.author.id == int(owner_id):
        if message.content == prefix + "update":
            await bot.tree.sync()
            print("updated command list")

@bot.hybrid_command()
async def set_color(ctx, *, flags: ColorFlags):
    if is_color(flags.color):
        if len(flags.color) == 4:
            hex_code = '#{}'.format(''.join(2 * c for c in flags.color.lstrip('#')))
        else:
            hex_code = flags.color


        for x in parsed["colors"]:
            if ctx.author.id == x["user_id"] and ctx.guild.id == x["guild_id"]:
                role = ctx.guild.get_role(x["role_id"])
                if role != None:
                    await role.edit(color = int(hex_code[1:], 16), name = hex_code.upper())
                    x["hex"] = hex_code
                    write_json()
                    await ctx.send("Successfully updated user color")
                    return
                else:
                    ctx.send("Role does not exist")
                    return

        role =  await ctx.guild.create_role(color = int(hex_code[1:], 16), name = hex_code.upper())
        await ctx.author.add_roles(role)
        parsed["colors"].append({"user_id": ctx.author.id, "hex": hex_code, "role_id": role.id, "guild_id": ctx.guild.id})
        write_json()
        await ctx.send("Added role color to you")

    else:
        await ctx.send("Invalid hex color")



bot.run(token)
