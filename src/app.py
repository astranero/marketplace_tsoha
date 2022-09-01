from src.views import app, views
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run()
