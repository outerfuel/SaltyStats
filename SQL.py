import sqlite3


def run():
    conn = sqlite3.connect('salty.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM MatchStats")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

    # Gathers current match details


def next_match():
    conn = sqlite3.connect('salty.db')
    c = conn.cursor()
    c.execute("SELECT * FROM CurMatch ORDER BY date DESC LIMIT 1")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

    # Gathers last match details


def last_match():
    conn = sqlite3.connect('salty.db')
    c = conn.cursor()
    c.execute("SELECT * FROM MatchStats ORDER BY date DESC LIMIT 1")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

    # Gathers all matches of specific character (red or blue)


def char(char):
    conn = sqlite3.connect('salty.db')
    c = conn.cursor()
    c.execute("SELECT * FROM MatchStats WHERE red_char LIKE ? or blue_char LIKE ?", (char, char))
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data
