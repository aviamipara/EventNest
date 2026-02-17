import ssl
from django.core.mail.backends.smtp import EmailBackend

class SSLEmailBackend(EmailBackend):
    """
    Custom EmailBackend to bypass SSL verification.
    Use this only for development/debugging when facing SSL Cert errors.
    """
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            
            # Create an unverified SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            if self.use_tls:
                self.connection.starttls(context=context)
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
                
            return True
        except OSError:
            if not self.fail_silently:
                raise
