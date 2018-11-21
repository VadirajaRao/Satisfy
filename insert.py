import mysql.connector as con
import datetime


class insert_val(object):
    """Function that inserts value into various tables."""
    def __init__(self):
        """Function that connects to the database."""
        self.sat = con.connect(
            host = "localhost",
            user = "vadi",
            passwd = "Vadi@1998",
            database = "satisfy"
        )
        self.cur = self.sat.cursor()

    def calculate_age(self, born):
        """To calculate age from date of birth."""
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def insert_user_mail (self, uid, mail):
        """Insert values into user_mail table."""
        sql = 'insert into user_mail(uid, mail) values (%s, %s)'
        val = (uid, mail)
        self.cur.execute(sql, val)
        return

    def insert_user_age (self, uid, age):
        """Insert value into user_age table."""
        sql = 'insert into user_age(uid, age) values (%s, %s)'
        val = (uid, age)
        self.cur.execute(sql, val)
        return

    def insert_user_speed (self, uid):
        """Insert value into user_speed table."""
        val = (uid, 0.0)
        self.cur.execute('insert into user_speed(uid, fin_speed) values (%s, %s)', val)
        return

    """ This function is yet to be completed. """
    def insert_user(self, *args):
        """Insert values into user table."""
        sql = 'insert into user(fname, lname, passwd, dob, city, height, weight, tot_dist, tot_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (args[1], args[2], args[3], args[4], args[5], args[6], args[7], 0.0, 0.0)
        self.cur.execute(sql, val)

        self.cur.execute('select max(uid) from user')
        uid = self.cur.fetchone()
        self.insert_user_mail(uid[0], args[0])

        dob = datetime.datetime.strptime(args[4], "%Y-%m-%d")
        age = self.calculate_age(dob)
        self.insert_user_age(uid[0], age)

        self.insert_user_speed(uid[0])
        self.sat.commit()

    def insert_friend(self, *args):
        """Insert values into friend table."""
        sql = 'insert into friends_of (uid, fid) values (%s, %s)'
        val = (args[0], args[1])
        self.cur.execute(sql, val)
        self.sat.commit()

    def insert_run(self, *args):
        """Insert values into run table."""
        sql = 'insert into run(uid, rdate, run_num, dist, time, type) values (%s, %s, %s, %s, %s, %s)'
        val = (args[0], args[1], args[2], args[3], args[4], args[5])
        self.cur.execute(sql, val)
        self.sat.commit()

    def insert_challenge(self, *args):
        """Insert values into challenge table."""
        sql = 'insert into challenge(dist, time, type, start, end) values (%s, %s, %s, %s, %s)'
        val = (args[0], args[1], args[2], args[3], args[4])
        self.cur.execute(sql, val)
        self.sat.commit()
        self.cur.execute('select max(cid) from challenge')
        res = self.cur.fetchone()
        return res[0]

    def insert_run_speed(self, *args):
        """Insert values into run_speed table."""
        sql = 'insert into run_speed(uid, rdate, run_num, speed) values (%s, %s, %s, %s)'
        val = (args[0], args[1], args[2], args[3])
        self.cur.execute(sql, val)
        self.sat.commit()

    def insert_participate(self, cid, uid):
        """Insert values into participate table."""
        sql = 'insert into participate(cid, uid) values (%s, %s)'
        val = (cid, uid)

        self.cur.execute(sql, val)
        self.sat.commit()

    def update_user_speed(self, uid, fin_speed):
        """Update the final speed of the user."""
        sql = 'update user_speed set fin_speed = %s where uid = %s'
        val = (fin_speed, uid)

        self.cur.execute(sql, val)
        self.sat.commit()