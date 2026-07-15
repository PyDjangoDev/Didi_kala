from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
import re



#====================  RegisterForm  ======================= # 

class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=40,
        min_length=10,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': "input-ui pr-2",
            'name': 'email',
            'autofocus': '',
            'placeholder': "ایمیل خود را وارد نمایید",
            'id': 'emailInput'
        }),
        error_messages={
            'required': 'این فیلد اجباری است',
            'min_length': 'ایمیل باید حداقل 10 کاراکتر باشد'
        }
    )
    
    password = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "input-ui pr-2",
            'name': 'password',
            'id': "passwordInput",
            'placeholder': "رمز عبور خود را وارد نمایید"
        }),
        error_messages={
            'required': 'این فیلد اجباری است',
            'min_length': 'رمز عبور باید حداقل 8 کاراکتر باشد'
        }
    )
    
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': "custom-control-input",
            'name': 'terms',
            'id': 'customCheck3'
        }),
        error_messages={
            'required': 'برای ثبت نام باید قوانین را بپذیرید'      
        }
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise forms.ValidationError("ایمیل نمی‌تواند خالی باشد")
        
        if email:
            user = User.objects.filter(email=email).first()
            if user is not None:
                raise forms.ValidationError('این ایمیل قبلاً در سیستم ثبت شده است')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise forms.ValidationError("لطفا یک ایمیل معتبر وارد کنید")
        
        allowed_chars = r'^[a-zA-Z0-9@._%+-]+$'
        if not re.match(allowed_chars, email):
            raise forms.ValidationError("ایمیل باید فقط با حروف انگلیسی وارد شود")
        
        if ' ' in email:
            raise forms.ValidationError("ایمیل نباید شامل فاصله باشد")
        
        
        next_part_of_email = email.split('@')[1].lower()
        
        temp_mail_domains = [
        'tempmail.com', 'temp-mail.org', 'guerrillamail.com', 
        'mailinator.com', '10minutemail.com', 'throwaway.email',
        'trashmail.com', 'yopmail.com', 'maildrop.cc', 
        'fakeinbox.com', 'dispostable.com', 'emltmp.com',
        'nowmymail.com', 'spamgourmet.com', 'tempemail.net',
        'guerrillamail.net', 'guerrillamail.org', 'mailinator.net',
        '10minutemail.net', '10minutemail.org', 'yopmail.fr',
        'yopmail.net', 'yopmail.org', 'mailinator.org',
        'tempmail.net', 'tempmail.org', 'temp-mail.net',
        'temp-mail.info', 'mailnator.com', 'spambox.us',
        'spambox.info', 'trash2000.com', 'wegwerfmail.com',
        'wegwerfmail.net', 'wegwerfmail.org'
    ]
        
        
        if next_part_of_email in temp_mail_domains:
            raise forms.ValidationError("استفاده از ایمیل موقت (Temp Mail) مجاز نیست")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
    
        if not password:
            raise forms.ValidationError("رمز عبور نمی‌تواند خالی باشد")
    
        if len(password) < 8:
            password_len = len(password)
            raise forms.ValidationError(f"رمز عبور باید حداقل ۸ کاراکتر باشد . طول رمز عبور فعلی {password_len} است")
    
        if len(password) > 20:
            password_len = len(password)
            raise forms.ValidationError(f" رمز عبور نباید بیشتر از ۲۰ کاراکتر باشد . طول رمز عبور فعلی {password_len} است")

    # مجاز: حروف انگلیسی، اعداد، @، نقطه، خط تیره، زیرخط
        if not re.match(r'^[A-Za-z0-9@._-]+$', password):
            raise forms.ValidationError("رمز عبور باید فقط شامل حروف انگلیسی، اعداد و کاراکترهای @ . _ باشد")
    
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف داشته باشد")
    
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("رمز عبور باید حداقل یک عدد داشته باشد")
    
        if ' ' in password:
            raise forms.ValidationError("رمز عبور نباید شامل فاصله باشد")
    
        return password
    
    
    
    def clean(self):
        cleaned_data = super().clean()

        
        return cleaned_data


#====================  LoginForm  ======================= # 
    
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': "input-ui pr-2",
            'name': 'email',
            'placeholder': "ایمیل خود را وارد نمایید",
            'autofocus': '',
            'id': 'loginEmailInput'
        })
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "input-ui pr-2",
            'name': 'password',
            'placeholder': "رمز عبور خود را وارد نمایید",
            'id': 'loginPasswordInput'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'name' : 'remember_me' ,
            'class' : 'custom-control-input',
            'id' : 'customCheck3'
            
        })
        
    )
    
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise forms.ValidationError('ایمیل نمی‌تواند خالی باشد')
        
        if len(email) < 11 : 
            raise forms.ValidationError('لطفا یک ایمیل معتبر وارد کنید')
        
        
        # بررسی الگوی ایمیل
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise forms.ValidationError("لطفا یک ایمیل معتبر وارد کنید")
        
        # بررسی انگلیسی بودن
        allowed_chars = r'^[a-zA-Z0-9@._%+-]+$'
        if not re.match(allowed_chars, email):
            raise forms.ValidationError("ایمیل باید فقط با حروف انگلیسی وارد شود")
        
        if ' ' in email:
            raise forms.ValidationError("ایمیل نباید شامل فاصله باشد")
        
        if email :
            user = User.objects.filter(email=email).first()
            if user is None :
                raise forms.ValidationError('کاربر با این ایمیل در سیستم ثبت نشده است')
            

        self.cleaned_data['user'] = User.objects.filter(email=email).first()

            
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = self.cleaned_data.get('user')
        
        if not password:
            raise forms.ValidationError("رمز عبور نمی‌تواند خالی باشد")
    
        if len(password) < 8:
            password_len = len(password)
            raise forms.ValidationError(f"رمز عبور باید حدقل 8 کاراکتر باشد (رمز عبور فعلی {password_len} کاراکتر است)")
    
        if len(password) > 20:
            password_len = len(password)
            raise forms.ValidationError(f'رمز عبور نباید بیشتر از 20 کاراکتر باشد (رمزعبور فعلی است{password_len})')
    
        if not re.match(r'^[A-Za-z0-9@._-]+$', password):
            raise forms.ValidationError("رمز عبور باید فقط شامل حروف انگلیسی، اعداد و کاراکترهای @ . _ باشد")
    
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("رمز عبور باید حداقل یک حرف داشته باشد")
    
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("رمز عبور باید حداقل یک عدد داشته باشد")
    
        if ' ' in password:
            raise forms.ValidationError("رمز عبور نباید شامل فاصله باشد")
        
        if password :
            if user and not check_password(password, user.password):
                raise forms.ValidationError('رمز عبور نادرست می باشد')


        return password
    
    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data
    
