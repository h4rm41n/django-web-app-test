from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import FormPeserta, ProgramForm, KelasForm, TrainerForm, TambahPendaftaranForm
from .models import Peserta, Program, Pendaftaran, Kelas, Trainer
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.models import User
from core.lib import useracak
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# @method_decorator(login_required, name='dispatch')
class Dashboard(LoginRequiredMixin, generic.TemplateView):
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


# class CreateKelas(generic.CreateView):
class CreateKelas(View):
    # form_class = KelasForm
    # model = Kelas
    # success_url = reverse_lazy('list-kelas')

    # def form_valid(self, form):
    #     kelas = form.save(commit=False)
    #     print(kelas.pendaftaran)
    def get(self, request):
        form = KelasForm
        return render(request, "peserta/kelas_form.html", {"form": form})

    def post(self, request):
        form = KelasForm(request.POST or None)
        if form.is_valid():
            kelas = form.save(commit=False)

            for dt in form.cleaned_data['pendaftaran']:
                Pendaftaran.objects.filter(id=dt.id).update(is_register=False)

            kelas.save()

            return redirect('list-kelas')

        return render(request, "peserta/kelas_form.html", {"form": form})


class TrainerList(generic.ListView):
    model = Trainer


class CreateTrainer(generic.CreateView):
    form_class = TrainerForm
    model = Trainer
    success_url = reverse_lazy('list-trainer')

    def form_valid(self, form):
        trainer = form.save(commit=False)
        
        userTrainer = User()
        userTrainer.username = useracak()
        userTrainer.is_staff = True
        userTrainer.set_password(userTrainer.username)
        userTrainer.save()

        trainer.user = userTrainer
        trainer.save()

        return super(CreateTrainer, self).form_valid(form)


class TambahKePendaftaran(View):
    def get(self, request, id):
        data = {
            "peserta": Peserta.objects.get(id=id),
            "form": TambahPendaftaranForm,
        }

        return render(request, "peserta/tambah_ke_pendaftaran.html", data)

    def post(self, request, id):
        peserta = Peserta.objects.get(id=id)
        program = Program.objects.get(id=int(request.POST['program']))
        pendaftaran = Pendaftaran()
        pendaftaran.peserta = peserta
        pendaftaran.program = program
        pendaftaran.save()

        return redirect('list-peserta')


    