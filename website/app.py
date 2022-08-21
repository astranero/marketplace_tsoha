from routes import views, login_manager, app, User

@login_manager.user_loader
def user_loader(user_id):
    return User.get(user_id)

def create_app():
    pass

app.register_blueprint(views, url_prefix="/")
if __name__ == "__main__":
    app.run(debug=True)
