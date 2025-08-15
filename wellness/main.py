from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, Response
from . import db
from .models import WellnessProgram, WellnessParticipation, Challenge, ChallengeParticipation, User
from datetime import datetime, timezone
import pytz
import pandas as pd
from io import BytesIO
from flask_login import login_required, current_user
from collections import Counter
from matplotlib import pyplot as plt
import io


main = Blueprint('main', __name__)


"""
=================================================================================
                     HELPER FUNCTIONS
=================================================================================
"""

def get_ist_time():
        ist = pytz.timezone("Asia/Kolkata")
        return datetime.now(ist)


"""
=================================================================================
            HELPER FUNCTIONS ENDED

            ADMIN - CRUD OPERATIONS ON PROGRAMS 
=================================================================================
"""

@main.route("/adminpview")
@login_required
def display_admin_wp():
    wplist = WellnessProgram.query.all()
    return render_template("adminprogramlist.html", programs=wplist)

@main.route('/addwp')
@login_required
def create_wellness_program():
    return render_template("addprogram.html")

@main.route("/addwp", methods=['POST'])
@login_required
def create_wp_post():
    pname = request.form["pname"]
    pstart = request.form["pstart"]
    pend = request.form["pend"]
    pvenue = request.form["pvenue"]
    porganizer = request.form['porganizer']
    pcategory = request.form['pcategory']
    pdesc = request.form['pdesc']
    pcontact = request.form['pcontact']

    print(pname, pstart, pend)

    pstart = datetime.strptime(pstart, '%Y-%m-%dT%H:%M')
    pstart = pstart.replace(tzinfo=timezone.utc)

    pend = datetime.strptime(pend, '%Y-%m-%dT%H:%M')
    pend = pend.replace(tzinfo=timezone.utc)

    wp = WellnessProgram(pname=pname, pstart=pstart, pend=pend,
                         pvenue=pvenue, porganizer=porganizer, 
                         pdesc=pdesc, pcontact=pcontact, pcategory=pcategory
                         )
    db.session.add(wp)
    db.session.commit()

    flash("new wellness program is added")

    return redirect(url_for("main.display_admin_wp"))

@main.route("/updatewp/<int:wpid>", methods=['GET', 'POST'])
@login_required
def update_wp(wpid):
    wp = WellnessProgram.query.get_or_404(wpid)
    print(wp.pid, wp.pname, wp.pdesc)

    if request.method == "POST":
        wp.pname = request.form["pname"]
        wp.pvenue = request.form["pvenue"]
        wp.porganizer = request.form['porganizer']
        wp.pdesc = request.form['pdesc']
        wp.pcontact = request.form['pcontact']
        wp.pcategory = request.form['pcategory']
        pstart = request.form['pstart']
        pend =request.form['pend']

        pstart = datetime.strptime(pstart, '%Y-%m-%dT%H:%M')
        pstart = pstart.replace(tzinfo=timezone.utc)

        pend = datetime.strptime(pend, '%Y-%m-%dT%H:%M')
        pend = pend.replace(tzinfo=timezone.utc)

        wp.pstart = pstart
        wp.pend = pend

        db.session.commit()
        flash("Program details updated successfully")

        return redirect(url_for("main.display_admin_wp"))

    print("hello")
    return render_template("updateprogram.html", program=wp)

@main.route("/deletewp/<int:wpid>", methods=['GET', 'POST'])
@login_required
def delete_wp(wpid):
    wp = WellnessProgram.query.get_or_404(wpid)
    db.session.delete(wp)
    db.session.commit()
    return redirect(url_for("main.display_admin_wp"))

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


"""
=================================================================================
            ADMIN - PROGRAMS CRUD ENDS HERE
            
            ADMIN - CHALLENGES CRU 
=================================================================================
"""

@main.route("/adminchview")
@login_required
def display_admin_ch():
    chlist = Challenge.query.all()
    return render_template("adminchallengelist.html", challenges=chlist)

@main.route('/addch')
@login_required
def create_challenge():
    return render_template("addchallenge.html")

