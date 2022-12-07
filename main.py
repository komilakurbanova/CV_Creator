from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, send_file
from flask_login import login_required, current_user
import datetime
import os
import pdfkit
import base64
from app import db
from models import CV
from flask import flash


main = Blueprint('main', __name__, url_prefix="/user")

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

@main.route("/")
@login_required
def home():
    return render_template("index.html")

@main.route("/make_cv", methods=["POST", "GET"])
@login_required
def make_cv():
    if request.method == 'POST':
        image = request.files['image']
        if image.filename != '':
            image.save(image.filename)
            image_binary = convert_to_binary_data(image.filename)
            os.remove(image.filename)
        else:
            image_binary = None
        bd = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        bd = bd.strftime('%d.%m.%Y')
        if request.form['action'] == 'save draft':
            cv = CV(name=request.form['name'],   surname=request.form['surname'],  birth_date=datetime.datetime.strptime(bd, '%d.%m.%Y').date(),
                    user_id=current_user.id,  skills=request.form['skills'],   education=request.form['education'],
                    job_exp=request.form['job_exp'], image=image_binary)
            db.session.add(cv)
            db.session.commit()
            session["cv_id"] = cv.id
            return render_template("make_cv.html", cv=cv)
        html_sample = f""" <h1>{request.form["name"]} {request.form["surname"]}</h1>"""
        if image_binary is not None:
            html_sample += f'<div style="vertical-align:top;display:inline-block;">' \
                           f'<img src="data:image/png;base64,{base64.b64encode(image_binary).decode()}" width=350px height=auto>' \
                           f'</div> ' \
                           f'<div style="width:14px; display:inline-block;"> </div>'
        html_sample += f"""<div style="display:inline-block;">
                           <h3>Birth Date:</h3>
                           <p>{bd}</p>
                           <h3>Skills: </h3>
                           <p> <div style="white-space: pre-line pre-line">{request.form["skills"]}</div> </p>
                           <h4>Education: </h3>
                           <p> <div style="white-space: pre-line">{request.form["education"]}</div> </p>
                           <h3>Job Experience: </h3>
                           <p> <div style="white-space: pre-line">{request.form["job_exp"]}</div> </p>
                           </div>"""
        filename = f"cv_{current_user.name}.pdf"
        pdfkit.from_string(html_sample, output_path=filename)
        response = send_file(filename, as_attachment=True)
        os.remove(filename)
        return response
    get_all_cvs = CV.query.filter_by(user_id=current_user.id)
    unpacked = [item for item in get_all_cvs]
    if len(unpacked) == 0:
        flash('Your CV is empty', 'error')
        return render_template("make_cv.html",
                               cv=CV(name="", surname="", birth_date=datetime.datetime.strptime("01.01.1900", '%d.%m.%Y').date(),
                                     user_id=current_user.id, skills="",  education="",  job_exp='',  image=None))
    last = unpacked[-1]
    return render_template("make_cv.html", cv=last)
