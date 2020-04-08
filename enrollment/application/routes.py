from application import app, db
from flask import render_template, request, json, Response
from application.models import User, Course, Enrollment

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login")
def login():
    return render_template("login.html", login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route("/register")
def register():
    return render_template("register.html", register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID') #Using get:if courseID field is not present it will return None
    title = request.form['title'] #Using array method:if title field is not present it will crash
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, data={"courseId":id,"courseTitle":title,"courseTerm":term})

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jsonData = courseData
    else:
        jsonData = courseData[int(idx)]
    
    return Response(json.dumps(jsonData), mimetype="application/json")

class User(db.Document):
    user_id = db.IntField( unique=True )
    first_name = db.StringField( max_length=50 )
    last_name = db.StringField( max_length=50 )
    email = db.StringField( max_length=30 )
    password = db.StringField( max_length=30 )

@app.route("/user")
def user():
    # User(user_id=1, first_name='Rohit', last_name='Jain', email='rrjain@uta.com', password='abc1234').save()
    # User(user_id=2, first_name='Priyal', last_name='Jain', email='prjain@uta.com', password='abc1234').save()
    # User(user_id=3, first_name='Bhoomi', last_name='Waghale', email='bwaghale@uta.com', password='abc1234').save()
    users = User.objects.all()
    return render_template('user.html', users=users)
