from discord.ext import commands

# command: speak
# args: none
# Sends a simple message via Discord
class Speak(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.hybrid_command()
    async def speak(ctx):
        await ctx.send('It\'s a dog eat dog world out there...')

def setup(bot):
    bot.add_cog(Speak(bot))