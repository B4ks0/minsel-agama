from django.db import models


class Kecamatan(models.Model):
    nama = models.CharField(max_length=100)
    kabupaten = models.CharField(max_length=100, default='Minahasa Selatan')
    provinsi = models.CharField(max_length=100, default='Sulawesi Utara')

    class Meta:
        managed = False
        db_table = 'kecamatan'

    def __str__(self):
        return self.nama


class Gereja(models.Model):
    STATUS_CHOICES = [
        ('Permanen', 'Permanen'),
        ('Semi Permanen', 'Semi Permanen'),
        ('Darurat', 'Darurat'),
        ('Sewa/Kontrak', 'Sewa/Kontrak'),
    ]

    kecamatan = models.CharField(max_length=100)
    nama_gereja = models.CharField(max_length=200)
    kelurahan_desa = models.CharField(max_length=150, blank=True, null=True)
    jumlah_umat_l = models.IntegerField(default=0, blank=True, null=True)
    jumlah_umat_p = models.IntegerField(default=0, blank=True, null=True)
    jumlah_umat = models.IntegerField(default=0, blank=True, null=True)
    nama_pimpinan = models.CharField(max_length=200, blank=True, null=True)
    status_bangunan = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Permanen', blank=True, null=True)
    jumlah_pdt = models.IntegerField(default=0, blank=True, null=True)
    jumlah_pdm = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gereja'

    def __str__(self):
        return self.nama_gereja


class MasjidBkm(models.Model):
    no_urut = models.IntegerField(blank=True, null=True)
    wilayah_kua = models.CharField(max_length=100, blank=True, null=True)
    desa = models.CharField(max_length=150, blank=True, null=True)
    nama_masjid = models.CharField(max_length=200, blank=True, null=True)
    ada_musholla = models.BooleanField(default=False, blank=True, null=True)
    nama_imam = models.CharField(max_length=200, blank=True, null=True)
    ketua_btm = models.CharField(max_length=200, blank=True, null=True)
    keterangan = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'masjid_bkm'

    def __str__(self):
        return self.nama_masjid or ''


class RekapGerejaPerKecamatan(models.Model):
    kecamatan = models.CharField(max_length=100, primary_key=True)
    jumlah_gereja = models.IntegerField()
    total_umat_laki = models.IntegerField()
    total_umat_perempuan = models.IntegerField()
    total_umat = models.IntegerField()
    total_pendeta = models.IntegerField()
    total_pdm = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'v_rekap_gereja_per_kecamatan'


class RekapMasjidPerKua(models.Model):
    wilayah_kua = models.CharField(max_length=100, primary_key=True)
    jumlah_masjid = models.IntegerField()
    jumlah_musholla = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'v_rekap_masjid_per_kua'
