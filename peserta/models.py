from django.db import models


class Peserta(models.Model):
    nama = models.CharField(max_length=255, blank=True, null=True)
    
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, blank=True, null=True, default=1)
    # program = models.ForeignKey(Program, on_delete=models.CASCADE)

    KOTA = (
        ('mataram', 'Mataram'),
        ('gerung', 'Gerung'),
        ('praya', 'Praya'),
        ('selong', 'Selong'),
        ('tanjung', 'Tanjung'),
    )
    kota = models.CharField(max_length=255, choices=KOTA, blank=True, null=True)
    
    alamat = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Form Peserta"
        verbose_name_plural = "Data Peserta"

    def __str__(self):
        return self.nama


class Program(models.Model):
    nama_program = models.CharField(max_length=255, blank=True, null=True)
    biaya = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama_program