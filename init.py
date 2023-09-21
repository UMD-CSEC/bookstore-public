import os
import sqlite3

if os.path.exists("database.db"):
    os.remove("database.db")

con1 = sqlite3.connect("database.db")
cur1 = con1.cursor()

if os.path.exists("static/bookstore.db"):
    os.remove("static/bookstore.db")

con2 = sqlite3.connect("static/bookstore.db")
cur2 = con2.cursor()

CREATE_BOOKS = """
    CREATE TABLE books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        img TEXT,
        price INTEGER,
        hidden BOOLEAN NOT NULL CHECK (hidden IN (0, 1)),
        justification TEXT
    )
    """

FLAG_BOOK = [[0, "FLAG_PLACEHOLDER1", "clarence \"anime\" lam", "/static/mangaguide.jpg", 28999, 1, "FLAG_PLACEHOLDER2"]]
FAKE_BOOKS = [
    [1, "Preventing Buffer Overflows", 'kevin "ok pwn time" higgs', "/static/cover1.png", 7999, 0, "kmh teach us heap"],
    [2, "Methods of generating secure root passwords", "Triacontakai", "/static/cover2.png", 3999, 0, "my root password is a"],
    [3, "Writing Perfect Code the First Time", 'Edw "I use Copilot" Feng', "/static/cover3.jpg", 19999, 0, "how to stop using chatgpt"],
    [4, "i swear functional programming has useful applications trust me", "edwfeng", "/static/cover4.png", 99999, 0, "it doesnt"],
    [5, "Dirty COW", "Triacontakai", "/static/cover5.jpg", 1103700, 0, "wtmoo easy beginner topics"],
    [6, "Math was never meant to be applied", "clam", "/static/cover6.png", 7999, 0, "number theory"],
    [7, "Writing impossible ML challenges", "Segal", "/static/cover7.jpg", 72700, 0, "french baguettes cloud blockchain ai machine learning buzzwords"],
    [8, "Graphic Design For The Passionate", "alexandra \"imdm\" maric", "/static/graphicdesign.jpg", 350, 0, "graphic design is my passion"],
]

cur1.execute(CREATE_BOOKS)
cur2.execute(CREATE_BOOKS)
cur1.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)", FLAG_BOOK + FAKE_BOOKS)
cur2.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)", FAKE_BOOKS)

CREATE_COUPONS = """
    CREATE TABLE coupons (
        id INTEGER PRIMARY KEY,
        code TEXT,
        discount INTEGER
    )
    """

FLAG_COUPON = [[9, "FLAG_PLACEHOLDER3", 100]]
FAKE_COUPONS = [
    [0, "differential tuition", -15],
    [1, "literally nothing", 0],
    [2, "deans discount", 10],
    [3, "presidents pension", 50],
    [4, "banneker/key but not quite", 99],
]

cur1.execute(CREATE_COUPONS)
cur2.execute(CREATE_COUPONS)
cur1.executemany("INSERT INTO coupons VALUES (?, ?, ?)", FAKE_COUPONS + FLAG_COUPON)
cur2.executemany("INSERT INTO coupons VALUES (?, ?, ?)", FAKE_COUPONS)

con1.commit()
con1.close()

con2.commit()
con2.close()


if os.path.exists("auth.db"):
    os.remove("auth.db")

auth = sqlite3.connect("auth.db")
cur3 = auth.cursor()

cur3.execute(
    """CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )"""
)
cur3.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    [1, "admin", "FLAG_PLACEHOLDER4"],
)

auth.commit()
auth.close()
