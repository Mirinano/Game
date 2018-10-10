import discord
import datetime
import random
import time as t

client = discord.Client()

master_server = ""

accept_word = ("わかった", "了解", "いいよ")

user_tuple = ("On", "Off")
user_str = "OnOff"
user_info = dict()
user_info["On"] = {"name": "ロニエ",
"Token": "",}
user_info["Off"] = {"name": "ロニエ",
"Token": ""}
janken_challenge = dict()
janken_challenge["On"] = {
"intro" : "じゃんですか？いいですよ！負けませんからね！",
"start" : "いきますよ。最初はグー。\nじゃんけん…、",
"restart" : "あいこで…、",
"win" : "やりました！私の勝ちです♪{}さんには負けませんよ♪",
"lose" : "あっれー、{}さんに負けてしまいました…\nでも、次は私が勝ちますからね！",
"cancel" : "{}さんじゃんけん辞めちゃうんですか？そうですか…\nまた、お相手してくださいね？"
}
janken_challenge["Off"] = {
"intro" : "じゃんけん…？暇なんですか…？\nわかりました。でも、私が勝ったらお仕事に戻ってくださいね？",
"start" : "せーの、最初はグー。\nじゃんけん…、",
"restart" : "あいこで…、",
"win" : "私の勝ち、ですね\nほら、{}さんもはやくお仕事に戻ってください！",
"lose" : "私が負けた…？\n{}さん、もう一回…！",
"cancel" : "あら、じゃんけんなんかやらずにお仕事に戻る気になってくれましたか？\nお仕事頑張ってくださいね！{}さん♪"
}

janken_emoji = ("✊", "✌", "✋")
janken_dict = dict()
janken_dict["✊"] = {"✊" : "restart", "✌" : "win", "✋": "lose"}
janken_dict["✌"] = {"✊" : "lose", "✌" : "restart", "✋": "win"}
janken_dict["✋"] = {"✊" : "win", "✌" : "lose", "✋" : "restart"}

marubatu_rule = """
マルバツゲームですか？いいですよ！
ルールは、⭕を3つ、縦横斜めのいずれかでそろえられれば<@{user}>さんの勝ち、
❌を3つ、縦横斜めのいずれかでそろえられてしまったら私の勝ちでいいですね？
ゲームを始めるときは⭕を、ゲームをやめるときは❌をクリックしてください。
"""

marubatu_content = """
⭕：{author_name}さん
❌：{bot_name}
現在の手番：{0}
　盤　面               番号表
{1}｜{2}｜{3}|    １｜２｜３
ー＋－＋－|    ー＋－＋－
{4}｜{5}｜{6}|    ４｜５｜６
ー＋－＋－|    ー＋－＋－　　
{7}｜{8}｜{9}|    ７｜８｜９
{select_content}
"""
select_content = """

⭕を入力したい番号を選択してください。
❌をクリックするとゲームを終了します。
※最後に❌が表示された後に操作してください。
"""
number_emoji = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
#creat dict
num = 1
number_emoji_dict = dict()
emoji_number_dict = dict()
for ne in number_emoji:
    number_emoji_dict[str(num)] = ne
    emoji_number_dict[ne] = str(num)
    num += 1

result_content = {
"win" : "<@{0}>さんの勝ちです！おめでとうございます！！",
"lose" : "私の勝ちです！<@{0}>さん残念！再挑戦、お待ちしています♪",
"draw" : "引き分けですね！\n<@{0}>さん、もう一戦やられますか？再戦するなら⭕を、やめるなら❌を選択してください！",
"retire" : "リタイアですね。\nわかりました！<@{0}>さん、また遊びましょうね♪",
"timeouterr" : "5分間、選択がなかったので、このゲームはやめにします！\n<@{0}>さん、疲れてるときはちゃんと寝てくださいね♪",
"err" : "<@391943696809197568>予期せぬエラーです。大至急調査をしてください。<@{0}>さんとのゲームです。"
}
draw_content = {
"retire" : "わかりました！<@{0}>さん、また遊んでくださいね♪",
"timeout" : "5分間、選択がなかったので、次のゲームはやめにします！\n<@{0}>さん、疲れてるときはちゃんと寝てくださいね♪"
}

