
from flask import render_template, request, redirect, url_for, flash
from . import guest_bp
from ..models import Campaign, Question, Response, Answer
from .. import db
from datetime import datetime

@guest_bp.route('/invite/<token>')
def invite_token(token):
    campaign = Campaign.query.filter_by(token=token).first_or_404()
    now = datetime.now()
    if (campaign.valid_from and now < campaign.valid_from) or (campaign.valid_until and now > campaign.valid_until):
        return render_template('guest/invite_expired.html', campaign=campaign)
    return render_template('guest/survey.html', campaign=campaign)

@guest_bp.route('/')
def survey_list():
    now = db.func.now()
    campaigns = Campaign.query.filter(
        db.or_(Campaign.valid_from == None, Campaign.valid_from <= now),
        db.or_(Campaign.valid_until == None, Campaign.valid_until >= now)
    ).all()
    return render_template('guest/survey_list.html', campaigns=campaigns)

@guest_bp.route('/campaign/<int:campaign_id>', methods=['GET','POST'])
def fill_survey(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if request.method == 'POST':
        guest_identifier = request.form.get('guest_identifier', 'Anonyme')
        response = Response(campaign=campaign, guest_identifier=guest_identifier)
        db.session.add(response)
        db.session.commit()
        for q in campaign.questions:
            answer_text = request.form.get(f'question_{q.id}')
            ans = Answer(response=response, question_id=q.id, answer_text=answer_text)
            db.session.add(ans)
        db.session.commit()
        flash('Merci pour votre participation !')
        return redirect(url_for('guest.survey_list'))
    return render_template('guest/survey.html', campaign=campaign)