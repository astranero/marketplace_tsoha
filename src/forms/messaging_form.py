
from flask_wtf import FlaskForm
from wtforms import(
    StringField,
    validators,
    ValidationError,
    TextAreaField)

from flask_login import current_user
from markupsafe import Markup
from src.models.messaging_models import MessageManager
from src.models.user_model import check_username

class MessageForm(FlaskForm):
    sender = StringField("sender", [validators.Length(
        min=4, max=40),
        validators.Email(message="Username format is incorrect."),
        validators.DataRequired()])
    receiver = StringField("receiver", [
        validators.Length(min=4, max=40),
        validators.Email(message="Username format is incorrect."),
        validators.DataRequired()])
    message = TextAreaField("message",
                            [validators.Length(min=0),
                             validators.DataRequired()])

    def validate_receiver(self, receiver):
        username_exists = check_username(receiver)
        if not username_exists:
            raise ValidationError("Username doesn't exist")

    def validate_sender(self, sender):
        username = current_user.username
        if sender == username:
            raise ValidationError("You can't send message to yourself.")

    def send_message(self, sender, receiver, message):
        if receiver != sender:
            message = MessageManager(
                sender=sender, receiver=receiver, message=message)
            message.insert_message()
            return True
        return False

    def send_report(self, sender, message):
        message = MessageManager(sender=sender, message=message, tag="report")
        message.insert_message()


class CommentReportForm(FlaskForm):
    sender = StringField("sender", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    reported = StringField("reported", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    product_id = StringField("product_id", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    comment_id = StringField("comment_id", [validators.Length(
        min=4, max=40), validators.DataRequired()])
    comment = StringField("comment", [validators.Length(
        min=0, max=350), validators.DataRequired()])
    message = TextAreaField("message", [validators.Length(
        min=0), validators.DataRequired()])

    def validate_reported(self, reported):
        username_exists = check_username(reported)
        if not username_exists:
            raise ValidationError(
                Markup("Username doesn't exist"))

    def validate_sender(self, sender):
        username = current_user.username
        if sender == username:
            raise ValidationError("You can't send message to yourself.")

    def send_report(self, sender, message):
        message = MessageManager(sender=sender, message=message, tag="report")
        message.insert_message()
