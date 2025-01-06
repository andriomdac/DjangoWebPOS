from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Brand
from .forms import BrandForm, BrandUpdateForm
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages


class BrandCreateView(CreateView):
    model = Brand
    template_name = 'brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Marca "{self.object.name}" criada com sucesso!')
        return response


class BrandListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class BrandUpdateView(UpdateView):
    model = Brand
    template_name = 'brand_update.html'
    form_class = BrandUpdateForm
    success_url = reverse_lazy('brand_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Marca "{self.object.name}" alterada com sucesso!')
        return response


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brand'


def brand_delete_view(request, pk):
    brand_object = get_object_or_404(Brand, id=pk)
    if request.method == 'POST':
        try: 
            brand_object.delete()
            messages.success(request, f'Marca "{brand_object.name}" deletada com sucesso!')
            return redirect('brand_list')
        except ProtectedError:
            return render(request, template_name='brand_delete.html', context={
                'object': brand_object,
                'message': f'Não é possível deletar a marca "{brand_object.name}", pois está sendo utilizada por um ou mais produtos'
                })
    return render(request, template_name='brand_delete.html', context={'object': brand_object})