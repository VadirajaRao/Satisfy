""" This script will run on the server and will keep the site alive. """

from flask import Flask, redirect, url_for, render_template, request, session
from flask_mail import Mail, Message
import insert
import check_credentials
import retriever

app = Flask(__name__)
app.secret_key = "we are the best"

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'satisfybit@gmail.com'
app.config['MAIL_PASSWORD'] = 'yamaha@mt_10'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = insert.insert_val()
check = check_credentials.credentials()
ret = retriever.retrieve()

@app.route('/', methods=['POST', 'GET'])
def main_page():
    """This function will load the main page of the website."""
    if 'username' in session:
        return redirect(url_for('homepage'))

    clear = False
    exists = False
    perror = ""
    if request.method == 'POST':
        mail = request.form['mail']
        passwd = request.form['passwd']

        mailid = (mail, )
        exists = check.signup(mail)
        
        if exists:
            clear = check.login(mailid, passwd)
            if not clear:
                perror = "Incorrect password"
        else:
            uerror = "Invalid username"
            return render_template('/index.html', uerror = uerror)

        if clear:
            session['username'] = mail

    if not clear:
        return render_template('/index.html', perror = perror)
    else:
        return redirect(url_for('homepage'))

@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    """This function will be executed when the sign-up option is selected.
    'mail id' is considered to be mandatory. If the mail id is given, then it will redirect to home page else the page reloads.
    """
    clear = False
    user_exists = False
    if request.method == 'POST':
        mail = request.form['mail']
        fname = request.form['fname']
        lname = request.form['lname']
        passwd = request.form['passwd']
        rpasswd = request.form['rpasswd']
        dob = request.form['dob']
        city = request.form['city']
        height = request.form['height']
        weight = request.form['weight']

        user_exists = check.signup(mail)

        if user_exists:
            message = "User already exists with this mail id."
            return render_template('/signup.html', existing_user = message)
        else:
            db.insert_user(mail, fname, lname, passwd, dob, city, height, weight)

        if not passwd == rpasswd:
            message = "The password is not repeated correctly."
            return render_template('/signup.html', not_matching_passwd = message)
        
        clear = True

    if not clear:
        return render_template('/signup.html')
    else:
        session['username'] = mail
        return render_template('/home.html')

@app.route('/home')
def homepage():
    uid = ret.get_uid(session['username'])

    ttime = ret.get_tot_time(uid)
    hours = int(ttime / 60)
    minutes = int(ttime - (hours * 60))
    sec = int((ttime - int(ttime)) * 60)
    fin_time = str(hours) + " : " + str(minutes) + " : " + str(sec)

    distance = ret.get_tot_dist(uid)
    
    speed = ret.get_fin_speed(uid)
    min = int(speed)
    sec = int((speed - min) * 60)
    perkm = str(min) + "' " + str(sec) + '" '
    return render_template('/home.html', time = fin_time, distance = distance, speed = perkm)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))

@app.route('/addrun', methods=['POST', 'GET'])
def addrun():
    clear = False
    run_num = 0
    uid = 0
    rdate = ''
    if request.method == 'POST':
        dist_km = request.form['dist_km']
        dist_m = request.form['dist_m']

        time_hours = request.form['time_hours']
        time_min = request.form['time_min']
        time_sec = request.form['time_sec']

        type = request.form['type']
        rdate = request.form['date']

        uid = ret.get_uid(session['username'])

        run_num = ret.get_run_num(uid, rdate)
        if run_num == None:
            run_num = 1
        else:
            run_num = int(run_num) + 1

        dist = float(dist_km) + (float(dist_m) / 1000)
        time = (float(time_hours) * 60) + float(time_min) + (float(time_sec) / 60)
        db.insert_run(uid, rdate, run_num, dist, time, type)

        speed = time / dist
        db.insert_run_speed(uid, rdate, run_num, speed)

        tot_speed = ret.get_tot_speed(uid)
        tot_runs = ret.get_number_of_runs(uid)

        new_speed = ((tot_speed * tot_runs) + speed) / (tot_runs + 1)

        db.update_user_speed(uid, new_speed)
        clear = True

    if not clear:
        return render_template('/addrun.html')
    else:
        ret.make_commit() # To make sure the changes made by the trigger are committed.
        return redirect(url_for('homepage'))

