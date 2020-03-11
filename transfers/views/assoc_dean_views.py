from django.views import generic
from django.http import JsonResponse
from django.shortcuts import render, redirect

from transfers.constants import TransferType, ApplicationsStatus
from transfers.models import PS2TSTransfer, TS2PSTransfer
from transfers.utils import fetch_ps2ts_list, fetch_ts2ps_list, update_application

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from transfers.decorators import ad_required

@method_decorator([login_required, ad_required], name='dispatch')
class AssocDeanHomeView(generic.TemplateView):
    def get(self, request, *args, **kwargs):        
        return render(request,"transfers/ad_home.html")

@method_decorator([login_required, ad_required], name='dispatch')
class AssocDeanLisApplicationstView(generic.ListView):
    def get(self, request, *args, **kwargs):
        if 'type' not in kwargs:
            type_of_request = None
            return redirect('/TMS/assoc-dean/home/')
        else:
            type_of_request = kwargs["type"]
            if int(type_of_request) == TransferType.PS2TS.value:
                return_list = fetch_ps2ts_list()
            elif int(type_of_request) == TransferType.TS2PS.value:
                return_list = fetch_ts2ps_list()
            else:
                return_list = []
        return JsonResponse(return_list, safe=False)

def reject_transfer_request(request):
    applicant = request.GET['student_username']
    status = ApplicationsStatus.REJECTED.value
    rejected_by = request.user.userprofile.user_type
    saved = update_application(applicant, rejected_by, status)
    response = {}
    if saved:
        response['error'] = False
        response['message'] = 'Application rejected.'
    else:
        response['error'] = True
        response['message'] = 'Failed to reject application!'
    return JsonResponse(response, safe=False)
