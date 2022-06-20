class AuthManager:
    def __init__(self, app):
        self.app = app             # store the app instance
        self.logged_in_user = None # logged in user data
    
    @property
    def logged_in_user_id(self):
        """ Return the id of the logged in user. """
        if self.logged_in_user: # if user is logged in
            return self.logged_in_user[0]
        else: # if no user logged in
            return None

    @property
    def logged_in_user_role(self):
        """ Return the id of the logged in user. """
        if self.logged_in_user: # if user is logged in
            return self.logged_in_user[-1]
        else: # if no user logged in
            return None

    def authenticate_user(self, email, password):
        user = self.app.db.select_user_by_email_password(email, password) # get user with this email and password
        if user: return user # if such user exists
        return None          # if such a user doesn't exist
    
    def login_user(self, email, password):
        user = self.authenticate_user(email, password)
        if user:
            self.logged_in_user = user # set logged in user
            return True
        else:
            return False

    def logout_user(self):
        self.logged_in_user = None               # reset logged in user
        self.app.home_page.show()                # redirect to home page
        self.app.navbar.show_login_page_btn()    # show login page button
        self.app.navbar.show_register_page_btn() # show register page button

    def register_user(self, first_name, last_name, email, password):
        # check if user with this email exists
        user = self.app.db.select_user_by_email(email)
        if user: return False

        # register user
        self.app.db.insert_user(first_name, last_name, email, password)
        return True