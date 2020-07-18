from django import forms
from peserta.models import Peserta, Program


class FormBiasa(forms.Form):
    nama = forms.CharField(required=True)
    program = forms.CharField(required=False)
    alamat = forms.CharField(required=False, widget=forms.Textarea())


class FormPeserta(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = '__all__'


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
