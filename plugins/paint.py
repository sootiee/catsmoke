from discord.ext import commands
import re
import json
import os

class ColorFlags(commands.FlagConverter):
    color: str = commands.flag(description="Color you wish to have as a role")

class Paint(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        
        # Set up database
        if not os.path.isfile("db.json"):
            with open('db.json', 'w') as json_file:
                init = {"colors": []}
                json.dump(init, json_file)

        with open('db.json') as json_file:
            self.parsed = json.load(json_file)
    
    def is_color(self, color):
        reg = re.compile(self.COLOR_REGEX)
        check = reg.fullmatch(color)
        return check

    def write_json(self):
        with open("db.json", "w") as json_file:
            json.dump(self.parsed, json_file)
    
    @commands.hybrid_command(name="paint")
    async def paint(self, ctx, *, flags: ColorFlags):
        if not self.is_color(flags.color):
            await ctx.send("Invalid hex color")
            return 
        
        if len(flags.color) == 4:
            hex_code = '#{}'.format(''.join(2 * c for c in flags.color.lstrip('#')))
        else:
            hex_code = flags.color

        for x in self.parsed["colors"]:
            if ctx.author.id == x["user_id"] and ctx.guild.id == x["guild_id"]:
                role = ctx.guild.get_role(x["role_id"])
                
                if role != None:
                    await ctx.send("Role does not exist")
                    return
                
                await role.edit(color = int(hex_code[1:], 16), name = hex_code.upper())
                x["hex"] = hex_code
                self.write_json()
                await ctx.send("Successfully updated user color")
                return
                    
        role =  await ctx.guild.create_role(color = int(hex_code[1:], 16), name = hex_code.upper())
        await ctx.author.add_roles(role)
        self.parsed["colors"].append({"user_id": ctx.author.id, "hex": hex_code, "role_id": role.id, "guild_id": ctx.guild.id})
        self.write_json()
        await ctx.send("Added role color to you")

async def setup(bot):
    await bot.add_cog(Paint(bot))