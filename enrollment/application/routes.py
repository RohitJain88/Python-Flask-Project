from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = form.password.data #3rd way: to get data from the form submitted in the browser

        #Validating form submitted email and password with the database
        user = User.objects(email=email).first()
        if user and password == user.password:
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry! Something went wrong", "danger")

    return render_template("login.html", form=form, title="Login", login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("-courseID")    
    return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, password=password, last_name=last_name)
        # user.set_password(password)
        user.save()

        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template("register.html", form=form, title="New User Registration", register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    courseID = request.form.get('courseID') #Using get:if courseID field is not present it will return None
    #courseTitle = request.form['title'] #Using array method:if title field is not present it will crash
    courseTitle = request.form.get('title')
    user_id = 1

    #Helps to determine if we are enrolling the course
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID)
            flash(f"You are enrolled in {courseTitle}", "success")

    classes = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': -1
                }
            }
        ]))
    
    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)
    #data={"courseId":id,"courseTitle":title,"courseTerm":term})

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
