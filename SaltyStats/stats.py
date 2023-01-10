import re
import sqlite3
from Match import CurMatchData
from Match import MatchData
from datetime import datetime


def run():
    def sql_run(data, y):
        conn = sqlite3.connect('salty.db')
        c = conn.cursor()

        if y == 0:

            c.execute("SELECT * FROM CurMatch WHERE date=?", (str(data.date),))

            if not c.fetchone():
                print("Next Match Starting Soon!")
                c.execute("INSERT or REPLACE INTO CurMatch (date,c_red_char,c_blue_char,tier) VALUES (?,?,?,?)",
                          (data.date, data.c_red_char, data.c_blue_char, data.tier))

            conn.commit()

        if y == 1:
            c.execute("SELECT * FROM MatchStats WHERE date=?", (str(data.date),))

            if not c.fetchone():
                print(data.date, "submitted")
                c.execute("INSERT INTO MatchStats VALUES (?,?,?,?,?,?)",
                          (data.date, data.winner, data.red_char, data.red_bet,
                           data.blue_char, data.blue_bet))
                conn.commit()

        conn.close()

    def msg_parse(inc_message, y):
        index_list = []
        print("inc message: ", y , inc_message)
        # BETTING OPEN PARSE
        if y == 0:
            inc_message = inc_message[0].split(' ')[4:-2]
            print("#41", inc_message)#TS

            index_list.append(inc_message.index('vs'))
            t_red_char = " ".join(inc_message[:index_list[0]])
            t_blue_char = " ".join(inc_message[1+index_list[0]:-3])
            print("#47", t_blue_char)
            t_blue_char = " ".join(t_blue_char.split(" "))[:-1]
            print("#49", t_blue_char)

            if "(Requested" in inc_message:
                t_blue_char = t_blue_char.split("(")[0]#TS
                t_blue_char = t_blue_char[:-2]#TS
                print("Requested 0:", t_blue_char)

            if 'Tier)' in inc_message:
                t_tier = " ".join(inc_message[1 + index_list[0]:])
                t_index = t_tier.index("Tier)")
                t_tier = t_tier[:t_index+5]
                t_tier = t_tier.split("!")[1:][0][1:]
                t_tier = t_tier[1:-1]
                print("Tier 0", t_tier)
                
            else:
                t_tier = "N/A"

            return t_tier, t_red_char, t_blue_char

        # BETTING CLOSED PARSE
        if y == 1:
            for index, item in enumerate(inc_message):
                if "$" in item:
                    index_list.append(index)

            red_char_name = inc_message[:index_list[0]]
            length = len(red_char_name)
            if red_char_name[length - 1] == "-":
                red_char_name = " ".join(red_char_name[:length - 2])
            else:
                red_char_name = " ".join(red_char_name)[:-1]

            blue_char_name = inc_message[index_list[0] + 1:index_list[1]]
            length = len(blue_char_name)
            if blue_char_name[length - 1] == "-":
                blue_char_name = " ".join(blue_char_name[:length - 2])
            else:
                blue_char_name = " ".join(blue_char_name)[:-1]

            red_char_price = inc_message[index_list[0]]
            red_char_price = int(red_char_price[1:-1].replace(",", ""))
            blue_char_price = inc_message[index_list[1]]
            blue_char_price = int(blue_char_price[1:].replace(",", ""))

            return red_char_name, red_char_price, blue_char_name, blue_char_price

        # BETTING WON PARSE
        elif y == 2:
            for index, item in enumerate(inc_message):
                if "wins!" in item:
                    winner_winner_chicken_dinner = " ".join(inc_message[0:index])
                    return winner_winner_chicken_dinner

    file = 'chat.log'
    with open(file, encoding="utf-8") as f:
        lines = f.read().splitlines()

    match_details = []

    for msg in lines:
        if msg[0:4].isnumeric():
            time_logged = msg.split()[0].strip()
            time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')
            username_message = msg.split('—')[1:]
            username_message = '—'.join(username_message).strip()
            bets_open = re.search("Bets are OPEN for", username_message)
            bets_locked = re.search("Bets are locked", username_message)
            bets_won = re.search("wins! Payouts to", username_message)
            print("#113 - presplit 0", msg)

            if bets_open:
                bets_open = msg.split(":")[4:]
                print("#118 - preparse 0", bets_open)#TS
                # Message Parse
                date = time_logged
                match_betting_details = msg_parse(bets_open, 0)
                tier = match_betting_details[0]
                c_red_char = match_betting_details[1]
                c_blue_char = match_betting_details[2]
                current_data = CurMatchData(date, c_red_char, c_blue_char, tier)

                sql_run(current_data, 0)

            elif bets_locked:
                bets_locked = msg.split(":")[4:]
                print("#131 - preparse 1", bets_locked)
                bets_locked = bets_locked[0].split(' ')[3:]
                if len(bets_locked) <= 1:
                    bets_locked = msg.split(" ")[4:]
                    bets_locked = bets_locked[4:]

                # Message Parse
                match_details = msg_parse(bets_locked, 1)

            elif bets_won:
                bets_won = msg.split(":")[4:]
                bets_won = bets_won[0].split(' ')

                if len(bets_won) <= 1:
                    bets_won = msg.split(" ")[4:]
                    og_bets_won = bets_won[1:]
                    og_bets_won[0] = og_bets_won[0][1:]
                    bets_won = og_bets_won
                    print("#149 - preparse 2", bets_won)

                # Message Parse
                if match_details:
                    date = time_logged
                    winner = msg_parse(bets_won, 2)
                    red_char = match_details[0]
                    red_bet = match_details[1]
                    blue_char = match_details[2]
                    blue_bet = match_details[3]

                    last_match = MatchData(date, winner, red_char, red_bet, blue_char, blue_bet)
                    sql_run(last_match, 1)

            bets_open = None
            bets_locked = None
            bets_won = None


run()
