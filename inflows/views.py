from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Inflow
from .forms import InflowCreateForm
from django.urls import reverse_lazy
from products.models import Product


def inflow_create_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = InflowCreateForm()
    if request.method == 'POST':
        form = InflowCreateForm(request.POST)
        if form.is_valid():
            inflow = form.save(commit=False)
            inflow.product = product
            inflow.save()
            return redirect('inflow_list')
    if request.method == 'GET':
        return render(request, template_name='inflow_create.html', context={'form': form, 'product': product})

            



class InflowListView(ListView):
    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    ordering = ['-created_at']

    def get_context_data(self):
        context = super().get_context_data()
        return context