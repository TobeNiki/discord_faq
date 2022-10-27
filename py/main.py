import asyncio
import json
import os
from typing import List
from unicodedata import name
from config.config import load_token
import discord
from discord.commands import Option
from content.indeces_management import Content_Management
from content.content_schema import Content
from discord.ext import commands
from user.user_management import User_Managemnt

intent = discord.Intents.default()
intent.messages = True

bot = commands.Bot(
    intent=intent
)

token = load_token()

manager = Content_Management()

category_list = manager.get_all_category()
 
user_manager = User_Managemnt()

#embed color type
success_type_color_is_orange = 0xff4000
error_type_color_is_red = 0x8b0000
class FaqSearchResultSelect(discord.ui.Select):
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

# Viewクラスを継承してdropdownを持ったviewを作成
class FAQView(discord.ui.View):
    def __init__(self, options:List[discord.SelectOption]):
        super().__init__(timeout=3000, disable_on_timeout=True)
        
        self.add_item(FaqSearchResultSelect(options=options))


@bot.slash_command(name="faq")
async def search_faq(
    ctx: discord.ApplicationContext,
    question: Option(str, "質問内容を入力してください", required=True)
    #category: Option(str, "カテゴリを選択してください", choices=category_list)
    ):
    content = Content(question=question, category="")
    result = manager.search_content(body=content)
    if not result:
        await ctx.respond("検索にヒットしませんでした.")
        return

    message = "FAQの検索結果は以下です。\n"
    options = []
    for index, faq in enumerate(result, 1):
        #discord.SelectOptionのvalueは100文字以上の文字列を渡せないので
        #elasticsearchのdocmentIdを渡してもう一度elasticsearchからidで取得してもらう
        options.append(discord.SelectOption(label=f"FAQ {index}", value=faq.content_id))
        message += f"{index}. {faq.question}"
    message += "下記のドロップダウンから目的のFAQを選択してください"

    view = FAQView(options=options)
    embed = discord.Embed(
        title="[FAQ]検索結果", 
        description=message, 
        color=success_type_color_is_orange)
    await ctx.interaction.response.send_message(embed=embed,view=view)

@bot.slash_command(name="faqregist")
async def faq_regist(
    ctx: discord.ApplicationContext,
    name: Option(str, "名前を入力してください", required=True),
    password: Option(str, "パスワードを入力してください", required=True),
    question: Option(str, "FAQの質問を入力してください"),
    category: Option(str, "FAQのカテゴリを入力してください"),
    answer: Option(str, "FAQの回答を入力してください")
    ):
    if not user_manager.basic_login(name=name, password=password):
        await ctx.respond("FAQ管理者へのログインに失敗しました")
        return

    content = Content(
        content_id=None, 
        regist_user=name, 
        category=category, 
        question=question, 
        answer=answer)
    try:
        manager.create_content(content)
    except:
        embed_error = discord.Embed(
            title="[FAQ]管理", 
            description="FAQの登録が失敗しました", 
            color=error_type_color_is_red)
        await ctx.interaction.response.send_message(embed=embed_error)
        return

    embed = discord.Embed(
        title="[FAQ]管理", 
        description="FAQの登録が完了しました", 
        color=success_type_color_is_orange)
    await ctx.interaction.response.send_message(embed=embed)


@bot.slash_command(name="faqdelete")
async def faq_delete(
    ctx: discord.ApplicationContext,
    name: Option(str, "名前を入力してください", required=True),
    password: Option(str, "パスワードを入力してください", required=True),
    faq_content_id: Option(str, "faqのコンテンツIDを入力してください")
    ):
    if not user_manager.basic_login(name=name, password=password):
        await ctx.respond("FAQ管理者へのログインに失敗しました")
        return
    try:
        manager.delete_content(faq_content_id)
    except:
        embed_error = discord.Embed(
            title="[FAQ]管理", 
            description="FAQの削除が失敗しました", 
            color=error_type_color_is_red)
        await ctx.interaction.response.send_message(embed=embed_error)
        return 

    embed = discord.Embed(
        title="[FAQ]管理", 
        description="FAQの削除が完了しました", 
        color=success_type_color_is_orange)
        
    await ctx.interaction.response.send_message(embed=embed)
    
@bot.slash_command(name="faqupdate")
async def faq_update(
    ctx: discord.ApplicationContext,
    name: Option(str, "名前を入力してください", required=True),
    password: Option(str, "パスワードを入力してください", required=True),
    faq_content_id: Option(str, "faqのコンテンツIDを入力してください"),
    question: Option(str, "FAQの質問を入力してください"),
    category: Option(str, "FAQのカテゴリを入力してください"),
    answer: Option(str, "FAQの回答を入力してください")
    ):

    if not user_manager.basic_login(name=name, password=password):
        await ctx.respond("FAQ管理者へのログインに失敗しました")
        return

    content = Content(
        content_id=faq_content_id, 
        regist_user=name, 
        category=category, 
        question=question, 
        answer=answer)
    try:
        manager.update_content(content)
    except:
        embed_error = discord.Embed(
            title="[FAQ]管理", 
            description="FAQの更新が失敗しました", 
            color=error_type_color_is_red)
        await ctx.interaction.response.send_message(embed=embed_error)
        return
    embed = discord.Embed(
        title="[FAQ]管理", 
        description="FAQの更新が完了しました", 
        color=success_type_color_is_orange)
    await ctx.interaction.response.send_message(embed=embed)


@bot.slash_command(name="faqbulkinsert")
async def faq_bulk_insert(
    ctx: discord.ApplicationContext,
    name: Option(str, "名前を入力してください", required=True),
    password: Option(str, "パスワードを入力してください", required=True),
    file: discord.Attachment
):
    if not user_manager.basic_login(name=name, password=password):
        await ctx.respond("FAQ管理者へのログインに失敗しました")
        return
    
    #elasticsearch のbulk insertは100MBの制限があるが、
    # Discord bot は8mbしか無理なため、特にsizeチェックはいらない
    if not (file.content_type == "application/json; charset=utf-8"):
        await ctx.respond("fileがjsonファイルではありません. ")
        return
    
    contents = json.load(file.read())
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manager.async_bulk_insert(contents))

    embed = discord.Embed(
        title="[FAQ]管理", 
        description="FAQのバルクインサートが完了しました", 
        color=success_type_color_is_orange)
    await ctx.interaction.response.send_message(embed=embed)
    
    
#==== user management command ====

    



bot.run(token)