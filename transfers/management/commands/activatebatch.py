from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from transfers.models import PS2TSTransfer,TS2PSTransfer,UserProfile
from transfers.constants import UserType

import csv
import os

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    def _activate(self):
        filename = 'fd_list_19-09-2020.csv'
        f = os.path.join(BASE_DIR, 'media', filename)
        ## Deactivating all student users first
        print("Deactivating all students... ", end="")
        for u in User.objects.filter(userprofile__user_type=UserType.STUDENT.value):
            u.is_active = False
            u.save()
        print("Done.")
        ## Activating student users present in list
        with open(f) as data_file:
            reader = csv.reader(data_file)
            next(reader) # skipping the header row
            for col in reader:
                username = col[0]
                print(username)
                try:
                    try:
                        user1 = User.objects.get(username=username)
                    except:
                        print("no such user")
                    try:
                        ps_ts = PS2TSTransfer.objects.get(applicant = user1.userprofile)
                        ps_ts.delete()
                    except:
                        print('no ps_ts')
                    try:
                        ts_ps = TS2PSTransfer.objects.get(applicant = user1.userprofile)
                        ts_ps.delete()   
                    except:
                        print('no ts_ps')
                    user1.is_active = True
                    user1.save()
                except Exception as e:
                    print(e)
                    print(username, 'NOT activated!')
                else:
                    print(username, 'activated successfully!')

    def handle(self, *args, **kwargs):
        self._activate()

