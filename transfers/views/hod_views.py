from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from transfers.constants import UserType, CampusType
from transfers.models import PS2TSTransfer, UserProfile
from transfers.utils import update_application

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from transfers.decorators import ad_required

@method_decorator([login_required, ad_required], name='dispatch')
class HODHomeView(generic.TemplateView):
    template_name = 'transfers/common.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

@login_required
@ad_required
def get_hod_data(request):
    response = {}
    try:
        current_user = request.user
        current_user_alias = 'Head Of Department'
        campus_alias = CampusType._member_names_[current_user.userprofile.campus]
        # applications where approval is pending
        pending_applications_qs = PS2TSTransfer.objects.filter(
            hod_email = current_user.email,
            is_supervisor_approved = True,
            is_hod_approved = False,
        ).values(
            'applicant__user__username',
            'applicant__user__first_name', 'applicant__user__last_name',
            'cgpa', 'thesis_locale', 'supervisor_email',
            'thesis_subject', 'name_of_org', 'expected_deliverables'
        )
        pending_applications_list = list(pending_applications_qs)
        # approved applications
        approved_applications_qs = PS2TSTransfer.objects.filter(
            hod_email = current_user.email,
            is_supervisor_approved = True,
            is_hod_approved = True,
        ).values(
            'applicant__user__username',
            'applicant__user__first_name', 'applicant__user__last_name',
            'cgpa', 'thesis_locale', 'supervisor_email',
            'thesis_subject', 'name_of_org', 'expected_deliverables'
        )
        approved_applications_list = list(approved_applications_qs)
        response['error'] = False
        response['message'] = 'success'
        response['data'] = {}
        response['data']['user'] = {
            'username': current_user.username,
            'designation': current_user_alias,
            'campus': campus_alias,
            'email': current_user.email

        }
        attributes_for_display = [
            {'display': 'Student ID', 'prop':'applicant__user__username'},
            {'display':'Student First Name','prop':'applicant__user__first_name'},
            {'display':'Student Last Name','prop':'applicant__user__last_name'},
            {'display':'CGPA','prop':'cgpa'},
            {'display': 'Supervisor (on-campus)', 'prop':'supervisor_email'},
            {'display':'Thesis Location','prop':'thesis_locale'},
            {'display':'Thesis Subject','prop':'thesis_subject'},
            {'display':'Organisation','prop':'name_of_org'},
            {'display':'Expected Deliverables','prop':'expected_deliverables'},
        ]
        response['data']['student_pending_attributes'] = attributes_for_display
        response['data']['student_approved_attributes'] = attributes_for_display
        response['data']['data_pending'] = [a for a in pending_applications_list]
        response['data']['data_approved']= [a for a in approved_applications_list]
    except Exception as e:
        response['data'] = {
            'username': current_user.username,
            'designation': current_user_alias,
            'campus': campus_alias,
            'email': current_user.email

        }
        response['error'] = True
        response['message'] = 'error'
    return JsonResponse(response, safe=False)


def approve_transfer_request(request):
    applicant = request.GET['student_username']
    status = request.GET['status']
    approved_by = request.user.userprofile.user_type
    saved = update_application(applicant, approved_by)
    response = {}
    if saved:
        response['error'] = False
        response['message'] = 'Application approved.'
    else:
        response['error'] = True
        response['message'] = 'Failed to approve application!'
    return JsonResponse(response, safe=False)