@main.route("/addch", methods=['POST'])
@login_required
def create_ch_post():
    chname = request.form["chname"]
    chstart = request.form["chstart"]
    chend = request.form["chend"]
    chvenue = request.form["chvenue"]
    chorganizer = request.form['chorganizer']
    chcategory = request.form['chcategory']
    chdesc = request.form['chdesc']
    chcontact = request.form['chcontact']
    chpoints = int(request.form['chpoints'])
    

    print(chname, chstart, chend)

    chstart = datetime.strptime(chstart, '%Y-%m-%dT%H:%M')
    chstart = chstart.replace(tzinfo=timezone.utc)

    chend = datetime.strptime(chend, '%Y-%m-%dT%H:%M')
    chend = chend.replace(tzinfo=timezone.utc)

    challenge = Challenge(chname=chname, chstart=chstart, chend=chend,
                         chvenue=chvenue, chorganizer=chorganizer, chpoints=chpoints,
                         chdesc=chdesc, chcontact=chcontact, chcategory=chcategory
                         )
    db.session.add(challenge)
    db.session.commit()

    flash("new challenge is added")

    return redirect(url_for("main.display_admin_ch"))

@main.route("/updatech/<int:chid>", methods=['GET', 'POST'])
@login_required
def update_ch(chid):
    ch = Challenge.query.get_or_404(chid)
    print(ch.chid, ch.chname, ch.chdesc)

    if request.method == "POST":
        ch.chname = request.form["chname"]
        ch.chvenue = request.form["chvenue"]
        ch.chorganizer = request.form['chorganizer']
        ch.chdesc = request.form['chdesc']
        ch.chcontact = request.form['chcontact']
        ch.chpoints = int(request.form['chpoints'])
        ch.chcategory = request.form['chcategory']
        chstart = request.form['chstart']
        chend =request.form['chend']

        chstart = datetime.strptime(chstart, '%Y-%m-%dT%H:%M')
        chstart = chstart.replace(tzinfo=timezone.utc)

        chend = datetime.strptime(chend, '%Y-%m-%dT%H:%M')
        chend = chend.replace(tzinfo=timezone.utc)

        ch.chstart = chstart
        ch.chend = chend

        db.session.commit()
        flash("Challenge details updated successfully")

        return redirect(url_for("main.display_admin_ch"))

    print("hello")
    return render_template("updatechallenge.html", challenge=ch)

@main.route("/deletech/<int:chid>", methods=['GET', 'POST'])
@login_required
def delete_ch(chid):
    challenge = Challenge.query.get_or_404(chid)
    db.session.delete(challenge)
    db.session.commit()
    return redirect(url_for("main.display_admin_ch"))




"""
=================================================================================
            ADMIN RELATED PROGRAMS FUNCTIONALITY ENDS HERE
            USER PROGRAMS RELATED FUNCTIONALITY STARTS FROM HERE 
=================================================================================
"""

@main.route("/userpview")
@login_required
def display_user_wp():
    wplist = WellnessProgram.query.all()
    return render_template("userprogramlist.html", programs=wplist)

@main.route("/registerwp/<int:wpid>", methods=['GET', 'POST'])
@login_required
def register_wp(wpid):
    userid = current_user.id
    status = 'REGISTERED'
    pregtime = get_ist_time()
    wparticipation = WellnessParticipation(pid=wpid, uid=userid, pregtime=pregtime, status=status)
    db.session.add(wparticipation)
    db.session.commit()
    flash("Succesfully registered for the wellness program")
    registration = WellnessParticipation.query.filter_by(uid=userid, pid=wpid).first()
    regid = registration.ppid
    return redirect(url_for("main.registration_success", regid = regid))

@main.route('/registration-success/<int:regid>')
@login_required
def registration_success(regid):
    preg = WellnessParticipation.query.get_or_404(regid)
    print(preg.ppid)
    pname = WellnessProgram.query.get_or_404(preg.pid).pname
    return render_template('pregsuccess.html', preg=preg, pname=pname)


@main.route("/profile/", methods=['GET', 'POST'])
@login_required
def getmyprograms():
    userid = current_user.id
    user = User.query.get_or_404(userid)
    pr_par = WellnessParticipation.query.filter_by(uid=userid).all()
    ch_par = ChallengeParticipation.query.filter_by(uid=userid).all()
    print(user.id, user.name)
    print(len(pr_par), len(ch_par))
    return render_template("profile.html", programs=pr_par, challenges=ch_par, user=user)

@main.route("/userchview")
@login_required
def display_user_ch():
    chlist = Challenge.query.all()
    return render_template("userchallengelist.html", challenges=chlist)

