from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    try:
        subject = 'Chào mừng bạn đến với Shop Giày!'
        
        # Tạo nội dung HTML cho email
        html_content = render_to_string('email/welcome_email.html', {
            'username': user.username,
            'email': user.email
        })
        
        # Tạo nội dung text cho email (không có HTML)
        text_content = strip_tags(html_content)
        
        # Gửi email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False 