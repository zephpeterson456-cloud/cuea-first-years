from django import forms
from .models import Post, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post_type", "title", "content", "image"]

        widgets = {
            "post_type": forms.Select(attrs={
                "class": "form-input",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Give your post a title (optional)",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "What's on your mind?",
                "rows": 5,
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-input",
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]

        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Tell the CUEA First Years community something about yourself...",
                "rows": 4,
                "maxlength": 300,
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "form-input",
            }),
        }


from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason", "details"]

        widgets = {
            "reason": forms.Select(attrs={
                "class": "form-input",
            }),
            "details": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Tell us more (optional)...",
                "rows": 4,
                "maxlength": 500,
            }),
        }
