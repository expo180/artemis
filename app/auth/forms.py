from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from markupsafe import Markup
import pycountry
from flask_babel import _
class CourseWorkRegistrationForm(FlaskForm):
    email = StringField(
        _('Email'), 
        validators = [
            Length(1, 64),
            Email()
        ]
    )

    country_code = SelectField('Code pays', choices=[], coerce=str)


    first_name = StringField(
        ("Prenom"),
        validators = [
            InputRequired()
        ]
    )

    last_name = StringField(
        ("Nom de famille"),
        validators = [
            InputRequired()
        ]
    )

    areas = [
        ("Design graphique", "Graphisme"),
        ("Design de mouvement", "Motion Design"),
        ("Design web", "Design web"),
        ("UI/UX Design", "UI/UX Design"),
        ("Design d'impression", "Design d'impression"),
        ("Design de marque et d'identité", "Design de marque et d'identité"),
        ("Illustration", "Illustration"),
        ("Design typographique", "Design typographique"),
        ("Graphiques pour les médias sociaux", "Graphiques pour les médias sociaux"),
        ("Graphisme environnemental", "Graphisme environnemental"),
        ("Design de logo", "Design de logo"),
        ("Design d'infographie", "Design d'infographie"),
        ("Design d'application", "Design d'application"),
        ("Design de réalité virtuelle (VR)", "Design de réalité virtuelle (VR)"),
        ("Design de réalité augmentée (AR)", "Design de réalité augmentée (AR)"),
        ("Art numérique", "Art numérique"),
        ("Design de mode", "Design de mode"),
        ("Design d'intérieur", "Design d'intérieur"),
        ("Dessin animé et bande dessinée", "Dessin animé et bande dessinée"),
        ("Merchandising visuel", "Merchandising visuel"),
        ("Présentations d'entreprise", "Présentations d'entreprise"),
        ("Design e-learning", "Design e-learning"),
        ("Design adaptable", "Design adaptable"),
        ("Design de jeu", "Design de jeu"),
        ("Médias imprimés", "Médias imprimés"),
        ("Emballage de produit", "Emballage de produit"),
        ("Art et illustration", "Art et illustration"),
        ("Médias numériques", "Médias numériques"),
        ("Marketing", "Marketing"),
        ("Divertissement", "Divertissement"),
        ("Technologie éducative", "Technologie éducative"),
        ("Édition", "Édition"),
        ("Développement web", "Développement web"),
        ("Développement de marque", "Développement de marque"),
        ("Design de l'information", "Design de l'information"),
        ("Marketing d'événements", "Marketing d'événements")
    ]

        


    phone_number = StringField(
        _("Entrer votre numero de telephone"), 
        validators=[
            InputRequired()
        ]
    )

    default_choice = areas[0][0]

    areas_of_interest = SelectField(
        _("Selectionner la formation"),
        choices=areas,
        default=default_choice
    )

   

    privacy_policy_agreement = BooleanField(
        _("You have read and accepted our <a href=''>Terms and Conditions</a>."),
        validators=[InputRequired()]
    )
