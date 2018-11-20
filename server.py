""" This script will run on the server and will keep the site alive. """

from flask import Flask, redirect, url_for, render_template, request, session
from flask_mail import Mail, Message
import insert
import check_credentials
import retriever

app = Flask(__name__)
app.secret_key = "we are the best"

mail = Mail(app)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "satisfybit@gmail.com"
app.config['MAIL_PASSWORD'] = "laferrar1"
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
    distance = ret.get_tot_dist(uid)
    speed = ret.get_fin_speed(uid)
    return render_template('/home.html', time = ttime, distance = distance, speed = speed)

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
        distance = request.form['distance']
        time = request.form['duration']
        type = request.form['type']
        sdate = request.form['start_date']
        edate = request.form['end_date']

        cid = db.insert_challenge(distance, time, type, sdate, edate)
        uid = ret.get_uid(session['username'])
        db.insert_participate(cid, uid)
        clear = True

    if not clear:
        return render_template('/cchallenge.html')
    else:
        return redirect(url_for('homepage'))

@app.route('/history')
def history():
    uid = ret.get_uid(session['username'])
    res = ret.get_all_runs(uid)

    return render_template('/history.html', runs = res)

@app.route('/challenges')
def challenges():
    uid = ret.get_uid(session['username'])
    challenges = ret.get_all_challenges(uid)
    return render_template('/challengelist.html', res = challenges)

@app.route('/friends', methods = ['POST', 'GET'])
def friends():
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

        else:
            error = "User does not exist"
            return render_template('/friends.html', error = error)

        clear = True

    if not clear:
        return render_template('/friends.html')
    else:
        return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.debug = True
    app.run(ssl_context = 'adhoc')