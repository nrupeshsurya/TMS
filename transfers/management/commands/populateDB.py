from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

import csv

from transfers.models import * #NOQA
from transfers.constants import UserType, CampusType


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='File from which data is to be read')
        parser.add_argument('campus', type=str, help='Campus name in CAPS or ANY if value given in CSV')

    def _create(self, filename, campus):
        student_password_file = open("studentPassword.txt", 'w')
        student_error_file = open("studentError.txt", 'w')
        with open(filename) as data_file:
            reader = csv.reader(data_file)
            # SKIPPING THE HEADER
            next(reader, None)
            for column in reader:
                username = column[0]  ## MODIFY THIS TO MATCH "student ID" COL IN CSV
                student_email = column[-1]  ## MODIFY THIS TO MATCH "email" COL IN CSV
                if campus == "ANY":
                    campus = column[1].upper()  ## MODIFY THIS TO MATCH "campus" COL IN CSV
                campus_val = CampusType._member_map_[campus].value
                temp_password = get_random_string(8)
                print(student_email, end= " ")
                try:
                    user_obj, created = User.objects.get_or_create(
                        username=username,
                        password=temp_password,
                        email=student_email,
                    )
                    if created:
                        # some formatting issue in the csv
                        # please remove this if csv if fine
                        full_name = column[2]  ## MODIFY THIS TO MATCH "student name" COL IN CSV
                        if full_name.endswith('.'):
                            full_name = full_name[:-1]
                        full_name = full_name.strip()
                        last_name = column[2].split()[-1]
                        first_name = column[2].split(' '+last_name)[0]
                        user_obj.first_name = first_name
                        user_obj.last_name = last_name
                        user_obj.save()
                        user_obj.userprofile.user_type = UserType.STUDENT.value
                        user_obj.userprofile.campus = campus_val
                        user_obj.userprofile.save()
                    print('UserProfile created')
                    data_to_write = username + ", " + str(temp_password) + "\n"
                    student_password_file.write(data_to_write)
                except Exception as e:
                    student_error_file.write(username+'\n')
                    print('UserProfile NOT created')
                    print(e)
                    continue
        # closing the password file
        student_password_file.close()
        student_error_file.close()

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        campus = kwargs['campus']
        self._create(filename, campus)
