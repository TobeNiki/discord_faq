
from typing import List
from discordbot.config.config import load_token
import discord
from discord.commands import Option
from py.content.indeces_management import Content_Management
from py.content.content_schema import Content
from discord.ext import commands

intent = discord.Intents.default()
intent.messages = True

bot = commands.Bot(
    intent=intent
)

token = load_token()

manager = Content_Management()

category_list = manager.get_all_category()
 
class UserInputSelect(discord.ui.Select):
    def __init__(self, options)->None:
        super().__init__(placeholder="FAQ", options=options)

    async def callback(self, interaction: discord.Interaction):
        faq_id = self.values[0]

        faq = manager.get_content(faq_id)

        embed = discord.Embed(title=faq.question, description=faq.answer, color=0xffbf00)
        embed.add_field(name="カテゴリー", value=faq.category)
        embed.add_field(name="登録者", value=faq.regist_user)
        embed.add_field(name="最終更新日",value=faq.update_date)
        embed.add_field(name="id", value=faq.content_id)
        await interaction.response.edit_message(embed=embed)

# Viewクラスを継承してButtonを持ったViewを
class TestView(discord.ui.View):
    def __init__(self, options:List[discord.SelectOption]):
        super().__init__(timeout=3000, disable_on_timeout=True)
        
        self.add_item(UserInputSelect(options=options))

options = []

@bot.slash_command(name="faq")
async def search_faq(
    ctx: discord.ApplicationContext,
    question: Option(str, "質問内容を入力してください", required=True)
    #category: Option(str, "カテゴリを選択してください", choices=category_list)
    ):
    content = Content(question=question, category="")
    result = manager.search_content(body=content)
    if len(result) == 0:
        await ctx.respond(f"検索にヒットしませんでした.")
        return

    message = f"""FAQの検索結果は以下です。\n"""
    for index, faq in enumerate(result, 1):
        options.append(discord.SelectOption(label=f"FAQ {index}", value=faq.content_id))
        message += f"{index}. {faq.question}"
    message += "下記のドロップダウンから目的のFAQを選択してください"

    view = TestView(options=options)
    
    embed = discord.Embed(title="[FAQ]検索結果", description=message, color=0xffbf00)
    await ctx.interaction.response.send_message(embed=embed,view=view)

bot.run(token)