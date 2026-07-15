from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password 
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone 
from django.utils.crypto import get_random_string
from django.views import View
from django.core.cache import cache
from django.utils.timezone import timedelta
from .models import User
from utils.get_ip import get_user_ip
from pattern_chacker import CheckPattern 
from .forms import RegisterForm, LoginForm

# Create your views here.

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render (request,template_name='register.html',context={
            'register_form' : register_form
            
        })
        
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
        
            otp = get_random_string(length=5,allowed_chars='0987654321')
            
            true_ip = (get_user_ip(request)).replace('.','_')
            
            cache_data={
                'email' : email,
                'password' : make_password(password),
                'otp' : otp,
                'ip' : true_ip
            }
            
            cache_key = f'otp_{true_ip}'
            cache.set(cache_key,cache_data,timeout=180)
            
            return redirect('otp')
        
        else:
            return render (request,template_name='register.html',context={
                'register_form' : register_form
            
            })
        
class OtpView(View):
    def check_user(self,request):
        ip = get_user_ip(request)
        cache_key = f'otp_{ip.replace('.','_')}'
        cache_ = cache.get(cache_key)
        if cache_ :
            return cache_ 
        else:
            None
            
    def get(self,request):
        result = self.check_user(request)
        
        if result and isinstance(result, dict):
            otp_code = result.get('otp', '')
            return render(request,'otp.html',context={
                'otp' : otp_code
            
            })
        else:
            return redirect('register')

    def post(self,request):
        result = self.check_user(request)
        if result is not None :
            num1 = request.POST.get('input1')
            num2 = request.POST.get('input2')
            num3 = request.POST.get('input3')
            num4 = request.POST.get('input4')
            num5 = request.POST.get('input5')
            otp_code = result.get('otp', '')
            
            if not all([num1, num2, num3, num4, num5]):
                return render(request, 'otp.html', {
                    'otp_error': True ,
                    'otp': otp_code  
                })
            
            if len(num1) != 1 or len(num2) != 1 or len(num3) != 1 or len(num4) != 1 or len(num5) != 1 :
                return render(request,'otp.html',{
                    'otp_len_error' : True,
                    'otp': otp_code 
                })
                
            final_code = f'{num1}{num2}{num3}{num4}{num5}'
            if result['otp'] != final_code :
                return render (request,'otp.html',{
                    'otp_not_true_error' : True,
                    'otp': otp_code 
                })
                
            user = User.objects.create_user(
                username=result['email'],
                email=result['email'],
                password=result['password']
            )    
            user.save()
            
            ip = get_user_ip(request)
            cache_key = f'otp_{ip.replace('.','_')}'
            cache.delete(cache_key)
            
            return redirect('login')
        else:
            raise Http404()

class LoginView(View):
    def get(self,request):
        Login_Form = LoginForm()
        return render(request,'login.html',{
            'Login_Form' : Login_Form
            
        })    
    
    def post(self,request):
        Login_Form = LoginForm(request.POST)
        if Login_Form.is_valid():
            user = Login_Form.cleaned_data.get('user')
            remember_me = Login_Form.cleaned_data.get('remember_me')
            
            login(request, user)
            
            if remember_me :
                request.session.set_expiry(2592000)
                    
            else : 
                request.session.set_expiry(0)
                
            return redirect('home')

        return render(request,'login.html',context={
            'Login_Form' : Login_Form

        })
        
        
def log_out(request):
    logout(request)
    return redirect('home')
    

    
