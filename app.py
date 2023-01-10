from flask import Flask
from flask import Response
from flask import render_template
import Match
import SQL
import os

from Char import Char

app = Flask(__name__)

@app.route('/char_stats/<char>')
def page2(char):
    # Char stat page whenever you click a character name on the index.
    # Would work for searches as well
    stats = Char(SQL.char(char), char)
    return render_template("char_stats.html", stats=stats)

@app.route('/')
def hello_world():
    # total matches played
    count = SQL.run()

    # SQL query about the last match, make it into an object.
    last_match = Match.LastMatch(SQL.last_match())

    # SQL query about the next match, make it into an object.
    next_match = Match.NextMatch(SQL.next_match())

    # SQL query for next match by character of red then blue, make the data into an object.
    next_red_stats = Char(SQL.char(next_match.red_name), next_match.red_name)
    next_blue_stats = Char(SQL.char(next_match.blue_name), next_match.blue_name)

    # Determine victor of last match to update hex color for text.
    if last_match.winner in last_match.red_name:
        win_color = "#dc3561"  # red team
    else:
        win_color = "#1d7bff"  # blue team

    return render_template("index.html", latest_match=last_match, count=count[0][0], win_color=win_color,
                           next_match=next_match, next_red_stats=next_red_stats, next_blue_stats=next_blue_stats)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