@main.route("/registerch/<int:chid>", methods=['GET', 'POST'])
@login_required
def register_ch(chid):
    userid = current_user.id
    status = 'REGISTERED'
    chregtime = get_ist_time()
    chparticipation = ChallengeParticipation(chid=chid, uid=userid, chregtime=chregtime, status=status)
    db.session.add(chparticipation)
    db.session.commit()
    flash("Succesfully registered for the challenge")
    registration = ChallengeParticipation.query.filter_by(uid=userid, chid=chid).first()
    regid = registration.cpid
    return redirect(url_for("main.ch_registration_success", regid = regid))

@main.route("/chregsucesss/<int:regid>")
@login_required
def ch_registration_success(regid):
    chreg = ChallengeParticipation.query.get_or_404(regid)
    print(chreg.cpid)
    chname = Challenge.query.get_or_404(chreg.chid).chname
    return render_template('chregsuccess.html', chreg=chreg, chname=chname)



"""
=================================================================================
            USER PROGRAMS FUNCTIONALITY ENDS HERE
            ADMIN PROGRAM PARTICIPATION FUNCTIONALITY STARTS FROM HERE 
=================================================================================
"""

@main.route("/wpparticipants<int:wpid>", methods=['POST', 'GET'])
@login_required
def get_program_participations(wpid):
    wp = WellnessProgram.query.get_or_404(wpid)
    if wp is None:
        flash("Invalid wellness program id")
        return redirect(url_for("auth.adminHome"))
    programname = wp.pname
    participations = WellnessParticipation.query.filter_by(pid=wpid)
    pid = wp.pid
    return render_template("programparticipants.html", participations=participations, pname=programname, pid=pid)

@main.route("/chparticipants<int:chid>", methods=['POST', 'GET'])
@login_required
def get_challenge_participations(chid):
    challenge = Challenge.query.get_or_404(chid)
    if challenge is None:
        flash("Invalid Challenge id")
        return redirect(url_for("auth.adminHome"))
    chname = challenge.chname
    chid = challenge.chid
    challenges = ChallengeParticipation.query.filter_by(chid=chid)
    return render_template("challengeparticipants.html", challenges=challenges, chname=chname, chid=chid)

@main.route("/updatecp/<int:cpid>", methods=['GET', 'POST'])
@login_required
def update_chpar(cpid):
    cp = ChallengeParticipation.query.get_or_404(cpid)
    print(cp.cpid, cp.chid, cp.uid, cp.chregtime)

    if request.method == "POST":
        cp.chid = request.form["chid"]
        cp.uid = request.form["uid"]
        #chregtime = request.form['chregtime']
        cp.status = request.form['status']

        # chregtime = datetime.strptime(chregtime, '%Y-%m-%dT%H:%M')
        # chregtime = chregtime.replace(tzinfo=timezone.utc)

        # cp.chregtime = chregtime

        db.session.commit()
        flash("Challenge participation details updated successfully")

        if cp.status == "COMPLETED":
            user = User.query.get_or_404(cp.uid)
            challenge = Challenge.query.get_or_404(cp.chid)
            print(type(user.points))
            if user.points is None:
                user.points = 0 + challenge.chpoints
            else:
                user.points = user.points + challenge.chpoints
            db.session.commit()

        return redirect(url_for("main.get_challenge_participations", chid=cp.chid))

    print("hello")
    return render_template("updatechparticipation.html", cp=cp)

