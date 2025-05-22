# This example requires the 'message_content' intent.
import discord
from discord.errors import NotFound
import os
from discord import app_commands, Interaction
from discord.ext import commands
from typing import Optional
from data import *
from groq import Groq

#in case your bot is facing any error, I have reset my secret key to resolve it. Here is the website: https://discord.com/developers/applications/1057651836011692113/bot , click on reset token to get the new secret key.

MY_SECRET = os.getenv("SECRET_KEY")
MY_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=MY_API_KEY, )
##### DATAS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is ready, ho gaya")


@bot.tree.command(name="help",
                  description="Get information about available commands")
@app_commands.describe(parts="Details about any one part among 22 parts",
                       articleinfo="Details of any individual article")
async def help(interaction: Interaction,
               parts: Optional[int] = None,
               articleinfo: Optional[str] = None):

    if parts is None and articleinfo is None:
        await interaction.response.send_message(
            '''### 📜 Constitution of India Overview:
- Contains 395 articles in 22 parts.
- Includes 12 schedules.

🚀 **Usage:**
- Type `/help <part number>` for information on a specific part.
- Type `/help <article number>` for information on a specific article.
- Use any negative number or a number greater than 22 in part number or number greater than 395 in article number to get the complete list.

📚 **Examples:**
- `/help parts 5` - Get more info about Part V.
- `/help parts -1` - Receive a complete list of the Constitution.
- `/help articleinfo 12` - Get more info about article 12.

🌐 **Explore and Learn!**
''')

    elif parts is not None and parts >= 0 and parts < 23:
        tag = details_parts[parts]["tags"]
        prompt = details_parts[parts]["Title"]
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role":
                    "user",
                    "content":
                    f"You are a wise person on Indian constituion. You have to give very concise response exact 2 sentence within 60 words(remember word count) Also give some emojis if needed to make attractive\n{prompt}",
                }],
                model="llama3-8b-8192",
            )

            extra = response.choices[0].message.content

        except NotFound:
            extra = details_parts[parts]['details']
            

        info = f"\nTo know the details of {details_parts[parts]['Title']}, visit here https://www.clearias.com/constitution-of-india/{tag}" + " 🚀✨"
        articles = "\n\n📰🔍 *Included articles under this part:* **" + details_parts[
            parts]["article"] + "** \n\n"
        ans = extra + articles + info
        await interaction.response.send_message(ans)

    elif articleinfo is not None:
        prompt = articleinfo
        response = client.chat.completions.create(
            messages=[{
                "role":
                "user",
                "content":
                f"You are a wise person on Indian constituion articles. You are given an article number, you just need to brief that particular article. Start with Article <given number> states that ..If anyone give invalid article number, tell him the range of number of articles. You have to give very concise response exact 2 sentence within 60 words(remember word count) Also give some emojis if needed to make attractive\n{prompt}",
            }],
            model="llama3-8b-8192",
        )

        ans = response.choices[0].message.content

        await interaction.response.send_message(ans)

    else:
        message = ""
        for i in details_parts:
            details_parts[i]["Title"] = " -" + details_parts[i][
                "Title"] if "CHAPTER" in details_parts[i][
                    "Title"] else details_parts[i]["Title"]
            message += details_parts[i]["Title"]
            message += "\n"
        message += "## :rocket: *Now please let me know in which part you interested.*\n"

        await interaction.response.send_message(
            "## You have entered invalid part number. Here is the list\n" +
            message)


bot.run(MY_SECRET)
