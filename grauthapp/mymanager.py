from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, Phone_number, password=None, **extra_fields):
        if not Phone_number:
            raise ValueError("Phone number is required ! ")

        user = self.model(Phone_number=Phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, Phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(Phone_number, password, **extra_fields)
