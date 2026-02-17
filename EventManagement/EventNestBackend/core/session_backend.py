from django.contrib.sessions.backends.db import SessionStore as DBSessionStore, CreateError, UpdateError
from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError, transaction, DatabaseError, router
from django.utils import timezone
from core.models import CustomSession

class SessionStore(DBSessionStore):
    @property
    def model(self):
        return CustomSession

    def load(self):
        """
        Loads the session data from the database.
        Since we removed session_data column, we return an empty dict unless
        we decide to store it elsewhere (e.g. cache/cookie).
        """
        try:
            s = CustomSession.objects.get(
                session_key=self.session_key,
                expire_date__gt=timezone.now()
            )
            # Reconstruct session data if user is logged in
            if s.user:
                return {
                    '_auth_user_id': str(s.user.id),
                    '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
                    '_auth_user_hash': s.user.get_session_auth_hash()
                }
            return {}
        except (CustomSession.DoesNotExist, CustomSession.MultipleObjectsReturned):
            self._session_key = None
            return {}

    def create_model_instance(self, data):
        """
        Return a new instance of the session model object, which serves to
        save session data into the database.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user_id = data.get('_auth_user_id')
        user = None
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                pass

        return CustomSession(
            session_key=self._get_or_create_session_key(),
            expire_date=self.get_expiry_date(),
            user=user
        )

    def save(self, must_create=False):
        """
        Saves the session data. 
        """
        if self.session_key is None:
            return self.create()
        
        # We simply create/update the row to track existence and expiry
        # But we do NOT encode or save the data payload
        obj = self.create_model_instance(self._session)
        using = router.db_for_write(self.model, instance=obj)
        try:
            with transaction.atomic(using=using):
                if must_create:
                    obj.save(force_insert=True, using=using)
                else:
                    # Update 'user' field as well
                    obj.save(force_insert=False, using=using, update_fields=['expire_date', 'user'])
        except IntegrityError:
            if must_create:
                raise CreateError
            raise
        except DatabaseError:
            if not must_create:
                raise UpdateError
            raise
