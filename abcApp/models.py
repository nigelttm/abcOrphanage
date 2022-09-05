from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

# Create your models here.
class CustomUserManager(BaseUserManager):
	def create_user(self, username, password):
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			username=username,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=20, null=False, blank=False, primary_key=True, unique=True)
    role = models.CharField(default="user", max_length=10)

    USERNAME_FIELD = 'user_id'
    objects = CustomUserManager()

    def __str__(self):
        return self.user_id

    def create_user(user_id, password, role=None):
        """
        Creates and saves a User with the given user id, password and role.
        """
        if not user_id:
            raise ValueError('Users must have a user id')

        if role is None:
            role = 'user'
        
        user = User(
            user_id = user_id,
            role = role,
        )

        user.set_password(password)
        user.save()
        return user

class Request(models.Model):
    request_Text = models.CharField(max_length=500, null=True, blank=True)
    request_Obj = models.CharField(max_length=20, null=False, blank=False)
    isCompleted = models.BooleanField(default=False)
    isPerm = models.BooleanField(default=False)

def getUpload(self, filename):
    return f'children/{self.child_id}/{filename}'

class Upload(models.Model):
    upload_name = models.CharField(max_length=20, null=False, blank=False)
    child_id = models.ForeignKey(User, on_delete=models.CASCADE)
    child_object = models.FileField(upload_to=getUpload, validators=[FileExtensionValidator(['mp3','png', 'jpg', 'jpeg', 'gif'])])
    likes = models.PositiveIntegerField(default=0)

class Donation(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    donatedBy = models.CharField(max_length=20, null=False, blank=False, default="Anonymous")
    donation_type = models.CharField(max_length=50, null=False, blank=False)
    delivery_date = models.DateField(null=True)

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, null=False, blank=False)
    visit_date = models.DateField(null=False, blank=False)
    responded = models.BooleanField(default=False)
    status = models.CharField(max_length=50, null=True, blank=False)
    qty = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])

class MoneyDonation(models.Model):
    donatedBy = models.CharField(max_length=20, null=False, blank=False, default="Anonymous")
    nric = models.CharField(max_length=10, null=True)
    qty = models.DecimalField(null=False, blank=False, max_digits=6, decimal_places=2)
    date = models.DateField(null=False)
    yearly = models.BooleanField(default=False)
