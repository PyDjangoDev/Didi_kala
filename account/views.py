from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password 
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone 
from django.utils.crypto import get_random_string
from django.views import View
from django.core.cache import cache
from .models import User
from utils.get_ip import get_user_ip
from utils.send_email import send_email
import jdatetime
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
            print(otp)
            true_ip = (get_user_ip(request)).replace('.','_')
            
            cache_data={
                'email' : email,
                'password' : make_password(password),
                'otp' : otp,
                'ip' : true_ip
            }
            
            cache_key = f'otp_{true_ip}'
            
            cache.set(cache_key,cache_data,timeout=300)
            
            
            now = timezone.now()
            persian_datetime = jdatetime.datetime.fromgregorian(datetime=now)
            persian_datetime_str = persian_datetime.strftime('%Y/%m/%d - %H:%M')
            
            persian_date = persian_datetime.strftime('%d %B %Y')
            persian_time = persian_datetime.strftime('%H:%M')
            
            
            send_email(
                subject='کد تایید فروشگاه دیدیکالا',
                to=email,
                context={
                    'otp': otp,
                    'email': email,
                    'send_date': persian_date,  
                    'send_time': persian_time,  
                    'send_datetime': persian_datetime_str  
                },
                template_name='email_templates/send_otp.html'
            )            
            
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
        
        if result:
            return render(request,'otp.html',context={        
                                                          
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
            email = result.get('email')
            final_code = f'{num1}{num2}{num3}{num4}{num5}'
            
            
            if not all([num1, num2, num3, num4, num5]):
                return render(request, 'otp.html', {
                    'otp_error': True ,
                    'email': email  
                })
            
            if len(num1) != 1 or len(num2) != 1 or len(num3) != 1 or len(num4) != 1 or len(num5) != 1 :
                return render(request,'otp.html',{
                    'otp_len_error' : True,
                    'email': email 
                })
                
            final_code = f'{num1}{num2}{num3}{num4}{num5}'
            if result['otp'] != final_code:
                # شمارش تعداد تلاش‌های ناموفق
                attempt_key = f'attempt_{result.get("ip")}'
                attempts = cache.get(attempt_key, 0) + 1
                cache.set(attempt_key, attempts, timeout=300)
                
                
                remaining_attempts = 3 - attempts
                if remaining_attempts <= 0:
                    # حذف کش بعد از ۳ تلاش ناموفق
                    ip = get_user_ip(request)
                    cache_key = f'otp_{ip.replace(".", "_")}'
                    cache.delete(cache_key)
                    cache.delete(attempt_key)
                    return render(request, 'otp.html', {
                        'error': 'تعداد تلاش‌های شما به پایان رسیده است. لطفاً دوباره ثبت‌نام کنید',
                        'error_type': 'max_attempts',
                        'email': email
                    })
                
                return render(request, 'otp.html', {
                    'error': f'کد تایید اشتباه است. {remaining_attempts} تلاش دیگر دارید',
                    'error_type': 'wrong_code',
                    'email': email,
                    'remaining_attempts': remaining_attempts
                })
                
            user = User(
                username=result['email'],
                email=result['email'],
                password=result['password']
            )    
            user.save()
            
            ip = get_user_ip(request)
            cache_key = f'otp_{ip.replace(".", "_")}'
            cache.delete(cache_key)
            attempt_key = f'attempt_{result.get("ip")}'
            cache.delete(attempt_key)
            
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
