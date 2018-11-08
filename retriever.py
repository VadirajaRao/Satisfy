"""Program to retrieve data from the database."""
import mysql.connector as con


class retrieve (object):
    """Functions for various retrievals."""
    def __init__ (self):
        self.sat = con.connect (
            host = "localhost",
            user = "vadi",
            passwd = "Vadi@1998",
            database = "satisfy"
        )
        self.cur = self.sat.cursor()

    def get_uid(self, mail):
        """Retruns uid using mail."""
        sql = 'select uid from user_mail where mail = %s'
        val = (mail, )

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]