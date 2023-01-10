class Char:
    def __init__(self, data, name):
        # STATS FOR CHAR
        # CONSTANT STATS

        self.name = name
        self.total_matches = len(data)  # Total Matches seen by name
        self.wins = 0
        self.losses = 0
        self.streak = 0
        self.w_percent = 0
        self.largest_bet = 0
        self.total_bet = 0
        self.avg_bet = 0
        self.big_ratio = 0
        self.big_ratio_for = ""
        self.big_ratio_winner = ""
        self.upset_victory = 0
        self.upset_defeat = 0

        for i, each in enumerate(data):
            # CONSTANTS
            date = data[i][0]
            winner = data[i][1]
            red_char = data[i][2]
            red_bet = data[i][3]
            blue_char = data[i][4]
            blue_bet = data[i][5]
            side = ""

            if name == red_char:
                side = "red"
            else:
                side = "blue"

            if winner == name:
                self.wins += 1  # Total Wins by name
                if self.wins > 0:
                    self.w_percent = 100 * (self.wins / self.total_matches)

                if self.streak >= 0:
                    self.streak = -1
                else:
                    self.streak += -1
            else:
                self.losses += 1  # Total Losses by name

                if self.wins > 0:
                    self.w_percent = 100*(self.wins / self.total_matches)

                if self.streak >= 0:
                    self.streak = -1
                else:
                    self.streak += -1

            # Largest bet on name
            if blue_char == name:
                if blue_bet > self.largest_bet:
                    self.largest_bet = blue_bet
            else:
                if red_bet > self.largest_bet:
                    self.largest_bet = red_bet

            # Total bet amount on name
            if blue_char == name:
                self.total_bet += blue_bet
            elif red_char == name:
                self.total_bet += red_bet

            # Average bet amount on name
            self.avg_bet = round(self.total_bet / self.total_matches, 1)

            # Largest Bet Ratio Match
            denominator = min(red_bet, blue_bet)
            numerator = max(red_bet, blue_bet)
            ratio = round(numerator / denominator, 0)
            if ratio > self.big_ratio:
                self.big_ratio = ratio
                if red_bet == max(red_bet, blue_bet):
                    if side == "red":
                        if winner == self.name:
                            self.big_ratio_for = "FOR (won)"
                        else:
                            self.big_ratio_for = "FOR (lost)"
                    else:
                        if winner == self.name:
                            self.big_ratio_for = "AGAINST (won)"
                        else:
                            self.big_ratio_for = "AGAINST (lost)"
                else:
                    if side == "blue":
                        if winner == self.name:
                            self.big_ratio_for = "FOR (won)"
                        else:
                            self.big_ratio_for = "FOR (lost)"
                    else:
                        if winner == self.name:
                            self.big_ratio_for = "AGAINST (won)"
                        else:
                            self.big_ratio_for = "AGAINST (lost)"

            # Upset Victories (Wins with ratio > 2:1)
            if ratio > 2:
                if winner == name:
                    self.upset_victory += 1
                else:
                    self.upset_defeat += 1
