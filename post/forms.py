from django import forms
from .models import HousingPost

class CreateNewPostForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    title = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea())
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    number_of_people = forms.IntegerField()
    deposit = forms.DecimalField()
    monthly_payment = forms.DecimalField()
    furnished = forms.CharField(widget=forms.Textarea())
    facilities = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = HousingPost 
        fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities']
