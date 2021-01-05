#used to manage the form for workouts and can add in other input fields

from django import forms
from .models import Workouts
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#inherate UserCreatioForm
class WorkoutsForm(forms.ModelForm):

    #nested name space for configurations for forms and keep them in one place
    class Meta:
        #model that will be affected.
        model = Workouts
        #order in which we want the input fields to be in.
        fields = ['WName', 'date']

        #custom labels
        labels = {
            "WName": _('Workout name'),
            "date": _('Date (YYYY-MM-DD)'),
        }

        #custom help text
        help_texts = {
            "WName": _('Enter the workout name'),
            "date": _('What day did you first do the workout on?'),
        }

        #custom error messages
        error_messages = {
            "WName": {
                'max_length': _('Workout name is too long'),
            },
        }