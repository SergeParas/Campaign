from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')

class CampaignForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description')
    valid_from = DateTimeField('Début de validité (AAAA-MM-JJ HH:MM)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    valid_until = DateTimeField('Fin de validité (AAAA-MM-JJ HH:MM)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    submit = SubmitField('Enregistrer')

class QuestionForm(FlaskForm):
    text = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Ajouter la question')