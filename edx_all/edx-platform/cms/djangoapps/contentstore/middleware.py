from django.core.urlresolvers import reverse

from social_auth.exceptions import AuthAlreadyAssociated
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthCanceled

class AuthCanceledSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def raise_exception(self, request, exception):
        return False

    def get_redirect_uri(self, request, exception):
            if isinstance(exception, AuthCanceled):
                return '/signin'
            else:
                return super(AuthCanceledSocialAuthExceptionMiddleware, self).get_redirect_uri(request, exception)

