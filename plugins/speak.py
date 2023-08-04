from discord.ext import commands

# command: speak
# args: none
# Sends a simple message via Discord
class Speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def speak(self, ctx):
        await ctx.send('It\'s a dog eat dog world out there...')

async def setup(bot):
    await bot.add_cog(Speak(bot))