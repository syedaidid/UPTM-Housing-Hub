from django import forms
from .models import HousingPost, Image

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CreateNewPostForm(forms.ModelForm):
    # GENDER_CHOICES = [
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    # ]

    # title = forms.CharField(widget=forms.TextInput())
    # description = forms.CharField(widget=forms.Textarea())
    # gender = forms.ChoiceField(choices=GENDER_CHOICES)
    # number_of_people = forms.IntegerField()
    # deposit = forms.DecimalField()
    # monthly_payment = forms.DecimalField()
    # furnished = forms.CharField(widget=forms.Textarea())
    # facilities = forms.CharField(widget=forms.Textarea())
    image = MultipleFileField(label='image', required=False)

    class Meta:
        model = HousingPost 
        fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities', 'address']


class ImageForm(forms.ModelForm):
    image = MultipleFileField(label='image', required=False)

    class Meta:
        model = Image
        fields = ['image', ]

class PostUpdateForm(forms.ModelForm):
    image = MultipleFileField(label='image', required=False)

    class Meta:
        model = HousingPost
        fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities', 'image']