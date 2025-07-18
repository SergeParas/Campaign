from . import admin_bp
from flask import abort, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models import User, Campaign, Question, Answer, Response
from ..forms import LoginForm, CampaignForm, QuestionForm
from .. import db, login_manager
@admin_bp.route('/campaign/<int:campaign_id>/questions', methods=['GET'])
@login_required
def manage_questions(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner_id != current_user.id:
        abort(403)
    return render_template('admin/manage_questions.html', campaign=campaign)

@admin_bp.route('/campaign/<int:campaign_id>/question/<int:question_id>/edit', methods=['GET','POST'])
@login_required
def edit_question(campaign_id, question_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    question = Question.query.get_or_404(question_id)
    if campaign.owner_id != current_user.id or question.campaign_id != campaign.id:
        abort(403)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.text = form.text.data
        db.session.commit()
        flash("Question modifiée avec succès.")
        return redirect(url_for('admin.manage_questions', campaign_id=campaign_id))
    return render_template('admin/edit_question.html', form=form, campaign=campaign, question=question)

@admin_bp.route('/campaign/<int:campaign_id>/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(campaign_id, question_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    question = Question.query.get_or_404(question_id)
    if campaign.owner_id != current_user.id or question.campaign_id != campaign.id:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash("Question supprimée.")
    return redirect(url_for('admin.manage_questions', campaign_id=campaign_id))
# --- Statistiques ---
@admin_bp.route('/campaign/<int:campaign_id>/inspect', methods=['GET'])
@login_required
def campaign_inspect(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.owner_id != current_user.id:
        abort(403)
    responses = Response.query.filter_by(campaign_id=campaign.id).all()
    all_data = []
    for resp in responses:
        ansdict = {a.question_id: a.answer_text for a in resp.answers}
        all_data.append((resp, ansdict))
    nb_resp = len(responses)
    stat_questions = []
    for q in campaign.questions:
        total = 0
        not_null = 0
        for r in responses:
            ans = next((a for a in r.answers if a.question_id == q.id), None)
            total += 1 if ans else 0
            not_null += 1 if ans and ans.answer_text and ans.answer_text.strip() != '' else 0
        stat_questions.append({
            'question': q,
            'total': total,
            'rempli': not_null,
            'taux': f"{((not_null/nb_resp)*100):.0f}%" if nb_resp else '0%'
        })
    return render_template('admin/campaign_inspect.html', campaign=campaign, responses=all_data, stat_questions=stat_questions, nb_resp=nb_resp)
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models import User, Campaign, Question
from ..forms import LoginForm, CampaignForm, QuestionForm
from .. import db, login_manager
from . import admin_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Identifiants invalides ou droits insuffisants.')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('guest.survey_list'))
    campaigns = Campaign.query.filter_by(owner_id=current_user.id).all()
    return render_template('admin/dashboard.html', campaigns=campaigns)

@admin_bp.route('/campaign/new', methods=['GET','POST'])
@login_required
def new_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            title=form.title.data,
            description=form.description.data,
            owner=current_user
        )
        # Gestion dates extraites du form (si renseignées)
        if form.valid_from.data:
            campaign.valid_from = form.valid_from.data
        if form.valid_until.data:
            campaign.valid_until = form.valid_until.data
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/campaign_form.html', form=form)

@admin_bp.route('/campaign/<int:campaign_id>/add_question', methods=['GET','POST'])
@login_required
def add_question(campaign_id):
    form = QuestionForm()
    campaign = Campaign.query.get_or_404(campaign_id)
    if form.validate_on_submit():
        q = Question(text=form.text.data, campaign=campaign)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/question_form.html', form=form, campaign=campaign)