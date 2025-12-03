from django import forms
from .models import UserProfile
import random

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'phone': forms.TextInput(attrs={'placeholder': '10-digit phone number'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # normalize: remove spaces and leading + if you want, for now digits-only
        phone_digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(phone_digits) < 10:
            raise forms.ValidationError("Enter a valid phone number (at least 10 digits).")
        return phone_digits

    def save(self, commit=True):
        instance = super().save(commit=False)
        # generate 6-digit OTP
        instance.otp = f"{random.randint(100000, 999999):06d}"
        instance.is_verified = False
        if commit:
            instance.save()
        return instance


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit OTP'}),
        label="OTP"
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp', '').strip()
        if not otp.isdigit():
            raise forms.ValidationError("OTP must be digits only.")
        return otp
