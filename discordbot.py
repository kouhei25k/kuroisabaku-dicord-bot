
import discord
import datetime as dt
import boss_time
# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzEwNDgwMDUyMDY3ODkzMzgw.Xr1FHw.m3dinKkc5bWnyL6g-Mc6KF43yBM'

# 接続に必要なオブジェクトを生成
client = discord.Client()

times = ["01:30"]
bosses = {
    '/kuzaka': 'クザカ', '/nuberu': 'ヌーベル', '/kutumu': 'クツム', '/karanda': 'カランダ', '/opin': 'オピン', '/gamosu': 'ガーモス', '/muraka': 'ムラカ', '/gyunto': 'ギュント'
}

bosses_time_dict = {
    # クザカ時間
    '/kuzaka': [["01:30", "11:00", "16:00"], ["01:30", "11:00", "16:00"], [
        "01:30", "19:00"], ["01:30", "11:00"], ["01:30"], [
        "11:00", "19:00"], []],

    # ヌーベル時間
    '/nuberu': [["01:30", "19:00"], ["01:30", "19:00", "23:00"], [
        "01:30", "16:00"], ["16:00", "19:00"], ["11:00", "16:00"], [
        "11:00"], []],

    # クツム時間
    '/kutumu': [["16:00", "23:00"], ["16:00", "19:00"], [
        "16:00"], ["16:00", "19:00"], ["16:00", "23:00"], [
        "16:00"], ["11:00", "16:00"]],

    # カランダ
    '/karanda': [["19:00", "23:00"], ["23:00"], [
        "19:00"], ["01:30", "19:00"], ["01:30", "23:00"], ["16:00", "19:00"], ["11:00", "16:00"]],

    # オピン
    '/opin': [[], [], [], ["23:00"], [], ["01:30"], ["23:00"]],

    # ガーモス
    '/gamosu': [[], [], [], [], [], [], ["01:30", "19:00"]],

    # ムラカ
    '/muraka': [[], [], [], [], ["19:00"], [], []],

    # ギュント
    '/gyunto': [[], [], [], [], ["19:00"], [], []]
}


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# 曜日取得
weekday = dt.date.today().weekday()
# 曜日取得
nowtime = dt.datetime.now().strftime("%H:%M")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == '/weekday':
        await message.channel.send(weekday)

    if message.content == '/time':
        await message.channel.send(nowtime)

    if message.content == '/help':
        await message.channel.send('**コマンド一覧**')

        await message.channel.send('--すべてのボス出現時間--')
        await message.channel.send(' /boss・・・ボスごと')
        await message.channel.send(' /boss-time・・・時間ごと')
        await message.channel.send(' /boss-tm・・・明日のボスごと')
        await message.channel.send(' /boss-time-tm・・・明日の時間ごと')
        await message.channel.send('--個別ボス出現時間--')
        for boss_name in bosses:
            await message.channel.send(f'{boss_name} ・・・ {bosses[boss_name]}')

    if message.content == '/boss':
        await message.channel.send('今日のボス(ボスごと)')
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday] if nowtime < s]
            if boss_today_times:
                await message.channel.send(f'--{bosses[boss]}--')
                for boss_today_time in boss_today_times:
                    await message.channel.send(boss_today_time)

    if message.content == '/boss-tm':
        await message.channel.send('明日のボス(ボスごと)')
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday+1]]
            if boss_today_times:
                await message.channel.send(f'--{bosses[boss]}--')
                for boss_today_time in boss_today_times:
                    await message.channel.send(boss_today_time)

    if message.content == '/boss-time':
        await message.channel.send('今日のボス(時間ごと)')
        today_time_table = {"01:30": [], "11:00": [],
                            "16:00": [], "19:00": [], "23:00": []}
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday] if nowtime < s]
            for time in today_time_table:
                if time in boss_today_times:
                    today_time_table[time].append(boss)
        for time in today_time_table.items():
            if time[1]:
                await message.channel.send(f'--{time[0]}--')
                for boss_name in time[1]:
                    await message.channel.send(bosses[boss_name])

    if message.content == '/boss-time-tm':
        await message.channel.send('明日のボス(時間ごと)')
        today_time_table = {"01:30": [], "11:00": [],
                            "16:00": [], "19:00": [], "23:00": []}
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday+1]]
            for time in today_time_table:
                if time in boss_today_times:
                    today_time_table[time].append(boss)
        for time in today_time_table.items():
            if time[1]:
                await message.channel.send(f'--{time[0]}--')
                for boss_name in time[1]:
                    await message.channel.send(bosses[boss_name])

        # 個別のボス時間
    if message.content in bosses:
        boss_time = bosses_time_dict[message.content]
        boss_name_conv = bosses[message.content]
        await message.channel.send(f'本日の{boss_name_conv}は')
        today_time = [s for s in boss_time[weekday] if nowtime < s]
        if not today_time:
            await message.channel.send('ありません')
        else:
            for next_time in today_time:
                await message.channel.send(next_time)

        await message.channel.send('-----------')
        await message.channel.send(f'明日の{boss_name_conv}は')
        if not boss_time[weekday+1]:
            await message.channel.send('ありません')
        else:
            for tmrw_time in boss_time[weekday+1]:
                await message.channel.send(tmrw_time)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
