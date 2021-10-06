import os
from datetime import datetime
from application import app,auth,db,storage,UPLOAD_FOLDER
from flask import Flask,request,render_template,url_for,session,redirect,flash
from werkzeug.utils import secure_filename

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
    leader_speaks = None
    interview = None
    try:
        event_notice = db.child("events").get()
        blog_preview = db.child("blogs").order_by_key().limit_to_last(10).get()
    except:
        print("Error fetching events")

    if(request.form.get('feedback')):
        if request.method == "POST":
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

            feeback_data = {
                'email':email,
                'subject':subject,
                'message':message,
                'last_updated':str(datetime.now())
            }
            try:
                db.child("feedback").push(feeback_data)
            except:
                print("unable to push feedback")

    try:
        for event in event_notice.val():
            if(event):
                break
    except:
        event_notice = []

    try:
        for event in blog_preview.val():
            if(event):
                break
    except:
        blog_preview = []

    # Leadership Speaks
    try:
        leader_speaks = db.child("leader_speaks").get()
    except:
        print("Error fetching details")

    try:
        for ev in leader_speaks:
            if ev:
                break
    except:
        leader_speaks = []

    # Poster
    try:
        poster = db.child("poster").get()
    except:
        print("Error fetching details")
    
    try:
        for v in poster:
            if v:
                break
    except:
        poster = []

    try:
        interview = db.child("interview").get()
    except:
        print("Error fetching interviews")
    
    try:
        for v in interview:
            if v:
                break
    except:
        interview = []
    
    try:
        oppt = db.child("oppt").get()
        # print(oppt)
    except:
        oppt = []
    
    return render_template("index.html",data=data,event_notice=event_notice,blog_preview=blog_preview,n=n,leader_speaks=leader_speaks,poster=poster,interview=interview,oppt=oppt)

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

    if(request.form.get('submit_journal')):
        if request.method == "POST":
            journal = request.files['journal']
            fname = secure_filename(journal.filename)
            journal.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
            upload_path = os.path.join(upload_path,'uploads')
            upload_path = os.path.join(upload_path,fname)
            try:
                storage.child("pdf/"+ fname).put(upload_path)
            except:
                print("File Upload error")

            pdf_url = storage.child("pdf/"+ fname).get_url(session['usr'])
            author_name = request.form.get('author_name')
            title = request.form.get('title')
            description = request.form.get('description')
            tags = request.form.get('tags')

            add_pdf = {
                'author':author_name,
                'title':title,
                'description':description,
                'tags':tags,
                'pdf_url':pdf_url
            }
            try:
                db.child("Journal").push(add_pdf)
                print('upload Successfull')
            except:
                print("Unable to upload")


    if(request.form.get('add_event')):
        event_name = request.form.get('event')
        event_date = request.form.get('event_date')
        event_time = request.form.get('timing')
        event_reg_start = request.form.get('reg_start')
        event_reg_end = request.form.get('reg_end')
        event_url = request.form.get('event_url')

        event_data = {
            'event_name':event_name,
            'event_date':event_date,
            'event_time':event_time,
            'event_reg_start':event_reg_start,
            'event_reg_end':event_reg_end,
            'event_url':event_url,
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

        blogs = request.files['associated_image']
        fname = secure_filename(blogs.filename)
        blogs.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)
        try:
            storage.child("blog/"+ fname).put(upload_path)
        except:
            print("File Upload error")

        blog_url = storage.child("blog/"+ fname).get_url(session['usr'])
        
        upload_blog = {
            'blog_data':blog_data,
            'blog_author':blog_author,
            'title': title,
            'description': description,
            'last_updated': str(datetime.now()),
            'blog_url' : blog_url,
            'count':0
        }
        try:
            db.child("blogs").push(upload_blog)
        except:
            print('Cannot Upload blog')
    
    # Upload oppurtunities
    if(request.form.get('submit_opp')):
        blog_data = request.form.get('oppt_editordata')
        blog_author = request.form.get('oppt_name')
        title = request.form.get('oppt_title')
        description = request.form.get('oppt_desc')

        blogs = request.files['oppt_image']
        fname = secure_filename(blogs.filename)
        blogs.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)
        try:
            storage.child("oppt/"+ fname).put(upload_path)
        except:
            print("File Upload error")

        oppt_url = storage.child("oppt/"+ fname).get_url(session['usr'])
        
        upload_blog = {
            'oppt_data':blog_data,
            'oppt_author':blog_author,
            'title': title,
            'description': description,
            'last_updated': str(datetime.now()),
            'blog_url' : oppt_url,
            'count':0
        }
        try:
            db.child("oppt").push(upload_blog)
        except:
            print('Cannot Upload blog')
    # End Upload oppurtunities
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

    feedbacks = None
    if(request.args.get('action') == 'view_feedback'):
        try:
            feedbacks = db.child("feedback").order_by_key().get()
        except:
            print("Unable to fetch feedback")

        # Delete message
        try:
            if(request.args.get('delete_key')):
                delete_key = request.args.get('delete_key')
                db.child("feedback").child(delete_key).remove()
                return redirect(url_for('cms',action='view_feedback'))
        except:
            print("Some error occured")
    #Add memeber to the team
    if request.form.get('submit_member'):
        member_name = request.form.get('member_name')
        member_position = request.form.get('member_position')
        member_qualifications = request.form.get('member_qualifications')
        member_team = request.form.get('member_team')
        member_avatar = request.files['member_avatar']
        fname = secure_filename(member_avatar.filename)
        member_avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)

        try:
            storage.child("member_image/"+ fname).put(upload_path)
        except:
            print("File Upload error")
        
        member_url = storage.child("member_image/"+ fname).get_url(session['usr'])
        add_member = {
            'member_name':member_name,
            'member_position':member_position,
            'member_qualifications':member_qualifications,
            'member_team':member_team,
            'member_avatar':member_url
        }
        try:
            if(add_member['member_team'] == 'Editorial' and request.form.get('member_post')):
                m_post = request.form.get('member_post')
                db.child("members").child(member_team).child(m_post).push(add_member)  
            db.child("members").child(member_team).push(add_member)
        except:
            print("Unable to upload memeber try agin later")

    members_to_send = None
    li = []
    if send_action == 'edit_or_delete':
        try:
            members_to_send = db.child("members").get()
        except:
            print("Member not passed, error here")
    
    if send_action == 'delete_member':
        id_member = request.args.get('member_id')
        team = request.args.get('team')
        db.child('members').child(team).child(id_member).remove()
        return redirect(url_for('cms',action='edit_or_delete'))

    if send_action == 'delete_editor':
        id_member = request.args.get('member_id')
        team = request.args.get('team')
        db.child('members').child("Editorial").child(team).child(id_member).remove()
    
    # if send_action == 'edit_member':
    #     id_member = request.args.get('member_id')
    #     team = request.args.get('team')
    #     data = db.child('members').child(team).child(id_member).get()
    #     member_data = {}
    #     for d in data.each():
    #         member_data[d.key()] = d.val()
    #     return render_template('./cms/manage_user.html')

    if request.form.get('upload_leader'):
        leader_avatar = request.files['leader_speaks']
        fname = secure_filename(leader_avatar.filename)
        leader_avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)
            
        try:
            storage.child("leader_speaks/"+ fname).put(upload_path)
        except:
            print("File Upload error")
            
        leader_url = storage.child("leader_speaks/"+ fname).get_url(session['usr'])
        data_leader = {"image_url":leader_url}

        # d1 = request.form.get("hello")
        # print(d1)
        db.child("leader_speaks").push(data_leader)
        



    # poster
    if(request.form.get('upload_poster')):
        poster_avatar = request.files['poster']
        fname = secure_filename(poster_avatar.filename)
        poster_avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)
            
        try:
            storage.child("posters/"+ fname).put(upload_path)
        except:
            print("File Upload error")

        poster_url = storage.child("posters/"+ fname).get_url(session['usr'])
        data_poster = {"image_url":poster_url}

        # d1 = request.form.get("hello")
        # print(d1)
        db.child("poster").push(data_poster)

    if(request.form.get('submit_interview')):
        interview_name = request.form.get('interview_name')
        subject = request.form.get('subject')
        summary = request.form.get('summary')
        detail = request.form.get('editordata')
        image = request.files['image']
        fname = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
        upload_path = os.path.join(upload_path,'uploads')
        upload_path = os.path.join(upload_path,fname)

        try:
            storage.child("interview/"+ fname).put(upload_path)
        except:
            print("File Upload error")
        
        image_url = storage.child("interview/"+ fname).get_url(session['usr'])

        data = {
            "interview_name":interview_name,
            "subject":subject,
            "summary":summary,
            "detail":detail,
            "image_url":image_url
        }

        db.child("interview").push(data)
        

    editors_to_send = None
    try:
        editors_to_send = db.child("members").child("Editorial").get()
    except:
        editors_to_send = []
    
    return render_template("cms.html",send_action=send_action,events=events,feedbacks=feedbacks,members_to_send=members_to_send,editors_to_send=editors_to_send)

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
    members = None
    try:
        members = db.child("members").child("Honary Board").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in members.each():
            if member:
                break
    except:
        members = []

    return render_template('honary_board.html',members=members)

