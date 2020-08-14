import os
from datetime import datetime
from application import app,auth,db
from flask import Flask,request,render_template,url_for,session,redirect

base_dir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(base_dir,'static/data.txt')

with open(data_file, 'r',encoding="utf8") as file:
    data = file.read().replace('\n', '')


@app.route("/",methods=["GET","POST"])
def index():
    n = 5
    if(request.args.get('more')):
        n = n + int(request.args.get('more'))
    event_notice = None
    blog_preview = None
    try:
        event_notice = db.child("events").get()
        blog_preview = db.child("blogs").order_by_key().limit_to_last(n).get()
    except:
        print("Error fetching events")
        
    return render_template("index.html",data=data,event_notice=event_notice,blog_preview=blog_preview,n=n)

@app.route("/for_students")
def for_students():
    return render_template("for_student.html")

@app.route("/about_us")
def about_us():
    return render_template("aboutus.html")

@app.route('/cms',methods=['GET','POST'])
def cms():
    if(session['usr'] == None):
        return redirect('/')
    send_action = None
    if(request.args.get('action')):
        send_action = request.args.get('action')

    if(request.form.get('add_event')):
        event_name = request.form.get('event')
        event_date = request.form.get('event_date')
        event_time = request.form.get('timing')
        event_reg_start = request.form.get('reg_start')
        event_reg_end = request.form.get('reg_end')

        event_data = {
            'event_name':event_name,
            'event_date':event_date,
            'event_time':event_time,
            'event_reg_start':event_reg_start,
            'event_reg_end':event_reg_end,
            'last_updated':str(datetime.now())
        }
        try:
            db.child("events").push(event_data)
        except:
            print("Failed to Insert Data")
    
    if(request.form.get('submit_blog')):
        blog_data = request.form.get('editordata')
        blog_author = request.form.get('author_name')
        title = request.form.get('title')
        description = request.form.get('description')
        upload_blog = {
            'blog_data':blog_data,
            'blog_author':blog_author,
            'title': title,
            'description': description,
            'last_updated': str(datetime.now())
        }
        try:
            db.child("blogs").push(upload_blog)
        except:
            print('Cannot Upload blog')
    # Deleting the event as per user requirements
    if(request.args.get('remove')):
        key = request.args.get('key')
        db.child("events").child(key).remove()

    # Fetching the vents for action
    events = None
    try:
        events = db.child("events").get()
    except:
        print("Error fetching events")

    
    return render_template("cms.html",send_action=send_action,events=events)

@app.route('/cms_login',methods=['GET','POST'])
def cms_login():
    session['usr'] = None
    if(session['usr']):
        return redirect('cms')
    else:
        if(request.form.get('submit')):
            email = request.form.get('email')
            password = request.form.get('password')
            try:
                user = auth.sign_in_with_email_and_password(email,password)
                user = auth.refresh(user['refreshToken'])
                user_id = user['idToken']
                session['usr'] = user_id
                return redirect(url_for('cms'))
            except:
                print('Something happend')
    return render_template('cms_login.html')

@app.route('/view_blogs')
def view_blogs():
    blogs = None
    try:
        blogs = db.child("blogs").get()
    except:
        print("Could not fetch blog")
    
    return render_template('view_blogs.html',blogs=blogs)

@app.route('/view_details')
def view_details():
    key = request.args.get('key')
    blog = db.child("blogs").order_by_key().equal_to(key).limit_to_first(1).get()
    return render_template('view_details.html',blog=blog)

@app.route('/logout')
def logout():
    session['usr'] = None
    return redirect('/')

@app.route('/honary_board')
def honary_board():
    return render_template('honary_board.html')

@app.route('/editorial_board')
def editorial_board():
    return render_template('editorial_board.html')

@app.route('/core_members')
def core_members():
    return render_template('core_members.html')

@app.route('/coordinators')
def coordinators():
    return render_template('coordinators.html')

@app.route('/convenors')
def convenors():
    return render_template('convenors.html')

@app.route('/advisory_board')
def advisory_board():
    return render_template('advisory_board.html')
