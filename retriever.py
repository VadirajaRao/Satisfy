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

    def get_all_runs(self, uid):
        """Retruns the run details of one user."""
        sql = 'select r.dist, r.time, r.rdate, s.speed from run r, run_speed s where r.uid = s.uid and r.run_num = s.run_num and r.rdate = s.rdate and r.uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        result = self.cur.fetchall()
        print("\n\n" + str(result) + "\n\n")

        return result

    def get_all_challenges(self, uid):
        """Returns the challenges of a user."""
        sql = 'select cid from participate where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)

        res = self.cur.fetchall()

        result = []
        sql = 'select dist, time, type, start, end from challenge where cid = %s'
        for i in res:
            val = (i[0], )
            self.cur.execute(sql, val)
            r = self.cur.fetchone()
            result.append(r)

        return result

    def get_fname(self, uid):
        """Returns the fname based on uid."""
        sql = 'select fname from user where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        res = self.cur.fetchone()

        return res[0]

    def get_lname(self, uid):
        """returns the lanme based on uid."""
        sql = 'select lname from user where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        res = self.cur.fetchone()

        return res[0]

    def get_tot_speed(self, uid):
        """Returns the average speed based on uid."""
        sql = 'select fin_speed from user_speed where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        res = self.cur.fetchone()

        return res[0]

    def get_number_of_runs(self, uid):
        """Returns the number of runs."""
        sql = 'select count(*) from run where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)
        res = self.cur.fetchone()

        return res[0]

    def get_all_friends(self, uid):
        """Returns all the friends based on uid."""
        sql = 'select fid from friends_of where uid = %s'
        val = (uid, )
        self.cur.execute(sql, val)

        return self.cur.fetchall()

    def make_commit(self):
        """Commit the changes into the database."""
        self.sat.commit()