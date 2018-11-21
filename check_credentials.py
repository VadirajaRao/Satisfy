import mysql.connector as con

class credentials(object):
    """Functions to check the credentials of a user at various points."""
    def __init__(self):
        """Creating connection to the database and creating a cursor."""
        self.sat = con.connect(
            host = "localhost",
            user = "vadi",
            passwd = "Vadi@1998",
            database = "satisfy"
        )
        self.cur = self.sat.cursor(buffered=True)

    def login(self, mail, passwd):
        """This function checks for the necessary fields which ensures the user is legit."""
        self.cur.execute('select uid from user_mail where mail = %s', mail)

        uid_t = self.cur.fetchone()

        self.cur.execute('select passwd from user where uid = %s', uid_t)

        obtain_t = self.cur.fetchone()
        obtain = obtain_t[0]

        if obtain == passwd:
            return True
        else:
            return False

    def signup (self, mail):
        """Check if there is an already existing user with the mail id provided."""
        args = [mail, 0]
        result = self.cur.callproc('user_exists', args) # 'user_exists' is a stored procedure.

        if result == None:
            return False
        elif len(result) == 0:
            return False
        else:
            return True