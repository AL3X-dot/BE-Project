from flask import Flask, escape, request,render_template, redirect , url_for , flash , session
from flask_mysqldb import MySQL 
import MySQLdb
from tweeter_services import get_followers_following, get_all_tweets , retweet
from model_services import classify_tweets
from googleAPI import get_recommendation

# Google API Key = AIzaSyBD8_Gaq64yP4D1WyLkkHi7UIpjUNJQsxs
app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'BE'
app.secret_key = "Baap"
mysql = MySQL(app)
# app.config['MYSQL_USER'] = 'sql12324433'
# app.config['MYSQL_PASSWORD'] = 'Ra1TUVuM3b'
# app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
# app.config['MYSQL_DB'] = 'sql12324433'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


def max_tweet_score(zoo , restaurant , museum):
    max_zoo , max_restaurant , max_museum = -1 , -1 , -1
    for single_zoo in zoo:
        if max_zoo < single_zoo.tweet_score:
            max_zoo = single_zoo.tweet_score
    for single_restaurant in restaurant:
        if max_restaurant < single_restaurant.tweet_score:
            max_restaurant = single_restaurant.tweet_score
    for single_museum in museum:
        if max_museum < single_restaurant.tweet_score:
            max_museum = single_museum.tweet_score
    return  max_zoo , max_restaurant , max_museum

def category_score(category , max_score):
    sum = 0
    for single_tweet in category:
        sum = sum + single_tweet.tweet_score
    return sum/max_score

def sentiment_score(zoo , restaurant , museum):
    for single_tweet in zoo:
        if single_tweet.sentiment == "Positive":
            single_tweet.tweet_score = single_tweet.tweet_score * 1.25
        elif single_tweet.sentiment == 'Negative':
            single_tweet.tweet_score = single_tweet.tweet_score * 0.75
    
    for single_tweet in restaurant:
        if single_tweet.sentiment == "Positive":
            single_tweet.tweet_score = single_tweet.tweet_score * 1.25
        elif single_tweet.sentiment == 'Negative':
            single_tweet.tweet_score = single_tweet.tweet_score * 0.75

    for single_tweet in museum:
        if single_tweet.sentiment == "Positive":
            single_tweet.tweet_score = single_tweet.tweet_score * 1.25
        elif single_tweet.sentiment == 'Negative':
            single_tweet.tweet_score = single_tweet.tweet_score * 0.75

    return zoo , restaurant , museum

def output(final_tweets):
    
    for tweet in final_tweets:
        print("====================================================================================")
        print('\033[1m' + 'Tweet Text')
        print('\033[0m' +tweet.tweet)
        print("--------------------------------------------------------------------------------")
        print('\033[1m' + 'Tweet Score :\t \033[0m' + str(tweet.sentiment))
        print("--------------------------------------------------------------------------------")
        print('\033[1m' + 'Travel Realted :\t \033[0m' + str(tweet.screen_name))
        print("--------------------------------------------------------------------------------")
        print('\033[1m' + 'Category :\t \033[0m' + str(tweet.travel_category))
        print("====================================================================================")
    
@app.route('/')
def initial():
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO `users`(`username`, `password`) VALUES ('baapp','123')")
    # mysql.connection.commit()
    return render_template('index.html')
     

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('index.html')
    
@app.route('/login' , methods = ['GET','POST'])
def login():
    username = request.form['your_name']
    password = request.form['your_pass']
    cur = mysql.connection.cursor()
    cur.execute("Select * from users where username = '"+username+"' and password = '"+password+"'")
    result = cur.fetchone()
    # return str(result[3])
    if result != None:
        final_tweets = get_all_tweets(result[3])
        print("[=[=[=[=[=[=[=[=[=[=[==[[[=[=[=[=[=[=[=[[==[=[==[==[]]]]]]]]]]]]]]]]]]]]]]]]]]")
        zoo , restaurant , museum = classify_tweets(final_tweets)
        zoo , restaurant , museum = sentiment_score(zoo , restaurant , museum)
        output(zoo)
        output(restaurant)
        output(museum)
        max_zoo , max_restaurant , max_museum = max_tweet_score(zoo , restaurant , museum)
        zoo_score = category_score(zoo , max_zoo)
        restaurant_score = category_score(restaurant , max_restaurant)
        museum_score = category_score(museum , max_museum)

        if (zoo_score > restaurant_score) and (zoo_score > museum_score):
            largest = "zoo"
        elif (museum_score > zoo_score) and (restaurant_score < museum_score):
            largest = "museum"
        else:
            largest = "restaurant"
        session['poi'] = largest

        retweet(zoo , restaurant , museum , largest)
        return render_template('landing.html' , username = username.upper())
            # (redirect(url_for('signup')))
    else:
        flash("Invalid Credential")
        return redirect(url_for('signin'))

@app.route('/recommendation' , methods = ['GET' , 'POST'])
def recommendation():
    poi = session.get('poi')
    destination = request.form['destination']
    normal_result, organic_result = get_recommendation(poi , destination)
    return render_template("landing.html" , normal_result = normal_result , organic_result = organic_result, destination = destination)
    

@app.route('/register' , methods = ['GET','POST'])
def register():
    print(request)
    username = request.form['username']
    password = request.form['pass']
    tweeter_id = request.form['tweeter_id']
    conf_password  = request.form['re_pass']
    if password != conf_password:
        flash("Password and Confirm Password must be same")
        return redirect(url_for('signup'))

    if username == "":
        flash("Please enter username")
        return redirect(url_for('signup'))
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `users`(`username`, `password` , `tweeter_id`) VALUES ('"+username+"' , '"+password+"' , '"+tweeter_id+"')")
    mysql.connection.commit()

    get_followers_following(tweeter_id)    
    flash("Registration successfull")
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug = True)



    # cur = mysql.connection.cursor()
    # # cur.execute('''CREATE TABLE users (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20) , password VARCHAR(20))''')
    # # cur.execute('''DROP TABLE users''')
    # cur.execute('''INSERT INTO `users`(`username`, `password`) VALUES ("baap" , "123")''')
    # mysql.connection.commit()
    # baap = cur.execute("Select * from users")
    # result = cur.fetchall()
    # return str(result)