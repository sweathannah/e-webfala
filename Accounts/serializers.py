from dj_rest_auth.serializers import LoginSerializer as DjRestAuthLoginSerializer
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer

class LoginSerializer(DjRestAuthLoginSerializer):
    username = None
    

    # def save(self):
    #     request = self.context.get('request')
    #     opts = {
    #         'use_https': request.is_secure(),
    #         'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

    #         ###### USE YOUR TEXT FILE ######
    #         'email_template_name': 'password_reset_form.html',

    #         'request': request,
    #     }
    #     self.reset_form.save(**opts)
        
        
