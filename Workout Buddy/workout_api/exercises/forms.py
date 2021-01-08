#used to manage the form for exercises and can add in other input fields

from django import forms
from .models import Exercises
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#inherate UserCreatioForm
class ExercisesForm(forms.ModelForm):

    #nested name space for configurations for forms and keep them in one place
    class Meta:
        #model that will be affected.
        model = Exercises
        #order in which we want the input fields to be in.
        fields = ['exercise', 'sameWeight']

        #custom labels
        labels = {
            "exercise": _('Exercise Name'),
            "sameWeight": _('Same Weight?'),
        }

        #custom help text
        help_texts = {
            "exercise": _('Enter the exercise name'),
            "sameWeight": _('Did you use the same weight for all the sets? Check the box if you did.'),
        }

        #custom error messages
        error_messages = {
            "exercise": {
                'max_length': _('Exercise name is too long'),
            },
        }