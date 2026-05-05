from django import forms
from .models import Kecamatan, Gereja, MasjidBkm


class KecamatanForm(forms.ModelForm):
    class Meta:
        model = Kecamatan
        fields = ['nama', 'kabupaten', 'provinsi']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kecamatan'}),
            'kabupaten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kabupaten'}),
            'provinsi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Provinsi'}),
        }


class GerejaForm(forms.ModelForm):
    class Meta:
        model = Gereja
        fields = ['kecamatan', 'nama_gereja', 'kelurahan_desa', 'jumlah_umat_l', 'jumlah_umat_p',
                  'jumlah_umat', 'nama_pimpinan', 'status_bangunan', 'jumlah_pdt', 'jumlah_pdm']
        widgets = {
            'kecamatan': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_gereja': forms.TextInput(attrs={'class': 'form-control'}),
            'kelurahan_desa': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_umat_l': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'jumlah_umat_p': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'jumlah_umat': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nama_pimpinan': forms.TextInput(attrs={'class': 'form-control'}),
            'status_bangunan': forms.Select(attrs={'class': 'form-select'}),
            'jumlah_pdt': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'jumlah_pdm': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class MasjidBkmForm(forms.ModelForm):
    class Meta:
        model = MasjidBkm
        fields = ['no_urut', 'wilayah_kua', 'desa', 'nama_masjid', 'ada_musholla',
                  'nama_imam', 'ketua_btm', 'keterangan']
        widgets = {
            'no_urut': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'wilayah_kua': forms.TextInput(attrs={'class': 'form-control'}),
            'desa': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_masjid': forms.TextInput(attrs={'class': 'form-control'}),
            'ada_musholla': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nama_imam': forms.TextInput(attrs={'class': 'form-control'}),
            'ketua_btm': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
