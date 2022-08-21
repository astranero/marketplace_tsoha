from app import db

class MessageManager():
    def __init__(self, sender=None, message_id=None, message=None, receiver="admin", tag="normal"):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.message_id = message_id
        self.tag = tag

    def insert_message(self):
        sql = """INSERT INTO messages (sender, receiver, message, tag)
        VALUES (:sender, :receiver, :message, :tag);"""
        db.session.execute(
            sql, {"sender": self.sender,
                  "receiver": self.receiver,
                  "message": self.message,
                  "tag": self.tag})
        db.session.commit()

    def fetch_messages(self):
        sql = """(SELECT id, sender, receiver, message, creation_date
        FROM messages
        WHERE sender=:sender AND  receiver=:receiver AND tag='normal')
        UNION ALL (
            SELECT id, sender, receiver, message, creation_date
            FROM messages WHERE sender=:receiver AND receiver=:sender AND tag='normal')
        ORDER BY creation_date ASC;"""
        data = db.session.execute(sql, {"sender": self.sender,
                                        "receiver": self.receiver}).fetchall()
        db.session.commit()
        return data

    def fetch_contact_messages(self):
        sql = """SELECT message_id, sender, receiver, message, creation_date
        FROM messages WHERE tag='contact-us'
        ORDER BY creation_date ASC;"""
        data = db.session.execute(sql).fetchall()
        return data

    def fetch_report_messages(self):
        sql = """SELECT message_id, sender, receiver, message, creation_date
        FROM messages
        WHERE tag='report'
        ORDER BY creation_date ASC;"""
        data = db.session.execute(sql).fetchall()
        db.session.commit()
        return data

    def delete_messages(self):
        sql = """DELETE FROM messages
        WHERE receiver=:receiver AND sender=:sender;"""
        db.session.execute(sql, {"receiver": self.receiver,
        "sender": self.sender})
        db.session.commit()

    def fetch_senders(self):
        sql = """SELECT COUNT(id), sender
        FROM messages
        WHERE receiver=:receiver
        GROUP BY sender;"""
        data = db.session.execute(sql, {"receiver": self.receiver}).fetchall()
        if data:
            return data
        return None

    def fetch_receivers(self):
        sql = """SELECT COUNT(id), receiver
        FROM messages WHERE sender=:sender
        GROUP BY receiver;"""
        data = db.session.execute(sql, {"sender": self.sender}).fetchall()
        if data:
            return data
        return None

    def delete_message(self, message_id):
        sql = "DELETE FROM messages WHERE id=:id;"
        db.session.execute(sql, {"id": message_id})
        db.session.commit()


class CommentManager():
    def __init__(self, comment=None, product_id=None, comment_id=None, username=None):
        self.comment = comment
        self.product_id = product_id
        self.comment_id = comment_id
        self.commentor_username = username

    def insert_comments(self):
        sql = """INSERT INTO comments (user_comment, product_id, commentor_username)
        VALUES (:user_comment, :product_id, :commentor_username); """
        db.session.execute(sql, {"user_comment": self.comment,
                           "product_id": self.product_id,
                                 "commentor_username": self.commentor_username})
        db.session.commit()

    def fetch_comments(self):
        sql = """SELECT id, user_comment, product_id, commentor_username, creation_date
        FROM comments WHERE product_id=:product_id
        ORDER BY creation_date DESC;"""
        return db.session.execute(sql, {"product_id": self.product_id}).fetchall()

    def delete_comment(self):
        sql = """DELETE FROM comments
        WHERE id=:comment_id;"""
        db.session.execute(sql, {"comment_id": self.comment_id})
        db.session.commit()
