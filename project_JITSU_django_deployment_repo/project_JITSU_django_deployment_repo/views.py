from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    """
    Google OAuth2 로그인을 구현하는 클래스입니다.
    """
    adapter_class = GoogleOAuth2Adapter

    def complete_login(self, request, app, token, **kwargs):
        try:
            extra_data = self.adapter_class(app).get_user_info(token)
            account = SocialAccount(extra_data=extra_data,
                                    uid=extra_data['sub'],
                                    provider=self.adapter_class().provider_id,
                                    user=token.user)
            account.sync(extra_data)
            account.save()
            return self.get_response(request, account.sociallogin)
        except OAuth2Error:
            return JsonResponse({'error': 'OAuth2Error'})
        except Exception as e:
            return JsonResponse({'error': str(e)})