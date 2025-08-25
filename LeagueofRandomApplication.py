import os
import discord
from discord import app_commands
import random
from dotenv import load_dotenv  # .env を使う場合

# .env を読み込む（開発環境向け）
load_dotenv()

# 環境変数からトークンを取得
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("環境変数 DISCORD_TOKEN が設定されていません")

# Bot本体
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ロールごとのチャンピオン一覧
champions_by_lane = {
    "top": 
    [
        "Aatrox", "Akali", "Ambessa", "Aurora", "Camille", "Cassiopeia", "Cho'Gath", "Darius", 
        "Dr.Mundo", "Fiora", "Gangplank", "Garen", "Gner", "Gragas", "Gwen", "Heimerdinger", 
        "Illaoi", "Irelia", "Jax", "Jayce", "K'Sante", "Kayle", "Kennen", "Kled", "Malphite", 
        "Mordekaiser", "Nasus", "Olaf", "Ornn", "Pantheon", "Poppy", "Quinn", "Renekton", 
        "Riven", "Rumble", "Ryze", "Sett", "Shen", "Singed", "Sion", "Tahm Kench", "Teemo", 
        "Trundle", "Tryndamare", "Udyr", "Urgot", "Varus", "Vayne", "Viego", "Vladimir", 
        "Volibear", "Warwick", "Wukong", "Yasuo", "Yone", "Yorick", "Zac"
    ],

    "jungle": 
    [
        "Amumu", "Bel'Veth", "Brand", "Briar", "Diana", "Dr.Mundo", "Ekko", "Elise", "Evelynn", "Fiddlesticks",
        "Gragas", "Graves", "Gwen", "Hecarim", "Ivern", "Jarvan IV", "Jax", "Karthus", "Kayn", "Kha'Zix", 
        "Kindred","Lee Sin", "Lillia", "Master Yi", "Morgana", "Mordekaiser", "Naafiri", "Nautilus", "Nidalee", "Nocturne",
        "Nunu & Willump", "Pantheon", "Poppy", "Quiyana","Rammus", "Rek'Sai", "Rengar", "Sejuani", "Shaco", "Shyvana", 
        "Skarner", "Sylas", "Taliyah", "Talon", "Trundle","Udyr", "Vi", "Viego", "Volibear", "Warwick", 
        "Wukong", "Xin Zhao", "Zac", "Zed"
    ],

    "middle": 
    [
        "Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Aurora", "Azir", "Brand",
        "Cassiopeia", "Corki", "Cho'gath" "Diana", "Ekko", "Fizz", "Galio", "Heimerdinger", "Hwei", "Irelia", "Jayce",
        "Kassadin", "Katarina", "Kayle", "Kennen", "LeBlanc", "Lissandra", "Lux", "Malphite", "Malzahar", "Mel", "Millio", "Morgana", "Naafiri",
        "Neeko", "Orianna", "Pantheon", "Qiyana", "Ryze", "Sion", "Smolder", "Swain", "Sylas", "Syndra", "Taliyah", "Talon", "Tristana",
        "Twisted Fate", "Twitch", "Veigar", "Vel'Koz", "Vex", "Viego", "Viktor", "Vladimir", "Xerath", "Yasuo", "Yone", "Zed",
        "Ziggs", "Zoe"
    ],

    "bottom": 
    [
        "Aphelios", "Ashe", "Caitlyn", "Corki", "Draven", "Ezreal", "Hwei", "Jhin", "Jinx", "Kai'Sa", 
        "Kalista","Kog'Maw", "Lucian", "Mel", "Miss Fortune", "Nilah", "Samira", "Senna", "Sivir", "Smolder", 
        "Swain", "Tristana","Twitch", "Varus", "Vayne", "Xayah", "Yasuo", "Yunara", "Zeri", "Ziggs"
    ],

    "support": 
    [
        "Alistar", "Bard", "Brand", "Blitzcrank", "Braum", "Elise", "Fiddlesticks", "Galio", "Hwei", "Janna", 
        "Karma", "LeBlanc", "Leona", "Lulu", "Lux", "Maokai", "Mel", "Millio", "Morgana", "Nami", 
        "Nautilus","Nidalee", "Neeko", "Pantheon", "Poppy", "Pyke", "Rakan", "Rell", "Renata Glasc", "Senna", 
        "Seraphine", "Shaco", "Shen", "Sona", "Soraka", "Tahm Kench", "Teemo", "Taric", "Thresh", "Vel'Koz",
        "Xerath", "Yuumi", "Zilean", "Zoe", "Zyra"
    ]
}

# /lane コマンド
@tree.command(name="lane", description="ランダムな出力します")
@app_commands.choices(
    category = [
        app_commands.Choice(name="ALL", value="all"),
        app_commands.Choice(name="TOP", value="top"),
        app_commands.Choice(name="JG", value="jungle"),
        app_commands.Choice(name="MID", value="middle"),
        app_commands.Choice(name="BOT", value="bottom"),
        app_commands.Choice(name="SUP", value="support")
        ]
    )

async def lane(interaction: discord.Interaction, category: app_commands.Choice[str]):
    if category.value == "all":
        # 全てのロールのチャンピオンを結合
        all_champions = []
        for champs in champions_by_lane.values():
            all_champions.extend(champs)
        choice = random.choice(all_champions)
    else:
        choice = random.choice(champions_by_lane[category.value])
    
    await interaction.response.send_message(f"🎲 {category.name}  **{choice}** ")



# Bot起動時
@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ ログイン成功: {client.user}")

client.run(TOKEN)