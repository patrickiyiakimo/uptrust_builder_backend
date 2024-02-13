from flask import Flask,render_template, request, jsonify, flash
from emails import EmailGenerator
import logging, os, requests, json
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from config import app, db, Email


""" FORMS """

class Uploade_CV(FlaskForm):
    cv_file = FileField("CV")
    submit = SubmitField("Upload Cv")

@app.route('/')
def home():
    return "Hello There"


@app.route('/cv-analyser', methods=['POST', 'GET'])
def cv_analyser():
    """
    Using CV model over here
    PARAMETERS: CV document
                Job requirements
    """
    file = Uploade_CV()
    cv_file = file.cv_file.get()

    # with open()
    return jsonify({'Rate': cv_file,
                    'status_code': 200})

@app.route('/email-writer', methods=['POST', 'GET'])
def email_writer():
    # Check if user.id of student has a CV stored in the database
    # Else Cv is necessary

    """ Generate the Email
    """
    if request.method == 'POST':
        job_desc = request.get_json()["job_description"]
        appl_name = request.get_json()["applicant_name"]
        appl_email = request.get_json()["applicant_email"]
        user_id = request.get_json()["user_id"]
        
        # print(job_desc)
        # print(appl_email)
        # print(appl_name)
        # # print(os.getenv('API_KEY'))
        try:
            _email = EmailGenerator()
            email = _email.generate_email(job_description=job_desc, applicant_name=appl_name, applicant_email=appl_email)
            with app.app_context():
                new_user = Email(email=email,
                                 user_id=user_id,
                                 applicant_name=appl_name,
                                 applicant_email=appl_email,
                                 job_description=str(json.dumps(job_desc)))
                print(_email)
                db.session.add(new_user)
                db.session.commit()
            return jsonify({'message': _email.generate_email(job_description=job_desc, applicant_name=appl_name, applicant_email=appl_email),
                        'status_code': 200})
        except ValueError as err:
            logging.debug(err)
            return jsonify({
                "message": "failed",
                "status_code": 400
            })
    return jsonify({
        "message": "This api receives a post request. failed",
        "status_code": 400
    })



@app.route('/followback_email')
def followback_email():
    pass

@app.route('/job-recommendation')
def job_recommendation():
    pass

""" Notifications """


if __name__ == "__main__":
    app.run(host='localhost', debug=True)