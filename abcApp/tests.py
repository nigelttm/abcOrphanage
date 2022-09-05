from django.test import TestCase
from abcApp.models import *
from django.contrib.auth import authenticate
from abcApp.forms import *
# Create your tests here.

class RequestTestCase(TestCase):
    def setUp(self):
        Request.objects.create(request_Text="Tuna", request_Obj="Canned Food")
        Request.objects.create(request_Text="NTUC", request_Obj="Voucher", isPerm = True)

    def test_checkPerm(self):
        """Check Default Perm is working"""
        tuna = Request.objects.get(request_Text="Tuna")
        ntuc = Request.objects.get(request_Text="NTUC")
        self.assertEqual(tuna.isPerm, False)
        self.assertEqual(ntuc.isPerm, True)

    def test_checkCompleted(self):
        """Check Completion is working"""
        tuna = Request.objects.get(request_Text="Tuna")
        tuna.isCompleted = True
        tuna.save()
        newTuna = Request.objects.get(request_Text="Tuna")
        self.assertEqual(newTuna.isCompleted, True)

class UserTestCase(TestCase):
    def setUp(self):
        User.create_user(user_id='admin',password='admin', role='admin')
        User.create_user(user_id='child',password='child', role='child')
        User.create_user(user_id='user',password='user')

    def test_loginValidation(self):
        """Check Login Validation is working"""
        user = User.objects.get(user_id="user")
        checkUser = authenticate(username="user",password="user")
        self.assertEqual(user, checkUser)

    def test_checkRole(self):
        """Check Default Role is working"""
        admin = User.objects.get(user_id="admin")
        child = User.objects.get(user_id="child")
        user = User.objects.get(user_id="user")
        self.assertEqual(admin.role, "admin")
        self.assertEqual(child.role, "child")
        self.assertEqual(user.role, "user")

class SignUpFormTestCase(TestCase):

    def testFormSuccuss(self):
        """Check Sign Up Form is working"""
        form = SignUpForm(data={"user_id": "user1234", "password1": "12345Abc.", "password2": "12345Abc."})
        form.save()
        user = User.objects.get(user_id="user1234")
        checkUser = authenticate(username="user1234",password="12345Abc.")
        self.assertEqual(user, checkUser)

    def testFormFailPasswordNotSame(self):
        """Check Sign Up Form Incorrect Password is working"""
        form = SignUpForm(data={"user_id": "user1234", "password1": "12345Abc.", "password2": "12345"})
        self.assertEqual(form.errors["password2"], ["The two password fields didn’t match."])

    def testFormFailInUseUsername(self):
        """Check Sign Up Form Similar Username Error is working"""
        user = User.create_user(user_id='user1234',password='user')
        form = SignUpForm(data={"user_id": "user1234", "password1": "12345Abc.", "password2": "12345Abc."})
        self.assertEqual(form.errors["user_id"], ['Username "user1234" is already in use.'])

class RequestDonationFormTestCase(TestCase):
    def setUp(self):
        Request.objects.create(request_Text="Tuna", request_Obj="Canned Food")
        Request.objects.create(request_Text="NTUC", request_Obj="Voucher", isPerm = True)

    def testFormSuccuss(self):
        """Check Request Donation Form is working"""
        form = RequestDonationForm(data={"user": "Anonymous", "donation_type": "ninjavan"})
        tuna = Request.objects.get(request_Text="Tuna")
        if not tuna.isPerm:
            tuna.isCompleted = True
            tuna.save()
        form.instance.request = tuna
        form.save()
        newDonation = Donation.objects.get(request_id=tuna)
        self.assertEqual(tuna.isCompleted, True)
        self.assertEqual(tuna.id, newDonation.request_id)

    def testFormIsPermSuccuss(self):
        """Check Request Donation Form is working for Perm items"""
        form = RequestDonationForm(data={"user": "Anonymous", "donation_type": "ninjavan"})
        ntuc = Request.objects.get(request_Text="NTUC")
        if not ntuc.isPerm:
            ntuc.isCompleted = True
            ntuc.save()
        form.instance.request = ntuc
        form.save()
        newDonation = Donation.objects.get(request_id=ntuc)
        self.assertEqual(ntuc.isCompleted, False)
        self.assertEqual(ntuc.id, newDonation.request_id)

