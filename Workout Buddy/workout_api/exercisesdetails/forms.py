#used to manage the form for exercises and can add in other input fields

from django import forms
from .models import ExercisesDetails
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#inherate UserCreationForm
class ExercisesDetailsForm(forms.ModelForm):

    #nested name space for configurations for forms and keep them in one place
    class Meta:
        #model that will be affected.
        model = ExercisesDetails
        #order in which we want the input fields to be in.
        fields = ['weight', 'set_amount', 'total_reps']

        #custom labels
        labels = {
            "weight": _('Exercise weight'),
            "set_amount": _('Number of sets'),
            "total_reps": _('Number of reps'),
        }

        #custom help text
        help_texts = {
            "weight": _('Enter the amount of weight you did.'),
            "set_amount": _('How many sets did you do with this weight?'),
            "total_reps": _('How many total reps did you do for each set? If you did different number of reps for the sets, add each set individually then'),
        }

        #custom error messages
        error_messages = {
            "weight": {
                'max_value': _('That is a lot of weight! Please enter a number smaller you super human.'),
            },
            "set_amount": {
                'max_value': _('That is a lot of sets! Please enter a number smaller you super human.'),
            },
            "total_reps": {
                'max_value': _('That is a lot of reps! Please enter a number smaller you super human.'),
            },
        }