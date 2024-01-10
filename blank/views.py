from django.shortcuts import render, redirect
from .models import Member, Saldo, Aposta
from django.db.models import F, Sum
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
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Set date range
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)

        # Query the database for various sums
        ganhos_queryset = Member.objects.filter(status='ganhou')
        pendente_queryset = Member.objects.filter(status='pendente')

        total_valor = ganhos_queryset.aggregate(total=Sum('ganho'))['total']
        total_valor_pendente = pendente_queryset.aggregate(total=Sum('valor'))['total']
        total_valor_p_ganhos = pendente_queryset.aggregate(total=Sum('ganho'))['total']

        possiveis_ganhos = total_valor_p_ganhos - total_valor_pendente
        l_pendente = total_valor_p_ganhos / 2

        # Calculate the total_valor_data within the specified date range
        total_valor_data = ganhos_queryset.filter(data__range=[start_date, end_date]).aggregate(total=Sum('ganho'))['total']

        # Calculate the percentage of Lucro Ganho
        P_lucro = (l_pendente / total_valor_pendente) * 100 if total_valor_pendente != 0 else 0

        # Add the calculated values to the context
        context.update({
            'total_valor': total_valor,
            'total_valor_pendente': total_valor_pendente,
            'total_valor_p_ganhos': total_valor_p_ganhos,
            'possiveis_ganhos': possiveis_ganhos,
            'l_pendente': l_pendente,
            'P_lucro': P_lucro,
        })

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
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)

        queryset = (
            Member.objects
            .filter(status='ganhou', data__range=[start_date, end_date])
            .values('data')
            .annotate(total_ganho=Sum('ganho'))
        )

        return queryset