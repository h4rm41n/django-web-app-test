from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import FormPeserta, ProgramForm
from .models import Peserta, Program, Pendaftaran
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.models import User
from core.lib import useracak


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


class CreatePendaftaran(View):
    def get(self, request):
        form = FormPeserta
        template_name = 'peserta/pendaftaran_form.html'

        return render(request, template_name, {"form": form, "label": "Pendaftaran Baru"})


    def post(self, request):
        form = FormPeserta(request.POST or None)
        template_name = 'peserta/pendaftaran_form.html'

        if form.is_valid():
            peserta = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.is_staff = True
            user.set_password(user.username)
            user.save()

            peserta.user = user
            peserta.save()

            pendaftaran = Pendaftaran()
            pendaftaran.peserta = peserta
            pendaftaran.program = Program.objects.get(pk=request.POST['program'])
            pendaftaran.save()
            
            return redirect('/')

        return render(request, template_name, {"form": form, "label": "Pendaftaran Baru"})

# class EditProgram(FormMixinPeserta, generic.UpdateView):
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['label'] = "Edit Program"

#         return context


# class DeleteProgram(View):
#     def get(self, req, *args, **kwargs):
#         obj = get_object_or_404(Program, id=kwargs['id'])
#         obj.delete()

#         return redirect('list-program')