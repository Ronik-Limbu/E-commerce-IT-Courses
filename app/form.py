from django import forms
from .models import Profile,Review
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_picture','address','phone']
        
        widgets={
            'profile_picture':forms.FileInput(),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'})
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['rating','comment']
        widgets={
            'rating':forms.Select(choices=[(i,i) for i in range(1,6)],attrs={'class':'form-control'}),
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }


