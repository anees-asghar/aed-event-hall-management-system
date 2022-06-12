class AuthManager:
    def __init__(self, app):
        self.app = app
        self.db = self.app.db
        self.logged_in_user = None
    
    @property
    def logged_in_user_id(self):
        if self.logged_in_user:
            return self.logged_in_user[0]
        else:
            return None

    @property
    def logged_in_user_role(self):
        if self.logged_in_user:
            if self.logged_in_user[3] == "admin": return "Admin" # TEMPORARY
            return self.logged_in_user[3]
        else:
            return None

    def authenticate_user(self, email, password):
        user = self.db.select_user_by_email_password(email, password) # get user with this email and password
        if user: # if such a user exists return their user id
            return user  # user[0] == user id
        return None # if such a user doesn't exist return None
    
    def login_user(self, email, password):
        user = self.authenticate_user(email, password)
        if user:
            self.logged_in_user = user # set logged in user
            return True
        else:
            return False

    def logout_user(self):
        self.logged_in_user = None               # reser logged in user
        self.app.home_page.show()                # redirect to home page
        self.app.navbar.show_login_page_btn()    # show login page button
        self.app.navbar.show_register_page_btn() # show register page button

    def register_user(self, first_name, last_name, email, password):
        # check if user with this email exists
        user = self.db.select_user_by_email(email)
        if user: return False

        # register user
        self.db.insert_user(first_name, last_name, email, password)
        return True