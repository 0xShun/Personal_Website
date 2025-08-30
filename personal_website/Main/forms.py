from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # Honeypot field to catch bots
    honeypot = forms.CharField(required=False, 
                              widget=forms.TextInput(attrs={'style': 'display:none !important', 
                                                          'tabindex': '-1',
                                                          'autocomplete': 'off'}),
                              label="Leave this field empty")
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'website', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'notion-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email (not published)', 'class': 'notion-input'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com (optional)', 'class': 'notion-input'}),
            'content': forms.Textarea(attrs={'placeholder': 'Your comment...', 'rows': 4, 'class': 'notion-textarea'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        # If honeypot is filled, it's probably a bot
        if cleaned_data.get('honeypot'):
            raise forms.ValidationError("Bot detected!")
        return cleaned_data
