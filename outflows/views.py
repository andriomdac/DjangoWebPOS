from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Outflow
from .forms import OutflowCreateForm
from django.urls import reverse_lazy
from products.models import Product


def outflow_create_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OutflowCreateForm()
    if request.method == 'POST':
        form = OutflowCreateForm(request.POST)
        if form.is_valid():
            outflow = form.save(commit=False)
            outflow.product = product
            outflow.save()
            return redirect('outflow_list')
    return render(request, template_name='outflow_create.html', context={'form': form, 'product': product})


class OutflowListView(ListView):
    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    ordering = ['-created_at']