from django import forms
from peserta.models import Peserta, Program, Trainer, Kelas


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        exclude = ('user',)
        widgets = {
            'tgl_lahir': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TrainerForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget\
                .attrs['class'] = 'form-control input-sm'
# class FormPendaftaran(forms.ModelForm):

class FormPeserta(forms.ModelForm):
    program_query = Program.objects.all().order_by('nama_program')
    program = forms.ModelChoiceField(queryset=program_query)

    class Meta:
        model = Peserta
        exclude = ('user',)
        widgets = {
            'tgl_lahir': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormPeserta, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget\
                .attrs['class'] = 'form-control input-sm'


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.name == "name":
                visible.field.widget\
                .attrs['autofocus'] = 'autofocus'

            visible.field.widget\
                .attrs['class'] = 'form-control input-sm'


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        exclude = ('peserta',)

    def __init__(self, *args, **kwargs):
        super(KelasForm, self).__init__(*args, **kwargs)
        self.fields['trainer']\
            .queryset = Trainer.objects.all()
        
        for visible in self.visible_fields():
            if visible.name == "trainer":
                visible.field.widget\
                .attrs['multiple'] = 'multiple'

            visible.field.widget\
                .attrs['class'] = 'form-control input-sm'