@main.route("/progdownload/<int:wpid>", methods=['POST', 'GET'])
@login_required
def download_plist(wpid):
    program = WellnessProgram.query.get_or_404(wpid)
    if program is None:
        flash("Invalid program ID")
        return redirect(url_for("main.display_admin_wp"))
    pname = program.pname
    participants = WellnessParticipation.query.filter_by(pid=wpid)
    participant_data = [
        {
            "Participation ID": participant.ppid,
            "Participant ID": participant.uid,  
            "Status": participant.status, 
            "Reg time": participant.pregtime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-6],
            "Signature": " "
        }
        for participant in participants
    ]

    for participant in participant_data:
        print(participant["Reg time"])
        
    df = pd.DataFrame(participant_data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        workbook = writer.book
        worksheet = workbook.create_sheet(title="Participants", index=0)
        worksheet.merge_cells('A1:h1')
        worksheet['A1'] = f"Program: {pname}" 

        df.to_excel(writer, index=False, startrow=2, sheet_name='Participants')
        column_widths = {
            "A": 20, "B": 20, "C": 20, "D": 50 , "E": 40
        }
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name=f'program_{wpid}_participants.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@main.route("/chdownload/<int:chid>", methods=['POST', 'GET'])
@login_required
def download_chlist(chid):
    challenge = Challenge.query.get_or_404(chid)
    if challenge is None:
        flash("Invalid challenge ID")
        return redirect(url_for("main.display_admin_wp"))
    chname = challenge.chname
    participants = ChallengeParticipation.query.filter_by(chid=chid)
    participant_data = [
        {
            "Participation ID": participant.cpid,
            "Participant ID": participant.uid,  
            "Status": participant.status, 
            "Reg time": participant.chregtime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-6],
            "Points":" ",
            "Signature": " "
        }
        for participant in participants
    ]

    for participant in participant_data:
        print(participant["Reg time"])
        
    df = pd.DataFrame(participant_data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        workbook = writer.book
        worksheet = workbook.create_sheet(title="Participants", index=0)
        worksheet.merge_cells('A1:h1')
        worksheet['A1'] = f"Challenge: {chname}" 

        df.to_excel(writer, index=False, startrow=2, sheet_name='Participants')
        column_widths = {
            "A": 20, "B": 20, "C": 20, "D": 50 , "E": 40
        }
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name=f'challenge_{chid}_participants.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@main.route("/ch_category_participation")
@login_required
def ch_category_participation():

    #plot1
    chpar = ChallengeParticipation.query.all()
    
    # Extract the categories from the Challenge model based on participations
    categories = ['SPORTS', 'ART', 'ACADEMICS', 'ENTERTAINMENT']
    counts = [0,0,0,0]

    for ch in chpar:
        challenge = Challenge.query.get_or_404(ch.chid)
        category = challenge.chcategory
        for i in range(0, 4):
            if categories[i] == category.upper():
                counts[i] += 1
                break

    # Create a bar plot
    fig, ax = plt.subplots()
    ax.bar(categories, counts, color='skyblue')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Number of Participations')
    ax.set_title('Challenge Participation by Category')
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # Return the image as a response
    return Response(img, mimetype='image/png')

@main.route("/pr_category_participation")
@login_required
def pr_category_participation():

    print("hellooooo")

    #plot1
    pr_par = WellnessParticipation.query.all()
    
    # Extract the categories from the Program model based on participations
    categories = ['SPORTS', 'ART', 'ACADEMICS', 'ENTERTAINMENT']
    counts = [0,0,0,0]

    for pr in pr_par:
        print("hellooooo")
        program = WellnessProgram.query.get_or_404(pr.pid)
        category = program.pcategory
        print(category)
        for i in range(0, 4):
            if categories[i] == category.upper():
                counts[i] += 1
                break

    # Create a bar plot
    fig, ax = plt.subplots()
    ax.bar(categories, counts, color='skyblue')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Number of Participations')
    ax.set_title('Challenge Participation by Category')
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # Return the image as a response
    return Response(img, mimetype='image/png')

@main.route('/ch_gender_participation')
@login_required
def ch_gender_participation():
   
    chpar = ChallengeParticipation.query.all()
    genders = ['MALE', 'FEMALE', 'OTHER']
    counts = [0,0,0]

    for ch in chpar:
        user = User.query.get_or_404(ch.uid)
        gender = user.gender
        print(user.gender)
        for i in range(0, 3):
            if genders[i] == gender.upper():
                counts[i] += 1
                break

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(counts, labels=genders, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # Save the pie chart to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    
    # Return the pie chart as a response with the appropriate mimetype
    return Response(img, mimetype='image/png')


@main.route('/pr_gender_participation')
@login_required
def pr_gender_participation():
   
    pr_par = WellnessParticipation.query.all()
    genders = ['MALE', 'FEMALE', 'OTHER']
    counts = [0,0,0]

    for ch in pr_par:
        user = User.query.get_or_404(ch.uid)
        gender = user.gender
        for i in range(0, 3):
            if genders[i] == gender.upper():
                counts[i] += 1
                break

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(counts, labels=genders, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # Save the pie chart to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    
    # Return the pie chart as a response with the appropriate mimetype
    return Response(img, mimetype='image/png')






    




