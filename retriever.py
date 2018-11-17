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
        self.cur = self.sat.cursor(buffered = True) # 'bufffered = True' was causing the MySQL errors(unread parameter and arguments missing error). If you get any such errors, check this line.

    def get_uid(self, mail):
        """Retruns uid using mail."""
        sql = 'select uid from user_mail where mail = %s'
        val = (mail, )

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]

    def get_tot_time(self, uid):
        """Returns total time logged."""
        sql = 'select tot_time from user where uid = %s'
        val = (uid, )

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]

    def get_tot_dist(self, uid):
        """Returns total distance coverec."""
        sql = 'select tot_dist from user where uid = %s'
        val = (uid, )

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]

    def get_fin_speed(self, uid):
        """Retruns speed based on total distance and total time."""
        sql = 'select fin_speed from user_speed where uid = %s'
        val = (uid, )

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]

    def get_run_num(self, uid, rdate):
        """Returns the run_num from run table for that particular day."""
        sql = 'select max(run_num) from run where uid = %s and rdate = %s'
        val = (uid, rdate)

        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        return result[0]

    def change_user_tot(self, uid, run_num, rdate):
        """Reflects changes with users total in user table, based on changes in other tables."""
        sql = 'select dist, time from run where uid = "%s" and run_num = "%s" and rdate = "%s"'
        val = (uid, run_num, rdate)
        self.cur.execute(sql, val)
        result = self.cur.fetchone()
        dist = result[0]
        time = result[1]

        sql = 'select tot_dist, tot_time from user where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        result = self.cur.fetchone()
        tot_dist = float(dist) + float(result[0])
        tot_time = float(time) + float(result[1])

        sql = 'update user set tot_dist = %s where uid = %s'
        val = (tot_dist, uid)
        self.cur.execute(sql, val)
        self.sat.commit()

        sql = 'update user set tot_time = %s where uid = %s'
        val = (tot_time, uid)
        self.cur.execute(sql, val)
        self.sat.commit()