@app.route('/editorial_board')
def editorial_board():
    members = None
    senior_editor = None
    student_editor = None
    editor_in_chief = None

    try:
        senior_editor = db.child("members").child("Editorial").child("Senior Editor").get()
    except:
        print("Error occured fetching Honary Board")

    try:
        student_editor = db.child("members").child("Editorial").child("Student Editor").get()
    except:
        print("Error occured fetching Honary Board")

    try:
        editor_in_chief = db.child("members").child("Editorial").child("Editor in Chief").get()
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in senior_editor.each():
            if member:
                break
    except:
        senior_editor = []

    try:
        for member in senior_editor.each():
            if member:
                break
    except:
        senior_editor = []

    try:
        for member in student_editor.each():
            if member:
                break
    except:
        student_editor = []

    try:
        for member in editor_in_chief.each():
            if member:
                break
    except:
        editor_in_chief = []
    
    return render_template('editorial_board.html',senior_editor=senior_editor,student_editor=student_editor,editor_in_chief=editor_in_chief)

@app.route('/core_members')
def core_members():
    members = None
    try:
        members = db.child("members").child("Core Members").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in members.each():
            if member:
                break
    except:
        members = []
    return render_template('core_members.html',members=members)

@app.route('/coordinators')
def coordinators():
    members = None
    try:
        members = db.child("members").child("Coordinators").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in members.each():
            if member:
                break
    except:
        members = []

    return render_template('coordinators.html',members=members)