@app.route('/create_challenge', methods = ['POST', 'GET'])
def create_challenge():
    clear = False
    if request.method == 'POST':
        distance_km = request.form['km']
        distance_m = request.form['m']
        tot_distance = float(distance_km) + (float(distance_m) / 1000)
        hours = request.form['hours']
        minutes = request.form['minutes']
        sec = request.form['sec']
        tot_time = (int(hours * 60)) + (float(minutes)) + (float(sec) / 60)
        type = request.form['type']
        sdate = request.form['start_date']
        edate = request.form['end_date']
        mail_list = []
        mail_list.insert(0, request.form['mail1'])
        mail_list.insert(1, request.form['mail2'])
        mail_list.insert(2, request.form['mail3'])
        mail_list.insert(3, request.form['mail4'])

        print("\n" + str(mail_list) + "\n")

        friend_list = ret.get_all_friends(ret.get_uid(session['username']))
        print("\nBefore : " + str(friend_list) + "\n")
        temp = []
        for friend in friend_list:
            temp.append(friend[0])
        print("\nAfter : " + str(temp) + "\n")
        uid_list = []
        uid_list.append(ret.get_uid(session['username']))

        for mail_id in mail_list:
            if mail_id == "none":
                continue
            
            if check.signup(mail_id):
                fid = ret.get_uid(mail_id)
                if fid in temp:
                    msg = Message('You have a new challenge!!', sender = 'satisfybit@gmail.com', recipients=[mail_id])
                    uid = ret.get_uid(session['username'])
                    uid_list.append(fid)
                    fname = ret.get_fname(uid)
                    lname = ret.get_lname(uid)
                    msg.body = fname + " " + lname + " has posed you a new challenge!!"
                    mail.send(msg)
                else:
                    not_friend = "One or more users are not your friend."
                    return render_template('/cchallenge.html', no_user = not_friend)
            else:
                user_does_not_exist = "User does not exist."
                return render_template('/cchallenge.html', no_user = user_does_not_exist)

        cid = db.insert_challenge(tot_distance, tot_time, type, sdate, edate)
        ret.make_commit()
        for uid in uid_list:
            db.insert_participate(cid, uid)
        clear = True

    if not clear:
        return render_template('/cchallenge.html')
    else:
        return redirect(url_for('challenges'))

@app.route('/history')
def history():
    uid = ret.get_uid(session['username'])
    res = ret.get_all_runs(uid)

    final = []
    temp = []
    for tuple in res:
        temp.clear()
        temp.insert(0, tuple[0])
        hours = int(tuple[1] / 60)
        minutes = int(tuple[1] - (hours * 60))
        sec = int((tuple[1] - int(tuple[1])) * 60)
        
        temp.insert(1 , (str(hours) + " : " + str(minutes) + " : " + str(sec)) )
        
        temp.insert(2, tuple[2])

        min = int(tuple[3])
        sec = int((tuple[3] - min) * 60)
        perkm = str(min) + "' " + str(sec) + '" '
        temp.insert(3, perkm)
        final.append(temp)

    return render_template('/history.html', runs = final)

@app.route('/challenges')
def challenges():
    uid = ret.get_uid(session['username'])
    challenges = ret.get_all_challenges(uid)
    temp = []
    final = []
    for challenge in challenges:
        temp.clear()
        temp.insert(0, challenge[0])

        hours = int(challenge[1] / 60)
        minutes = int(challenge[1] - (hours * 60))
        sec = int((challenge[1] - int(challenge[1])) * 60)
        temp.insert(1, (str(hours) + " : " + str(minutes) + " : " + str(sec)))

        temp.insert(2, challenge[2])
        temp.insert(3, challenge[3])
        temp.insert(4, challenge[4])
        final.append(temp)

    print("\n\nChallenges : " + str(final) + "\n\n")
    return render_template('/challengelist.html', res = final)

@app.route('/friends', methods = ['POST', 'GET'])
def friends():
    friend_list = ret.get_all_friends(ret.get_uid(session['username']))
    name_list = []
    for friend in friend_list:
        name = ret.get_fname(friend[0]) + " " + ret.get_lname(friend[0])
        name_list.append(name)

    print(name_list)
    
    clear = False
    exists = False
    if request.method == 'POST':
        mail_id = request.form['mail']
        exists = check.signup(mail_id)
        if exists:
            msg = Message('You have a new friend!!', sender = 'satisfybit@gmail.com', recipients=[mail_id])
            uid = ret.get_uid(session['username'])
            fname = ret.get_fname(uid)
            lname = ret.get_lname(uid)
            msg.body = fname + " " + lname + " has added you as a friend!!"
            mail.send(msg)

            fid = ret.get_uid(mail_id)
            db.insert_friend(uid, fid)

        else:
            error = "User does not exist"
            return render_template('/friends.html', error = error)

        clear = True

    if not clear:
        return render_template('/friends.html', names = name_list)
    else:
        ret.make_commit()
        return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.debug = True
    app.run(ssl_context = 'adhoc')