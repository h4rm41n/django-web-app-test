from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import FormPeserta, ProgramForm, KelasForm, TrainerForm
from .models import Peserta, Program, Pendaftaran, Kelas, Trainer
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.models import User
from core.lib import useracak
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



@method_decorator(login_required, name='dispatch')
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



@method_decorator(login_required, name='dispatch')
class PesertaList(generic.ListView):
    model = Peserta
    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class KelasList(generic.ListView):
    model = Kelas


class CreateKelas(generic.CreateView):
    form_class = KelasForm
    model = Kelas
    success_url = reverse_lazy('list-kelas')


class TrainerList(generic.ListView):
    model = Trainer


class CreateTrainer(generic.CreateView):
    form_class = TrainerForm
    model = Trainer
    success_url = reverse_lazy('list-trainer')