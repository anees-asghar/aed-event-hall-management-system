class AuthManager:
    def __init__(self, db, app):
        self.db = db
        self.app = app
        self.logged_in_user_id = None

    def authenticate_user(self, email, password):
        user = self.db.select_user_by_email_password(email, password) # get user with this email and password
        if user: # if such a user exists return their user id
            return user[0]  # user[0] == user id
        return None # if such a user doesn't exist return None
    
    def login_user(self, email, password):
        user_id = self.authenticate_user(email, password)
        if user_id:
            self.logged_in_user_id = user_id # set logged in user id
            return True
        else:
            return False

    def logout_user(self):
        self.logged_in_user_id = None # set logged in used id to none
        self.app.home_page.show() # redirect to home page
        self.app.navbar.show_login_btn() # show login button in navbar instead of logout

    def register_user(self, first_name, last_name, email, password):
        # check if user with this email exists
        user = self.db.select_user_by_email(email)
        if user: return False

        # register user
        self.db.insert_user(first_name, last_name, email, password)
        return True