from django.db import models
from django.contrib.auth.models import User


KOTA = (
    ('mataram', 'Mataram'),
    ('gerung', 'Gerung'),
    ('praya', 'Praya'),
    ('selong', 'Selong'),
    ('tanjung', 'Tanjung'),
)

KELAMIN = (
    ('L', 'Laki'),
    ('P', 'Perempuan'),
)

class Peserta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nama_peserta = models.CharField(max_length=255, blank=False, null=False)
    kelamin = models.CharField(max_length=2, choices=KELAMIN, blank=False, null=False)
    tempat_lahir = models.CharField(max_length=30, blank=False, null=False)
    tgl_lahir = models.DateField(blank=False, null=False)
    nomor_handphone = models.CharField(max_length=15, blank=True, null=True)
    agama = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    sosmed = models.CharField(max_length=255, blank=False, null=False)
    pendidikan_akhir = models.CharField(max_length=255, blank=True, null=True)
    kota = models.CharField(max_length=255, choices=KOTA, blank=False, null=False)
    alamat = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Form Peserta"
        verbose_name_plural = "Data Peserta"

    def __str__(self):
        return self.nama_peserta


class Program(models.Model):
    nama_program = models.CharField(max_length=255, blank=True, null=True)
    biaya = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nama_program


class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nama_trainer = models.CharField(max_length=255, blank=True, null=True)
    kelamin = models.CharField(max_length=2, choices=KELAMIN, blank=True, null=True)
    tempat_lahir = models.CharField(max_length=30, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    nomor_handphone = models.CharField(max_length=15, blank=True, null=True)
    agama = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    sosmed = models.CharField(max_length=255, blank=True, null=True)
    pendidikan_akhir = models.EmailField(max_length=255, blank=True, null=True)
    kota = models.CharField(max_length=255, choices=KOTA, blank=True, null=True)
    alamat = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Form Trainer"
        verbose_name_plural = "Data Trainer"

    def __str__(self):
        return self.nama_trainer


class Pendaftaran(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.SET_NULL, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, blank=True, null=True)
    keterangan = models.TextField(max_length=255, blank=True, null=True)


class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=255, blank=True, null=True)
    peserta = models.ForeignKey(Peserta, on_delete=models.SET_NULL, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, blank=True, null=True)
    keterangan = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nama_kelas