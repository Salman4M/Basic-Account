from django.shortcuts import render,redirect

# Create your views here.
from .forms import LoginForm,RegisterForm,ActivationForm,ResetPasswordForm,ResetPassword2Form,ResetPasswordCompleteForm,ChangePasswordForm
from django.contrib.auth import login,logout,get_user_model,authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


from django.utils.encoding import smart_str,smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from helpers.generator import Generator
from django.contrib import messages

User=get_user_model()

def login_view(request):
    form=LoginForm()

    if request.method=='POST':
        form=LoginForm(request.POST or None)

        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('account:home')

    context={'form':form}

    return render(request,'login.html',context)




def register_view(request):
    form = RegisterForm()
    if request.method=='POST':
        form=RegisterForm(request.POST or None)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            uuid=urlsafe_base64_encode(smart_bytes(user.id))
            code=Generator().check_code(size=6)
            user.activation_code=code
            user.save()
            send_mail(
                'Activate Your Account',
                f'your activation code {code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect ('account:activation',uuid=uuid)
        
    context={'form':form}


    return render(request,'register.html',context)


def activation_view(request,uuid):
    print(uuid)
    id=smart_str(urlsafe_base64_decode(uuid))
    user=User.objects.get(id=id)
    form=ActivationForm(instance=user)

    if request.method == 'POST':
        form=ActivationForm(request.POST or None, instance=user)
        if form.is_valid():
            user.is_active=True
            user.activation_code=None
            user.save()
            messages.success(request,'Your account has been succcessfully activated')

            return redirect('account:login')
        
    context={'form':form}

    return render(request,'activation.html',context)
        


def reset_password_view(request):
    form=ResetPasswordForm()

    if request.method=='POST':
        form = ResetPasswordForm(request.POST or None)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user=User.objects.get(email=email)

            uuid=urlsafe_base64_encode(smart_bytes(user.id))
            code=Generator().check_code(size=6)
            user.reset_password_code=code
            user.save()
                  
            send_mail(
                'Reset Password',
                f'code to reset your password is: {code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                )
            return redirect('account:reset-code',uuid=uuid)

        
    context={"form":form}

    return render(request,'reset_password.html',context)




def reset_password_code_view(request,uuid):
    id=smart_str(urlsafe_base64_decode(uuid))
    user=User.objects.get(id=id)
    form=ResetPassword2Form(instance=user)

    if request.method=='POST':
        form=ResetPassword2Form(request.POST or None,instance=user)

        if form.is_valid():
            user.reset_password_code=None
            token=PasswordResetTokenGenerator().make_token(user)
            user.save()

            return redirect('account:reset-password-complete',uuid=uuid,token=token)
        
    context={'form':form}

    return render(request,'password_complete.html',context)



def reset_password_complete(request,uuid,token):
    id=smart_str(urlsafe_base64_decode(uuid))
    user=User.objects.get(id=id)
    if not PasswordResetTokenGenerator().check_token(user,token):
        message='incorrect'
        messages.error=message
        return redirect('account:login')
    
    form=ResetPasswordCompleteForm()

    if request.method=='POST':
        form=ResetPasswordCompleteForm(request.POST or None)

        if form.is_valid():
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            return redirect('account:login')
    context={'form':form}


    return render(request,'password_done.html',context)


@login_required
def change_password_view(request):
    user=request.user
    form = ChangePasswordForm(instance=user)
    if request.method=='POST':
        form=ChangePasswordForm(request.POST or None, instance=user)

        if form.is_valid():
            sender=form.save(commit=False)
            sender.set_password(form.cleaned_data.get('password1'))
            sender.save()
            auth=authenticate(email=user.email,password=form.cleaned_data.get('password1'))
            login(request,auth)
            return  redirect('account:home')
        

    context={'form':form}

    return render(request,'change_password.html',context)




def logout_view(request):
    logout(request)
    return redirect('account:login')

@login_required
def home_view(request):
    return render(request,'home.html')