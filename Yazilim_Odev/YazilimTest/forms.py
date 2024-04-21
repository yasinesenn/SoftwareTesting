from django import forms
from .models import GitHubDepo
from django.core.validators import URLValidator

class GitHubDepoForm(forms.ModelForm):
    class Meta:
        model = GitHubDepo
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Repo URL'}),
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        control_Url = URLValidator()
        if not url.endswith('.git'):
            raise forms.ValidationError(".git uzantılı bir GitHub repository URL'si girmelisiniz.")
        
        try:
            control_Url(url)

        except forms.ValidationError:

            raise forms.ValidationError("Lütfen geçerli bir URL girin.")
        return url
    
    