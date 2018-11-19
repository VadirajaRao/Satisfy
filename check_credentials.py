import mysql.connector as con

class credentials(object):
    def __init__(self):
        self.sat = con.connect(
            host = "localhost",
            user = "root",
            passwd = "laferrar1",
            database = "satisfy"
        )
        self.cur = self.sat.cursor(buffered=True)

    def login(self, mail, passwd):
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
        val = (mail, )
        self.cur.execute('select user.uid \
        from user \
        where exists ( select * \
        from user_mail where user.uid = user_mail.uid and user_mail.mail = %s', val)

        result = self.cur.fetchone()

        if len(result) == 0:
            return False
        else:
            return True