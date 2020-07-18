from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import FormPeserta, FormBiasa, ProgramForm
from .models import Peserta, Program
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View


class Dashboard(generic.TemplateView):
    template_name = 'layout/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['hi'] = "Welcome to my aplication"

        return context


class ListProgram(generic.ListView):
    model = Program


class FormMixin(object):
    form_class = ProgramForm
    model = Program
    success_url = reverse_lazy('list-program')


class CreateProgram(FormMixin, generic.CreateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label"] = "Buat Program Baru"

        return context
  

class EditProgram(FormMixin, generic.UpdateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Edit Program"

        return context


class DeleteProgram(View):
    def get(self, req, *args, **kwargs):
        obj = get_object_or_404(Program, id=kwargs['id'])
        obj.delete()

        return redirect('list-program')





def deleteData(request, id):
    obj = Peserta.objects.filter(id=id)
    if obj.exists() and obj.count() == 1:
        obj = obj.get()
        obj.delete()

        # messages.success(request, 'Delete suskes')
        return redirect(request, '/')

    # messages.success(request, 'Delete Gagal')
    # return HttpResponseRedirect(request, '/')


def listData(request):
    peserta = Peserta.objects.all().order_by('nama')
    return render(request, "peserta/list_data.html",{
        "peserta": peserta,
    })


def formInput(request):
    if request.POST:
        #===== demo membuat form dari model
        # form = FormPeserta(request.POST or None)
        # if form.is_valid():
        #     form.save()
        #     return redirect('/kontrol')

        #===== demo membuat form tanpa model
        form_biasa = FormBiasa(request.POST or None)        
        if form_biasa.is_valid():
            peserta = Peserta()
            peserta.nama = form_biasa.cleaned_data['nama']
            peserta.program = form_biasa.cleaned_data['program']
            peserta.alamat = form_biasa.cleaned_data['alamat']
            peserta.save()

            return redirect('/kontrol')
            
        return render(request, "peserta/form_input.html", {
            "form": form_biasa,
        })

    form = FormBiasa()
    data = {
        "form": form,
    }
    return render(request, "peserta/form_input.html", data)