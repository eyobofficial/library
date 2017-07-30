from django import forms 
from django.core.exceptions import ValidationError

import datetime 

class RenewalForm(forms.Form):
    renewal_date = forms.DateField(help_text='Maximum renewal extension is 3 weeks')

    def clean_renewal_date(self):
        """
        Validate renewal_date
        """
        data = self.cleaned_data.get('renewal_date')

        # Check whether entered date is in the past
        if data < datetime.date.today():
            raise ValidationError('Can not enter a date form the past')

        # Check whether entered date is beyond the maximum allowed 3 week extension
        # if data < datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError('Can not renew beyond 3 weeks')

        return data
        