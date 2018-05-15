from queries import Queries

class User():

    def __init__(self, email, password):
        self.email = email
        q = Queries()
        self.resultado_login = q.query_padrao(query_text='SELECT * from usuarios.users where email = "%s" and senha = "%s";' % (email,password))
        self.authenticated = False

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self, email):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        if self.resultado_login:
            self.authenticated = True
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False