from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import Member, Saldo, Aposta
from django.db.models import F, Sum
from .forms import StatusForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from datetime import date


######### UPDATE VIEW ####
class CampoUpdate(UpdateView):
    model = Member
    fields = ['casa','status', 'ganho', 'odd']
    template_name = 'formularios/createview.html'
    success_url = reverse_lazy('listar-campo')

######### Create VIEW ####
class CampoCreate(CreateView):
    model = Member
    fields = ['data','casa', 'valor', 'odd', 'ganho', 'hora', 'status' ]
    template_name = 'formularios/createview.html'
    success_url = reverse_lazy('listar-campo')

######### DELETE VIEW ####
class CampoDelete(DeleteView):
    model = Member
    template_name = 'formularios/excluir.html'
    success_url = reverse_lazy('listar-campo')


#### LIST VIEW ###
class CampoList(ListView):
    model = Member
    template_name = 'formularios/campolist.html'

    def get_context_data(self, **kwargs):
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)

        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Calculate the total sum of 'valor' field
        total_valor = Member.objects.filter(status='ganhou').aggregate(total=Sum('ganho'))['total']
        total_valor_pendente = Member.objects.filter(status='pendente').aggregate(total=Sum('valor'))['total']
        total_valor_p_ganhos = Member.objects.filter(status='pendente').aggregate(total=Sum('ganho'))['total']
        possiveis_ganhos = total_valor_p_ganhos - total_valor_pendente
        total_valor_data = \
        Member.objects.filter(status='ganhou', data__range=[start_date, end_date]).aggregate(total=Sum('ganho'))[
            'total']

        # Add the total_valor to the context
        context['total_valor'] = total_valor
        context['total_valor_pendente'] = total_valor_pendente
        context['total_valor_p_ganhos'] = total_valor_p_ganhos
        context['possiveis_ganhos'] = possiveis_ganhos

        return context

#### SALDO ###
def saldo(request):
    mydata = Saldo.objects.all().values()
    total_valor = Saldo.objects.aggregate(total=Sum('valor'))['total']

    context = {
        'mymembers': mydata,
        'total_valor': total_valor,
    }

    return render(request, 'saldo.html', context)

class LucrosDayListView(ListView):
    model = Member
    template_name = 'formularios/lucros_day.html'
    context_object_name = 'total_ganho_per_day'

    def get_queryset(self):
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)

        queryset = (
            Member.objects
            .filter(status='ganhou', data__range=[start_date, end_date])
            .values('data')
            .annotate(total_ganho=Sum('ganho'))
        )

        return queryset