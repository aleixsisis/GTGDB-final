import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row
    return db

def GetAllReviews():
    db = GetDB()
    reviews = db.execute("""SELECT Reviews.id, Reviews.date, Reviews.game, Reviews.score, Reviews.review, Users.username, Reviews.user_id
                            FROM Reviews JOIN Users ON Reviews.user_id = Users.id
                            ORDER BY date DESC""").fetchall()
    db.close()
    return reviews

def CheckLogin(username, password):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=? COLLATE NOCASE", (username,)).fetchone()
    if user and check_password_hash(user['password'], password):
        return user
    return None

def RegisterUser(username, password):
    if username is None or password is None:
        return False
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit()
    return True

def AddReview(user_id, date, game, score, review):
    if date is None or game is None:
        return False
    db = GetDB()
    db.execute("INSERT INTO Reviews(user_id, date, game, score, review) VALUES (?, ?, ?, ?, ?)",
               (user_id, date, game, score, review))
    db.commit()
    return True

def GetReviewById(review_id):
    db = GetDB()
    review = db.execute("SELECT * FROM Reviews WHERE id = ?", (review_id,)).fetchone()
    db.close()
    return review

def UpdateReview(review_id, score, review):
    db = GetDB()
    db.execute("UPDATE Reviews SET score = ?, review = ? WHERE id = ?", (score, review, review_id))
    db.commit()
    db.close()

def DeleteReview(review_id):
    db = GetDB()
    db.execute("DELETE FROM Reviews WHERE id = ?", (review_id,))
    db.commit()
    db.close()

def ResetDatabase():
    db = GetDB()
    db.execute("DELETE FROM Reviews")
    db.execute("DELETE FROM Users")
    db.commit()
    db.close()
