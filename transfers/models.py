from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import CampusType, TransferType, UserType, ApplicationsStatus


class UserProfile(models.Model):
    """
    Profile model for each User in the app.
    Keep fields nullable to create a corresponding
    UserProfile model isntance automatically once a User
    model instance is created.
    """
    user_choices = [
        (UserType.STUDENT.value, 'Student'),
        (UserType.SUPERVISOR.value, 'Supervisor'),
        (UserType.HOD.value, 'Head of Department'),
        (UserType.AD.value, 'Associate Dean'),
        (UserType.PSD.value, 'PS-Division'),
    ]
    campus_choices = [
        (CampusType.GOA.value, 'Goa'),
        (CampusType.HYD.value, 'Hyderabad'),
        (CampusType.PILANI.value, 'Pilani'),
    ]

    user = models.OneToOneField(User, primary_key=True,
        on_delete=models.CASCADE)
    campus = models.IntegerField(choices=campus_choices, blank=True,
        null=True)
    contact = models.IntegerField(blank=True, null=True)
    user_type = models.IntegerField(choices=user_choices, blank=True,
        null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile()
        user_profile.user = instance
        user_profile.save()
    instance.userprofile.save()


class PS2TSTransfer(models.Model):
    """
    Model to store the information for
    PS --> TS transfer related queries
    """
    PS2TS = 0
    OTHER = 1
    sub_type_choices = [
        (PS2TS, 'PS to TS (Single Degree)'),
        (OTHER, 'PS-TS/TS-PS to TS-TS (Dual Degree)'),
    ]

    ON_CAMPUS = 0
    OFF_CAMPUS_INDIA = 1
    OFF_CAMPUS_ABROAD = 2
    thesis_locale_choices = [
        (ON_CAMPUS, 'On Campus'),
        (OFF_CAMPUS_INDIA, 'Off Campus (India)'),
        (OFF_CAMPUS_ABROAD, 'Off Campus Abroad'),
    ]
    # linking the application with its applicant
    applicant = models.OneToOneField(UserProfile, primary_key=True,
        on_delete=models.CASCADE)
    # corresponding on-campus supervisor
    supervisor_email = models.EmailField()
    # corresponding hod
    hod_email = models.EmailField()
    # sub-type for application; see choices above
    sub_type = models.IntegerField(choices=sub_type_choices)
    # other details required for the form
    cgpa = models.DecimalField(max_digits=6, decimal_places=2)
    thesis_locale = models.IntegerField(choices=thesis_locale_choices)
    thesis_subject = models.CharField(max_length=150,
        help_text='Broad area/Title of Thesis')
    name_of_org = models.CharField(max_length=100,
        help_text='Name of BITS Campus or Organization where thesis will be carried')
    expected_deliverables = models.TextField(help_text='Expected outcome of thesis')
    # fields to note the status of the application
    is_supervisor_approved = models.IntegerField(default=ApplicationsStatus.PENDING.value)
    is_hod_approved = models.IntegerField(default=ApplicationsStatus.PENDING.value)

    class Meta:
        verbose_name = 'PS to TS Application'
        verbose_name_plural = 'PS to TS Applications'

class TS2PSTransfer(models.Model):
    """
    Model to store the information for
    TS --> PS transfer related queries
    """
    TS2PS = 0
    PSTS2PSPS = 1
    TSTS2TSPS = 2
    sub_type_choices = [
        (TS2PS, 'TS to PS (Single Degree)'),
        (PSTS2PSPS, 'PS-TS to PS-PS (Dual Degree)'),
        (TSTS2TSPS, 'TS-TS to TS-PS (Dual Degree)'),
        ]
    # linking application with its applicant
    applicant = models.OneToOneField(UserProfile, primary_key=True,
        on_delete=models.CASCADE)
    # corresponding hod
    hod_email = models.EmailField()
    # sub-type for application; see choices above
    sub_type = models.IntegerField(choices=sub_type_choices)
    # other details required for the form
    cgpa = models.DecimalField(max_digits=6, decimal_places=2)
    reason_for_transfer = models.TextField()
    name_of_org = models.CharField(max_length=100,
            help_text='Name of BITS Campus or Organization where thesis was being carried')
    # field to note the status of the application
    is_hod_approved = models.IntegerField(default=ApplicationsStatus.PENDING.value)

    class Meta:
        verbose_name = 'TS to PS Application'
        verbose_name_plural = 'TS to PS Applications'

class DeadlineModel(models.Model):
 
    deadline_PS2TS = models.DateTimeField(null = True, blank = True)
    deadline_TS2PS = models.DateTimeField(null = True, blank = True)
    is_active_PS2TS = models.BooleanField(default=False)
    is_active_TS2PS = models.BooleanField(default=False)
    message = models.TextField(null=True,blank=True)
