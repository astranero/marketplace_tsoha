from src.views import app, views
app.register_blueprint(views, url_prefix="/")