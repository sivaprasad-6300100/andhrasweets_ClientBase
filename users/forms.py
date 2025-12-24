from django import forms
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "phone"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter your name"
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "Enter 10-digit phone number",
                "inputmode": "numeric",
                "pattern": "[0-9]{10}",  # Exactly 10 digits
                "maxlength": "10",       # Correct HTML attribute
                "title": "Enter exactly 10 digits"
            }),
        }

    # Optional: Disable Django automatic unique validation
    def validate_unique(self):
        pass

        

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")