class Moririn():
    client = discord.Client()
    def change_dict(self, content):
        # 4、6、8行目を取り出す。
        content_list = content.split("\n")
        line1 = content_list[4].split("|")[0]
        line2 = content_list[6].split("|")[0]
        line3 = content_list[8].split("|")[0]
        line1 = line1.split("｜")
        line2 = line2.split("｜")
        line3 = line3.split("｜")
        return_dict = dict()
        n = 1
        for line in (line1, line2, line3):
            for l in line:
                return_dict[str(n)] = l
                n += 1
        del content_list
        del line1
        del line2
        del line3
        del n
        return return_dict

    def reaction_add_check(self, content):
        emoji_dict = Moririn().change_dict(content=content)
        return_list = list()
        for num in list(range(1, 10)):
            if not (("○" in emoji_dict[str(num)]) or ("✕" in emoji_dict[str(num)])):
                return_list.append(str(num))
            else:
                pass
        del emoji_dict
        del num
        del content
        return return_list
    
    def change_item(self, content):
        item_dict = Moririn().change_dict(content=content)
        return_dict = dict()
        for num in list(range(1, 10)):
            if "○" in item_dict[str(num)]:
                return_dict[str(num)] = 1
            elif "✕" in item_dict[str(num)]:
                return_dict[str(num)] = -1
            else:
                return_dict[str(num)] = 0
        del num
        del item_dict
        return return_dict

    def check_game(self, num_dict):
        for num in list(range(0, 7, 3)):
            count = 0
            for n in list(range(1, 4, 1)):
                count += num_dict[str(num + n)]
            if count == 3:
                result = "win"
                break
            elif count == -3:
                result = "lose"
                break
            else:
                result = "draw"
        if not result in ("win", "lose"):
            for num in list(range(1, 4, 1)):
                count = 0
                for n in list(range(0, 7, 3)):
                    count += num_dict[str(num + n)]
                if count == 3:
                    result = "win"
                    break
                elif count == -3:
                    result = "lose"
                    break
                else:
                    result = "draw"
            if not result in ("win", "lose"):
                for num in [0, 2]:
                    count = num_dict[str(1 + num)] + num_dict[str(5)] + num_dict[str(9 - num)]
                    if count == 3:
                        result = "win"
                        break
                    elif count == -3:
                        result = "lose"
                        break
                    else:
                        result = "draw"
                if not result in ("win", "lose"):
                    result = "draw"
        del num
        del count
        return result

    def bot_play(self, reaction_list, num_dict):
        for nn in [-2, 2, -1, 1]:
            for num in list(range(0, 7, 3)):
                count = 0
                for n in list(range(1, 4, 1)):
                    count += num_dict[str(num + n)]
                if count == nn:
                    for n in list(range(1, 4, 1)):
                        if num_dict[str(num + n)] == 0:
                            number = num + n
                            return number
                        else:
                            pass
                else:
                    pass
            for num in list(range(1, 4, 1)):
                count = 0
                for n in list(range(0, 7, 3)):
                    count += num_dict[str(num + n)]
                if count == nn:
                    for n in list(range(0, 7, 3)):
                        if num_dict[str(num + n)] == 0:
                            number = num + n
                            return number
                        else:
                            pass
                else:
                    pass
            for num in [0, 2]:
                count = num_dict[str(1 + num)] + num_dict[str(5)] + num_dict[str(9 - num)]
                if count == nn:
                    for nm in [(1 + num), 5, (9 - num)]:
                        if num_dict[str(nm)] == 0:
                            return nm
                        else:
                            pass
                else:
                    pass
        return random.choice(reaction_list)
    
    def change_content(self, content_dict, emoji, player, bot_name, author):
        n = content_dict
        if player == bot_name:
            sc = ""
        else:
            sc = select_content
        content = marubatu_content.format(player, n["1"], n["2"], n["3"], n["4"], n["5"], n["6"], n["7"], n["8"], n["9"], author_name=author, bot_name=bot_name, select_content=sc)
        return content

