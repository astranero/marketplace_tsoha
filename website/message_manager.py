from routes import db
class MessageManager():
    def __init__(self, sender, message, receiver=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def insert_u2u_message(self):
        SQL = "INSERT INTO messages (sender, receiver, message) VALUES (:sender, :receiver, :message);"
        db.session.execute(SQL, {"sender":self.sender,"receiver":self.receiver, "message":self.message})
        db.session.commit()

    def insert_contact_us_message(self):
        SQL = "INSERT INTO contact_us_messages (sender, message) VALUES (:sender, :message);"
        db.session.execute(SQL, {"sender":self.sender, "message":self.message})
        db.session.commit()

    def fetch_messages(receiver):
        SQL = "SELECT id, message FROM messages WHERE receiver=:receiver ORDER BY creation_date DESC;"
        db.session.execute(SQL, {"receiver":receiver})

    def admin_fetch_u2u_messages(sender, receiver):
        SQL = "SELECT id, sender, receiver, message FROM messages WHERE sender=:sender AND receiver=:receiver ORDER BY creation_date DESC;"
    
    def admin_fetch_contact_us_messages():
        SQL = "SELECT id, sender, message FROM contact_us_messages ORDER BY sender DESC, creation_date DESC;"
    
    def delete_u2u_message(id):
        SQL = "DELETE FROM messages WHERE id=:id,"