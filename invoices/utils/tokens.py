from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordResetToken(PasswordResetTokenGenerator):
    pass

password_reset_token = PasswordResetToken()
