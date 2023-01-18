from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **args):
        if not email:
            raise ValueError("Provide Valid Email")

        email = self.normalize_email(email)
        user = self.model(email=email, **args)
        hashed_password = make_password(password)
        user.set_password(make_password(hashed_password))
        user.save()
        return user

    def create_superuser(self, email, password, **args):
        args.setdefault("is_staff", True)
        args.setdefault("is_superuser", True)
        args.setdefault("is_active", True)

        if args.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if args.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **args)