@client.event
async def on_ready():
    print("Complete!")

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.server.id == master_server:
            bot_name = random.choice(user_tuple)
            if (("じゃんけんしよ" in message.content) or ("じゃんけんをしよ" in message.content)):
                await client.send_message(message.channel, janken_challenge[bot_name]["intro"])
                await client.wait_for_message(timeout=5, content=accept_word, channel=message.channel, author=message.author)
                msg = await client.send_message(message.channel, janken_challenge[bot_name]["start"])
                while True:
                    for emoji in janken_emoji:
                        await client.add_reaction(msg, emoji)
                    target_reaction = await client.wait_for_reaction(message=msg, timeout=30)
                    if target_reaction == None:
                        if message.author.nick == None:
                            name = message.author.name
                        else:
                            name = message.author.nick
                        await client.send_message(message.channel, janken_challenge[bot_name]["cancel"].format(name))
                        break
                    else:
                        if target_reaction.user != client.user:
                            my_choice = random.choice(janken_emoji)
                            await client.send_message(message.channel, my_choice)
                            result = janken_dict[my_choice][target_reaction.reaction.emoji]
                            if result is "restart":
                                msg = await client.send_message(message.channel, janken_challenge[bot_name]["restart"])
                            elif result in ("win", "lose"):
                                if message.author.nick == None:
                                    name = message.author.name
                                else:
                                    name = message.author.nick
                                await client.send_message(message.channel, janken_challenge[bot_name][result].format(name))
                                break
                            else:
                                await client.send_message(message.channel, "【エラー】\n<@391943696809197568>コードを確認してください。")
                                break
                        else:
                            pass
            elif (("まるばつゲーム" in message.content) or ("マルバツゲーム" in message.content) or ("〇✖ゲーム" in message.content)):
                # start game.
                msg_ch = message.channel
                msg = await client.send_message(message.channel, marubatu_rule.format(user=message.author.id))
                await client.add_reaction(msg, "⭕")
                await client.add_reaction(msg, "❌")
                time = 300
                start_time = datetime.datetime.now()
                while True:
                    target_reaction = await client.wait_for_reaction(message=msg, timeout=time)
                    if target_reaction == None: #timeout
                        await client.send_message(message.channel, "5分間、選択がなかったから、このゲームはやめにしますね。\n<@{0}>さん、疲れているときはちゃんと休んでくださいね♪".format(message.author.id))
                        deal = "cancel"
                        break
                    else:
                        if target_reaction.user != client.user:
                            if target_reaction.reaction.emoji == "⭕":
                                deal = "start"
                                break
                            elif target_reaction.reaction.emoji == "❌":
                                await client.send_message(message.channel, "おっけー！<@{0}>さん、また遊ぼうね！".format(message.author.id))
                                deal = "cancel"
                                break
                            else:
                                await client.remove_reaction(msg, target_reaction.reaction.emoji, target_reaction.user)
                                elapsed_time = datetime.datetime.now() - start_time #経過時間を計測
                                time = time - int(elapsed_time.seconds)
                                if time > 0:
                                    pass
                                else:
                                    await client.send_message(message.channel, "5分間、選択がなかったから、このゲームはやめにするね！\n<@{0}>さん、また遊ぼうね！".format(message.author.id))
                                    deal = "cancel"
                                    break
                        else:
                            pass
                if deal == "cancel":
                    pass
                elif deal == "start":
                    content_dict = dict()
                    for num in range(1, 10):
                        content_dict[str(num)] = "　"
                    while True:
                        #let's game!
                        if message.author.nick == None:
                            author_name = message.author.name
                        else:
                            author_name = message.author.nick
                        author = "<@" + message.author.id + ">"
                        bot_name = "ロニエ"
                        player_emoji = {bot_name: "✕ ", author: "○"}
                        players = {bot_name, author}
                        player = random.choice(list(players))
                        md = "　"
                        if player == bot_name:
                            sc = ""
                        else:
                            sc = select_content
                        msg = await client.send_message(message.channel, marubatu_content.format(player, md, md, md, md, md, md, md, md, md, author_name=author_name, bot_name=bot_name, select_content=sc))
                        while True:
                            content = msg.content
                            num_dict = Moririn().change_item(content)
                            result = Moririn().check_game(num_dict)
                            if result in ["win", "lose"]:
                                n = content_dict
                                msg = await client.edit_message(message=msg, new_content=marubatu_content.format(player, n["1"], n["2"], n["3"], n["4"], n["5"], n["6"], n["7"], n["8"], n["9"], author_name=author_name, bot_name=bot_name, select_content=""))
                                break
                            else:
                                reaction_list = Moririn().reaction_add_check(content)
                                if len(reaction_list) == 0:
                                    result = "draw"
                                    n = content_dict
                                    msg = await client.edit_message(message=msg, new_content=marubatu_content.format(player, n["1"], n["2"], n["3"], n["4"], n["5"], n["6"], n["7"], n["8"], n["9"], author_name=author_name, bot_name=bot_name, select_content=""))
                                    break
                                else:
                                    if player == bot_name:
                                        change_num = Moririn().bot_play(reaction_list, num_dict)
                                        content_dict[str(change_num)] = "✕ "
                                        t.sleep(10)
                                    elif player == author:
                                        for rl in reaction_list:
                                            await client.add_reaction(msg, number_emoji_dict[str(rl)])
                                        await client.add_reaction(msg, "❌")
                                        timeout = 300
                                        while True:
                                            start_time = datetime.datetime.now()
                                            target_reaction = await client.wait_for_reaction(message=msg, timeout=timeout)
                                            if target_reaction == None: #タイムアウト
                                                result = "timeouterr"
                                                break
                                            else:
                                                if target_reaction.user == message.author:
                                                    if target_reaction.reaction.emoji == "❌": 
                                                        result = "retire"
                                                        break
                                                    else:
                                                        try:
                                                            change_num = emoji_number_dict[target_reaction.reaction.emoji]
                                                            content_dict[str(change_num)] = "○"
                                                            break
                                                        except:
                                                            elapsed_time = datetime.datetime.now() - start_time #経過時間を計測
                                                            timeout = timeout - int(elapsed_time.seconds)
                                                            await client.remove_reaction(message=msg, emoji=target_reaction.reaction.emoji, member=target_reaction.user)
                                                            if timeout > 0:
                                                                pass
                                                            else:
                                                                result = "timeouterr"
                                                                break
                                                else:
                                                    pass
                                        if result in ["retire", "timeouterr"]:
                                            break
                                        else:
                                            pass
                                        await client.clear_reactions(msg)
                                    else:
                                        result = "err"
                                        break
                                    for np in players.difference({player}):
                                        new_player = np
                                    new_content = Moririn().change_content(content_dict=content_dict, emoji=player_emoji[player], player=new_player, bot_name=bot_name, author=message.author.name)
                                    player = new_player
                                    msg = await client.edit_message(message=msg, new_content=new_content)
                        if result == "draw":
                            msg = await client.send_message(msg_ch, result_content[result].format(message.author.id))
                            await client.add_reaction(msg, "⭕")
                            await client.add_reaction(msg, "❌")
                            while True:
                                start_time = datetime.datetime.now()
                                timeout = 300
                                target_reaction = await client.wait_for_reaction(message=msg, timeout=timeout)
                                if target_reaction == None: #タイムアウト
                                    result = "timeout"
                                    break
                                else:
                                    if target_reaction.user == message.author:
                                        if target_reaction.reaction.emoji == "❌":
                                            result = "retire"
                                            break
                                        elif target_reaction.reaction.emoji == "⭕":
                                            result = "restart"
                                            break
                                        else:
                                            elapsed_time = datetime.datetime.now() - start_time #経過時間を計測
                                            timeout = timeout - int(elapsed_time.seconds)
                                            await client.remove_reaction(message=msg, emoji=target_reaction.reaction.emoji, member=target_reaction.user)
                                            if timeout > 0:
                                                pass
                                            else:
                                                result = "timeout"
                                                break
                                    else:
                                        pass
                            if result == "restart":
                                await client.send_message(msg_ch, "それじゃあ次のゲームを始めます！")
                                content_dict = dict()
                                for num in range(1, 10):
                                    content_dict[str(num)] = "　"
                            else:
                                await client.send_message(msg_ch, draw_content[result].format(message.author.id))
                                break
                        else:
                            await client.send_message(msg_ch, result_content[result].format(message.author.id))
                            break
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

client.run("Token")
