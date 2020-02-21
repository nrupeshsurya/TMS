from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from transfers.constants import TransferType
 
from transfers.models import DeadlineModel
 
from transfers.utils import update_psd_data, get_deadline_status
from transfers.forms import PSDForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from transfers.decorators import psd_required

@method_decorator([login_required, psd_required], name='dispatch')
class PSDview(generic.TemplateView):
    form_class = PSDForm
    initial = {'key': 'value'}
    template_name = 'transfers/psd_dashboard.html'
    context = {}

    def get(self, request, *args, **kwargs):
        # To update is_active fields
        get_deadline_status(TransferType.PS2TS.value)
        get_deadline_status(TransferType.TS2PS.value)
        form = self.form_class(instance=DeadlineModel.objects.all().first())
        self.context = {
            'form': form
        }
        return render(request, self.template_name, self.context)
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            update_psd_data(form)

        # To update is_active fields
        get_deadline_status(TransferType.PS2TS.value)
        get_deadline_status(TransferType.TS2PS.value)
        form = self.form_class(instance=DeadlineModel.objects.all().first())
        self.context = {
            'form': form
        }
        return render(request, self.template_name, self.context)

def get_form_data(request, *args, **kwargs):
    template_name = 'transfers/psd_dashboard.html'
    form = PSDForm(request.POST)
    if form.is_valid():
        update_psd_data(form)
    # To update is_active fields
    get_deadline_status(TransferType.PS2TS.value)
    get_deadline_status(TransferType.TS2PS.value)
    form = PSDForm(instance=DeadlineModel.objects.all().first())
    context = {
        'form'  : form
    }
    return render(request, template_name, context)

@login_required
@psd_required
def get_PSD_data(request, *args, **kwargs):
    response = {}
    try:
        DeadlineModel.objects.first().deadline_PS2TS

        deadline_PS2TS = DeadlineModel.objects.first().deadline_PS2TS
        deadline_TS2PS = DeadlineModel.objects.first().deadline_TS2PS
        is_active_PS2TS = DeadlineModel.objects.first().is_active_PS2TS
        is_active_TS2PS = DeadlineModel.objects.first().is_active_TS2PS
        message = DeadlineModel.objects.first().message

        response['data'] = {
            'deadline_PS2TS': deadline_PS2TS,
            'deadline_TS2PS': deadline_TS2PS,
            'is_active_PS2TS': is_active_PS2TS,
            'is_active_TS2PS': is_active_TS2PS,
            'message': message
        }
        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        response['data'] = {}
        response['error'] = True
        response['message'] = 'error'
    return JsonResponse(response, safe=False)
