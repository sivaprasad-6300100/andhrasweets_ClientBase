from django import forms
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "phone"]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter phone number"}),
        }


        # Disable Django automatic unique validation
    def validate_unique(self):
        pass



class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")

