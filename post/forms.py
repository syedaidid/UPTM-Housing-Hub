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
    image = MultipleFileField(label='image', required=False)

    class Meta:
        model = HousingPost
        fields = ['title', 'description', 'gender', 'number_of_people', 'deposit', 'monthly_payment', 'furnished', 'facilities', 'accessibilities', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required attribute to False for the fields you want to make not required
        self.fields['description'].required = False
        self.fields['furnished'].required = False
        self.fields['facilities'].required = False
        self.fields['accessibilities'].required = False
        self.fields['address'].required = False

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