from typing import Any
from django.contrib.auth import get_user_model,authenticate
from django import forms

User=get_user_model()




class LoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('email','password')


    def get_user(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')

        user = authenticate(email=email,password=password)

        return user
    
    def clean(self):
        user=self.get_user()

        if not user:
            raise forms.ValidationError('Email or password is wrong')
        
        if not user.is_active:
            raise forms.ValidationError('Account is not activated')


        return self.cleaned_data
    


class RegisterForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email','password1','password2')


    
    def clean(self):
        email=self.cleaned_data.get('email')
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')


        user=User.objects.filter(email=email).exists()
        if email and password1 and password2:
            if user:
                raise forms.ValidationError('This user already exists')
            
            if password1!=password2:
                raise forms.ValidationError("password don't match")
            
        else:
            raise forms.ValidationError("Fill all required fields")
        

        return self.cleaned_data
            
    



class ActivationForm(forms.ModelForm):
    code=forms.CharField()
    class Meta:
        model=User
        fields=('code',)

    def clean(self):
        code=self.cleaned_data.get('code')

        if self.instance.is_active:
            raise forms.ValidationError('Your account has already activated. Go to login page')
        if code!=self.instance.activation_code:
            raise forms.ValidationError('Activation code is wrong')
        
        return self.cleaned_data



class ResetPasswordForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=('email',)

    def clean(self):
        email = self.cleaned_data.get('email')
        check_email=User.objects.filter(email=email).exists()

        if not check_email:
            raise forms.ValidationError("can't find an account associated with this email")

        if check_email and not User.objects.get(email=email).is_active:
            raise forms.ValidationError('You need to activate your account first')
        
        return self.cleaned_data
    


class ResetPassword2Form(forms.ModelForm):
    code=forms.CharField()

    class Meta:
        model=User
        fields=('code',)


    def clean(self):
        code = self.cleaned_data.get('code')

        if code!=self.instance.reset_password_code:
            raise forms.ValidationError('Codes dont match')
        

        return self.cleaned_data

        


class ResetPasswordCompleteForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('password1','password2')


    def clean(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')

        if password1 and password2:
            if password1!=password2:
                raise forms.ValidationError('they dont match')
            
        else:
            raise forms.ValidationError('fill the required fields')
    

class ChangePasswordForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('password','password1','password2')


    def clean(self):
        email=self.instance.email
        password=self.cleaned_data.get('password')
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')


        user=authenticate(email=email,password=password)

        if not user:
            raise forms.ValidationError('your current password is incorrect')
        
        if password1!=password2:
                raise forms.ValidationError("passwords don't match")
            

        return self.cleaned_data





    