from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from functools import wraps
from .models import Kecamatan, Gereja, MasjidBkm, RekapGerejaPerKecamatan, RekapMasjidPerKua
from .forms import KecamatanForm, GerejaForm, MasjidBkmForm
from .analytics import run_spk, run_spk_gereja


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_admin_user(request.user):
            messages.warning(request, 'Akun user hanya dapat melihat data. Fitur SPK dan CRUD khusus admin.')
            return redirect('gereja_list')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard' if request.user.is_staff else 'gereja_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if user.is_staff:
                return redirect(next_url or 'dashboard')
            return redirect('gereja_list')
        messages.error(request, 'Username atau password tidak sesuai.')

    return render(request, 'main/auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Anda berhasil logout.')
    return redirect('login')


@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('gereja_list')
    total_gereja = Gereja.objects.count()
    total_masjid = MasjidBkm.objects.count()
    total_kecamatan = Kecamatan.objects.count()
    rekap_gereja = RekapGerejaPerKecamatan.objects.all().order_by('kecamatan')
    rekap_masjid = RekapMasjidPerKua.objects.all().order_by('wilayah_kua')
    return render(request, 'main/dashboard.html', {
        'total_gereja': total_gereja,
        'total_masjid': total_masjid,
        'total_kecamatan': total_kecamatan,
        'rekap_gereja': rekap_gereja,
        'rekap_masjid': rekap_masjid,
    })


@admin_required
def spk_prioritas(request):
    try:
        eps = float(request.GET.get('eps', 0.45))
    except ValueError:
        eps = 0.45
    try:
        min_samples = int(request.GET.get('min_samples', 4))
    except ValueError:
        min_samples = 4

    eps = min(max(eps, 0.10), 2.00)
    min_samples = min(max(min_samples, 2), 20)

    context = run_spk(
        Gereja.objects.all().order_by('kecamatan', 'nama_gereja'),
        MasjidBkm.objects.all().order_by('wilayah_kua', 'nama_masjid'),
        eps=eps,
        min_samples=min_samples,
    )
    return render(request, 'main/spk_prioritas.html', context)


@admin_required
def spk_gereja(request):
    try:
        eps = float(request.GET.get('eps', 0.45))
    except ValueError:
        eps = 0.45
    try:
        min_samples = int(request.GET.get('min_samples', 4))
    except ValueError:
        min_samples = 4

    eps = min(max(eps, 0.10), 2.00)
    min_samples = min(max(min_samples, 2), 20)

    context = run_spk_gereja(
        Gereja.objects.all().order_by('kecamatan', 'nama_gereja'),
        eps=eps,
        min_samples=min_samples,
    )
    return render(request, 'main/spk_gereja.html', context)


# --- Kecamatan ---

@login_required
def kecamatan_list(request):
    q = request.GET.get('q', '')
    qs = Kecamatan.objects.all().order_by('nama')
    if q:
        qs = qs.filter(nama__icontains=q)
    return render(request, 'main/kecamatan/list.html', {'kecamatan_list': qs, 'q': q})


@admin_required
def kecamatan_tambah(request):
    form = KecamatanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kecamatan berhasil ditambahkan.')
        return redirect('kecamatan_list')
    return render(request, 'main/kecamatan/form.html', {'form': form, 'judul': 'Tambah Kecamatan'})


@admin_required
def kecamatan_edit(request, pk):
    obj = get_object_or_404(Kecamatan, pk=pk)
    form = KecamatanForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kecamatan berhasil diperbarui.')
        return redirect('kecamatan_list')
    return render(request, 'main/kecamatan/form.html', {'form': form, 'judul': 'Edit Kecamatan', 'obj': obj})


@admin_required
def kecamatan_hapus(request, pk):
    obj = get_object_or_404(Kecamatan, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Kecamatan berhasil dihapus.')
        return redirect('kecamatan_list')
    return render(request, 'main/kecamatan/confirm_delete.html', {'obj': obj, 'nama': obj.nama})


# --- Gereja ---

@login_required
def gereja_list(request):
    q = request.GET.get('q', '')
    kec = request.GET.get('kec', '')
    qs = Gereja.objects.all().order_by('kecamatan', 'nama_gereja')
    if q:
        qs = qs.filter(Q(nama_gereja__icontains=q) | Q(kelurahan_desa__icontains=q) | Q(nama_pimpinan__icontains=q))
    if kec:
        qs = qs.filter(kecamatan__icontains=kec)
    kecamatan_list = Gereja.objects.values_list('kecamatan', flat=True).distinct().order_by('kecamatan')
    return render(request, 'main/gereja/list.html', {
        'gereja_list': qs,
        'q': q,
        'kec': kec,
        'kecamatan_list': kecamatan_list,
    })


@admin_required
def gereja_tambah(request):
    form = GerejaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data gereja berhasil ditambahkan.')
        return redirect('gereja_list')
    return render(request, 'main/gereja/form.html', {'form': form, 'judul': 'Tambah Gereja'})


@admin_required
def gereja_edit(request, pk):
    obj = get_object_or_404(Gereja, pk=pk)
    form = GerejaForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data gereja berhasil diperbarui.')
        return redirect('gereja_list')
    return render(request, 'main/gereja/form.html', {'form': form, 'judul': 'Edit Gereja', 'obj': obj})


@admin_required
def gereja_hapus(request, pk):
    obj = get_object_or_404(Gereja, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Data gereja berhasil dihapus.')
        return redirect('gereja_list')
    return render(request, 'main/gereja/confirm_delete.html', {'obj': obj, 'nama': obj.nama_gereja})


# --- Masjid BKM ---

@login_required
def masjid_list(request):
    q = request.GET.get('q', '')
    kua = request.GET.get('kua', '')
    qs = MasjidBkm.objects.all().order_by('no_urut')
    if q:
        qs = qs.filter(Q(nama_masjid__icontains=q) | Q(desa__icontains=q) | Q(nama_imam__icontains=q))
    if kua:
        qs = qs.filter(wilayah_kua__icontains=kua)
    kua_list = MasjidBkm.objects.values_list('wilayah_kua', flat=True).distinct().order_by('wilayah_kua')
    return render(request, 'main/masjid/list.html', {
        'masjid_list': qs,
        'q': q,
        'kua': kua,
        'kua_list': kua_list,
    })


@admin_required
def masjid_tambah(request):
    form = MasjidBkmForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data masjid berhasil ditambahkan.')
        return redirect('masjid_list')
    return render(request, 'main/masjid/form.html', {'form': form, 'judul': 'Tambah Masjid/BKM'})


@admin_required
def masjid_edit(request, pk):
    obj = get_object_or_404(MasjidBkm, pk=pk)
    form = MasjidBkmForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data masjid berhasil diperbarui.')
        return redirect('masjid_list')
    return render(request, 'main/masjid/form.html', {'form': form, 'judul': 'Edit Masjid/BKM', 'obj': obj})


@admin_required
def masjid_hapus(request, pk):
    obj = get_object_or_404(MasjidBkm, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Data masjid berhasil dihapus.')
        return redirect('masjid_list')
    return render(request, 'main/masjid/confirm_delete.html', {'obj': obj, 'nama': obj.nama_masjid})
