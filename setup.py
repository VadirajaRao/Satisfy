import mysql.connector

""" Creates a connection object to MySQL server """
satisfy = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    passwd = 'laferrar1',
    database = 'satisfy'
)

""" creating a cursor """
cur = satisfy.cursor()

"""Creating 'user' table """

"""
    uid : int | not null | primary key | auto_increment
    fname : varchar(25) | not null
    lname : varchar(25) | not null
    passwd : varchar(20) | not null
    dob : date | not null
    city : varchar(20) | not null
    height : int | not null
    weight : int | not null
    tot_distance : float | not null
    tot_time : float | not null
"""

cur.execute('create table user (uid int not null primary key auto_increment, fname varchar(25) not null, lname varchar(25) not null, passwd varchar(25) not null, dob date not null, city varchar(25) not null, height int not null, weight int not null, tot_dist float not null, tot_time float not null)')

"""Creating 'friends_of' table"""

"""
    uid : int | foreign key | primary key
    fid : int | foreign key | primary key
"""

cur.execute('create table friends_of (uid int not null, fid int not null, primary key(uid, fid), constraint uid1_fk foreign key(uid) references user(uid) on delete cascade, constraint uid2_fk foreign key(fid) references user(uid) on delete cascade)')

""" Creating 'run' table """

"""
    uid : int | foreign key | primary key
    rdate : date | not null | primary key
    run_num : int | not null | primary key
    distance : float | not null
    time : float | not null
    type : varchar(10) | not null
"""

cur.execute('create table run (uid int not null, rdate date not null, run_num int not null, dist float not null, time float not null, type varchar(10) not null, primary key(uid, rdate, run_num), constraint uid3_fk foreign key(uid) references user(uid) on delete cascade)')

""" Creating 'challenge' table """

"""
    cid : int | not null | auto_increment | primary key
    distance : float | not null
    time : float | not null
    type : varchar(10) | not null
    start : date | not null
    end : date | not null
"""

cur.execute('create table challenge (cid int not null auto_increment primary key, dist float not null, time float not null, type varchar(10) not null, start date not null, end date not null)')

""" Creating 'participate' table """

"""
    cid : int | not null | foreign key | primary key
    uid : int | not null | foreign key | primary key
"""

cur.execute('create table participate (cid int not null, uid int not null, primary key(cid, uid), constraint uid4_fk foreign key(uid) references user(uid) on delete cascade, constraint cid1_fk foreign key(cid) references challenge(cid) on delete cascade)')

""" Creating 'user_mail' table """

"""
    uid  : int | not null | foreign key | primary key
    mail : varchar(30) | not null
"""

cur.execute('create table user_mail (uid int not null primary key, mail varchar(30) not null, constraint uid5_fk foreign key(uid) references user(uid) on delete cascade)')

""" Creating 'user_age' table """

"""
    uid : int | not null | foreign key | primary key
    age : int | not null
"""

cur.execute('create table user_age (uid int not null primary key, age int not null, constraint uid6_fk foreign key(uid) references user(uid) on delete cascade)')

""" Creating 'run_speed' table """

"""
    uid     : int | not null | foreign key | primary key
    rdate   : date | not null | foreign key | primary key
    run_num : int | not null | foreign key | primary key
    speed   : float | not null
"""

cur.execute('create table run_speed (uid int not null, rdate date not null, run_num int not null, speed float not null, primary key(uid, rdate, run_num), constraint uid7_fk foreign key(uid, rdate, run_num) references run(uid, rdate, run_num) on delete cascade)')


""" Creating 'user_speed' table"""

"""
    uid : int | not null | foreign key | primary key
    fin_speed : float | not null
"""

cur.execute('create table user_speed (uid int not null primary key, fin_speed float not null, constraint uid8_fk foreign key(uid) references user(uid) on delete cascade)')

""" Creating trigger."""

cur.execute('delimiter //')
cur.execute('create trigger compute_total before insert on run for each row begin update user set tot_dist = tot_dist + new.dist where user.uid = new.uid; update user set tot_time = tot_time + new.time where user.uid = new.uid; end//')
cur.execute('delimiter ;')

satisfy.commit()