@app.route('/convenors')
def convenors():
    members = None
    try:
        members = db.child("members").child("Convenors").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in members.each():
            if member:
                break
    except:
        members = []
    return render_template('convenors.html',members=members)

@app.route('/advisory_board')
def advisory_board():
    members = None
    try:
        members = db.child("members").child("Advisiory Board").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")
    
    try:
        for member in members.each():
            if member:
                break
    except:
        members = []
    return render_template('advisory_board.html',members=members)

@app.route('/techinical_board')
def techinical_board():
    members = None
    try:
        members = db.child("members").child("Techinical Board").get()
        # for member in members.each():
        #     member_avatar = member.val()['member_avatar']
        #     member_name = member.val()['member_name']
        #     member_position = member.val()['member_position']
        #     member_qualifications = member.val()['member_qualifications']
        #     member_team = member.val()['member_team']
    except:
        print("Error occured fetching Honary Board")

    try:
        for member in members.each():
            if member:
                break
    except:
        members = []
    return render_template('techinical_board.html',members=members)

@app.route('/view_journals')
def view_journals():
    journals = None
    try:
        journals = db.child("Journal").get()
    except:
        print("Error fetching details")
    return render_template('view_journals.html',journals=journals)

@app.route('/blogs')
def blogs():
    blogs = None
    try:
        blogs = db.child("blogs").get()
    except:
        print("Could not fetch blog")

    try:
        for blog in blogs.each():
            if blog:
                break
    except:
        blogs = []
    
    return render_template('blogs.html',blogs=blogs)

@app.route('/blog_details')
def blog_details():
    key = request.args.get('key')
    data = None
    count = 0
    try:
        data = db.child("blogs").child(key).get()
    except:
        print("Could not fetch")
    
    try:
        for d in data.each():
            if d:
                break
    except:
        data = []
    # d1 = dict(data)

    # View count
    count = data.val()['count']
    db.child("blogs").child(key).update({"count":count + 1})
    return render_template('blog_detail.html',data = data)

# Oppurtunities details
@app.route('/oppt_details')
def oppt_details():
    key = request.args.get('key')
    data = None
    count = 0
    try:
        data = db.child("oppt").child(key).get()
    except:
        print("Could not fetch")
    
    try:
        for d in data.each():
            if d:
                break
    except:
        data = []
    # d1 = dict(data)

    # View count
    count = data.val()['count']
    db.child("blogs").child(key).update({"count":count + 1})
    return render_template('oppt_detail.html',data = data)

@app.route('/interview_details')
def interview_details():
    key = request.args.get('key')
    print(key)
    data = None
    try:
        data = db.child("interview").child(key).get()
    except:
        print("COuld not fetch data")
    
    try:
        for d in data.each():
            if d:
                break
    except:
        data = []
    return render_template('interview_details.html',data=data)