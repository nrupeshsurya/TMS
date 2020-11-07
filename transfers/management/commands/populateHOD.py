from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

import csv

from transfers.models import * #NOQA
from transfers.constants import UserType, CampusType


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='File from which data is to be read')
        parser.add_argument('campus', type=str, help='Campus')

    def _create(self, filename, campus):
        hod_password_file = open("hodPassword.txt", 'w')
        hod_error_file = open("hodError.txt", 'w')
        with open(filename) as data_file:
            reader = csv.reader(data_file)
            # skipping the header
            next(reader, None)
            for column in reader:
                hod_email = column[-1] # Hyd Campus
                temp_password = get_random_string(8)
                print(hod_email, end= " ")
                try:
                    user_obj, created = User.objects.get_or_create(
                        username=hod_email,
                        password=temp_password,
                        email=hod_email,
                    )
                    if created:
                        # some formatting issue in the csv
                        # please remove this if csv if fine
                        first_name = column[2]
                        user_obj.first_name = first_name
                        user_obj.save()
                        user_obj.userprofile.user_type = UserType.HOD.value
                        user_obj.userprofile.campus = CampusType._member_map_[campus].value
                        user_obj.userprofile.save()
                    print('UserProfile created')
                    data_to_write = column[1] + ", " + str(temp_password) + "\n"
                    hod_password_file.write(data_to_write)
                except Exception as e:
                    hod_error_file.write(column[1]+'\n')
                    print('UserProfile NOT created')
                    print(e)
                    continue
        # closing the password file
        hod_password_file.close()

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        campus = kwargs['campus']
        self._create(filename, campus)
