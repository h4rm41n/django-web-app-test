from django.contrib import admin
from peserta.models import Peserta, Program


class PesertaAdmin(admin.ModelAdmin):
    # list_display = ['nama', 'program', 'alamat']
    list_display = ('nama_peserta', 'alamat',)
    # list_editable = ['program']

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('nama_program', 'biaya', 'keterangan',)


admin.site.register(Peserta, PesertaAdmin)
admin.site.register(Program, ProgramAdmin)