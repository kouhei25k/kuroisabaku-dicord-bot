
import discord
import datetime as dt
# 自分のBotのアクセストークンに置き換えてください
TOKEN = '*************************'

# 接続に必要なオブジェクトを生成
client = discord.Client()


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


async def reply(message):
    reply = f'{message.author.mention} 呼んだ？'  # 返信メッセージの作成
    await message.channel.send(reply)  # 返信メッセージを送信

# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    if client.user in message.mentions:  # 話しかけられたかの判定
        await reply(message)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    weekday = dt.date.today().weekday()
    nowtime = dt.datetime.now().strftime("%H:%M")
   # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == '/user':
        user = message.author.mention + "\nhello"
        await message.channel.send(user)

    if message.content == '/weekday':
        await message.channel.send(weekday)

    if message.content == '/time':

        await message.channel.send(nowtime)

    if message.content == '/help':
        help_message = message.author.mention + \
            "\n**コマンド一覧 **\n--すべてのボス出現時間--\n/boss・・・ボスごと\n/boss-time・・・時間ごと\n/boss-tm・・・明日のボスごと\n/boss-time-tm・・・明日の時間ごと\n\n--個別ボス出現時間--"
        for boss_name in bosses:
            help_message += f'\n{boss_name} ・・・ {bosses[boss_name]}'
        await message.channel.send(help_message)

    if message.content == '/boss':
        boss_msg = message.author.mention + '\n今日のボス(ボスごと)'
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday] if nowtime < s]
            if boss_today_times:
                boss_msg += f'\n--{bosses[boss]}--'
                for boss_today_time in boss_today_times:
                    boss_msg += f'\n{boss_today_time}'
        await message.channel.send(boss_msg)

    if message.content == '/boss-tm':
        boss_tm_msg = message.author.mention + '\n明日のボス(ボスごと)'
        for boss in bosses_time_dict:
            boss_time = bosses_time_dict[boss]
            boss_today_times = [s for s in boss_time[weekday+1]]
            if boss_today_times:
                boss_tm_msg += f'\n--{bosses[boss]}--'
                for boss_today_time in boss_today_times:
                    boss_tm_msg += f'\n{boss_today_time}'
        await message.channel.send(boss_tm_msg)

    if message.content == '/boss-time':
        boss_time_msg = message.author.mention + '\n今日のボス(時間ごと)'
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
                boss_time_msg += f'\n--{time[0]}--'
                for boss_name in time[1]:
                    boss_time_msg += f'\n{bosses[boss_name]}'
        await message.channel.send(boss_time_msg)

    if message.content == '/boss-time-tm':
        boss_time_tm_msg = message.author.mention + '\n明日のボス(時間ごと)'
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
                boss_time_tm_msg += f'\n--{time[0]}--'
                for boss_name in time[1]:
                    boss_time_tm_msg += f'\n{bosses[boss_name]}'
        await message.channel.send(boss_time_tm_msg)

        # 個別のボス時間
    # if message.content in bosses:
    #     boss_time = bosses_time_dict[message.content]
    #     boss_name_conv = bosses[message.content]
    #     await message.channel.send(f'本日の{boss_name_conv}は')
    #     today_time = [s for s in boss_time[weekday] if nowtime < s]
    #     if not today_time:
    #         await message.channel.send('ありません')
    #     else:
    #         for next_time in today_time:
    #             await message.channel.send(next_time)
    #     await message.channel.send('-----------')
    #     await message.channel.send(f'明日の{boss_name_conv}は')
    #     if not boss_time[weekday+1]:
    #         await message.channel.send('ありません')
    #     else:
    #         for tmrw_time in boss_time[weekday+1]:
    #             await message.channel.send(tmrw_time)

    if message.content in bosses:
        boss_time = bosses_time_dict[message.content]
        boss_name_conv = bosses[message.content]
        each_boss_msg = message.author.mention + f'\n本日の{boss_name_conv}は'
        today_time = [s for s in boss_time[weekday] if nowtime < s]
        if not today_time:
            each_boss_msg += '\nありません'
        else:
            for next_time in today_time:
                each_boss_msg += f'\n{next_time}'
        each_boss_msg += f'\n-----------\n明日の{boss_name_conv}は'
        if not boss_time[weekday+1]:
            each_boss_msg += '\nありません'
        else:
            for tmrw_time in boss_time[weekday+1]:
                each_boss_msg += f'\n{tmrw_time}'
        await message.channel.send(each_boss_msg)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
