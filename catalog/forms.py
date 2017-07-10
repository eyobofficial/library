from django import forms

class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=120)
    email = forms.EmailField(required=False)
    body = forms.CharField(label='Message', widget=forms.Textarea)

    def email_message(self):
        pass