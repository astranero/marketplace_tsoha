from routes import db


class MessageManager():
    def __init__(self, sender, message, receiver="admin", tag="normal"):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.tag = tag

    def insert_message(self):
        SQL = "INSERT INTO messages (sender, receiver, message, tag) VALUES (:sender, :receiver, :message, :tag);"
        db.session.execute(
            SQL, {"sender": self.sender, "receiver": self.receiver, "message": self.message, "tag": self.tag})
        db.session.commit()

    def fetch_messages(sender, receiver):
        SQL = """(SELECT id, sender, receiver, message, creation_date FROM messages WHERE sender=:sender AND  receiver=:receiver AND tag="normal") 
        UNION ALL (SELECT id, sender, receiver, message, creation_date FROM messages WHERE sender=:receiver AND receiver=:sender AND tag="normal") ORDER BY creation_date ASC;"""
        data = db.session.execute(
            SQL, {"sender": sender, "receiver": receiver}).fetchall()
        db.session.commit()
        return data

    def delete_messages(sender, receiver):
        SQL = "DELETE FROM messages WHERE receiver=:receiver AND sender=:sender;"
        db.session.execute(SQL, {"receiver": receiver, "sender": sender})
        db.session.commit()

    def fetch_senders(receiver):
        SQL = "SELECT COUNT(id), sender FROM messages WHERE receiver=:receiver GROUP BY sender;"
        data = db.session.execute(SQL, {"receiver": receiver}).fetchall()
        db.session.commit()
        if data:
            return data

    def fetch_receivers(sender):
        SQL = "SELECT COUNT(id), receiver FROM messages WHERE sender=:sender GROUP BY receiver;"
        data = db.session.execute(SQL, {"sender": sender}).fetchall()
        db.session.commit()
        if data:
            return data

    def fetch_contact_messages():
        SQL = """SELECT message_id, sender, receiver, message, creation_date FROM messages WHERE tag="admin" ORDER BY creation_date ASC;"""
        data = db.session.execute(
            SQL).fetchall()
        db.session.commit()
        return data
        
    def fetch_report_messages():
        SQL = """SELECT message_id, sender, receiver, message, creation_date FROM messages WHERE tag="contact-us" ORDER BY creation_date ASC;"""
        data = db.session.execute(
            SQL).fetchall()
        db.session.commit()
        return data

    def delete_message(id):
        SQL = "DELETE FROM messages WHERE id=:id;"
        db.session.execute(SQL, {"id": id})
        db.session.commit()