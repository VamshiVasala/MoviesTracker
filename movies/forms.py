from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'image_url','genres','cast']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Movie Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 4}),
            'year': forms.NumberInput(attrs={'placeholder': 'Enter release year'}),
            'image_url': forms.HiddenInput(),
            'genres': forms.HiddenInput(),
            'cast': forms.HiddenInput(),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year:
            raise forms.ValidationError("Year is required")
        if year < 1900 or year > 2100:
            raise forms.ValidationError("Enter a valid year")
        return year
