from routes import db
class MessageManager():
    def __init__(self, sender, message, receiver="admin"):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def insert_message(self):
        SQL = "INSERT INTO messages (sender, receiver, message) VALUES (:sender, :receiver, :message);"
        db.session.execute(SQL, {"sender":self.sender,"receiver":self.receiver, "message":self.message})
        db.session.commit()

    def fetch_messages(receiver):
        SQL = "SELECT id, sender, message FROM messages WHERE receiver=:receiver ORDER BY  sender DESC, creation_date DESC;"
        db.session.execute(SQL, {"receiver":receiver})

    def admin_fetch_messages(sender, receiver):
        SQL = "SELECT id, sender, receiver, message FROM messages WHERE sender=:sender AND receiver=:receiver ORDER BY creation_date DESC;"
    
    def delete_message(id):
        SQL = "DELETE FROM messages WHERE id=:id,"
    
    def update_message(id):
        pass