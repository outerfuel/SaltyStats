class LastMatch:
    def __init__(self, data):

        self.date = data[0][0]
        self.winner = data[0][1]
        self.red_name = data[0][2]
        self.red_bet = data[0][3]
        self.blue_name = data[0][4]
        self.blue_bet = data[0][5]


class NextMatch:
    def __init__(self, data):

        self.date = data[0][0]
        self.red_name = data[0][1]
        self.blue_name = data[0][2]
        self.tier = data[0][3]


class CurMatchData:
    def __init__(self, date, c_red_char, c_blue_char, tier):
        self.date = date
        self.c_red_char = c_red_char
        self.c_blue_char = c_blue_char
        self.tier = tier


class MatchData:
    def __init__(self, date, winner, red_char, red_bet, blue_char, blue_bet):
        self.date = date
        self.winner = winner
        self.red_char = red_char
        self.red_bet = red_bet
        self.blue_char = blue_char
        self.blue_bet = blue_bet
