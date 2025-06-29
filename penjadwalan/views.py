from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CollectionSchedule, CollectionRecord, Schedule
from .forms import CollectionScheduleForm, CollectionRecordForm, ScheduleForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class ScheduleListView(LoginRequiredMixin, ListView):
    model = CollectionSchedule
    template_name = 'penjadwalan/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 10

    def get_queryset(self):
        return CollectionSchedule.objects.all().order_by('-scheduled_date')

class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = CollectionSchedule
    template_name = 'penjadwalan/schedule_detail.html'
    context_object_name = 'schedule'

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = CollectionSchedule
    form_class = CollectionScheduleForm
    template_name = 'penjadwalan/schedule_form.html'
    success_url = reverse_lazy('penjadwalan:schedule_list')

    def form_valid(self, form):
        messages.success(self.request, 'Jadwal pengambilan berhasil dibuat.')
        return super().form_valid(form)

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = CollectionSchedule
    form_class = CollectionScheduleForm
    template_name = 'penjadwalan/schedule_form.html'
    success_url = reverse_lazy('penjadwalan:schedule_list')

    def form_valid(self, form):
        messages.success(self.request, 'Jadwal pengambilan berhasil diperbarui.')
        return super().form_valid(form)

class RecordCreateView(LoginRequiredMixin, CreateView):
    model = CollectionRecord
    form_class = CollectionRecordForm
    template_name = 'penjadwalan/record_form.html'

    def get_success_url(self):
        return reverse_lazy('penjadwalan:schedule_detail', kwargs={'pk': self.object.schedule.pk})

    def form_valid(self, form):
        form.instance.schedule = get_object_or_404(CollectionSchedule, pk=self.kwargs['schedule_pk'])
        messages.success(self.request, 'Catatan pengambilan berhasil dibuat.')
        return super().form_valid(form)

def schedule_list(request):
    schedules = Schedule.objects.all().order_by('tanggal', 'waktu')
    return render(request, 'penjadwalan/schedule_list.html', {
        'schedules': schedules
    })

@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            messages.success(request, 'Jadwal berhasil dibuat.')
            return redirect('penjadwalan:schedule')
    else:
        form = ScheduleForm()
    
    return render(request, 'penjadwalan/schedule_form.html', {
        'form': form,
        'title': 'Buat Jadwal Baru'
    })

@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jadwal berhasil diperbarui.')
            return redirect('penjadwalan:schedule')
    else:
        form = ScheduleForm(instance=schedule)
    
    return render(request, 'penjadwalan/schedule_form.html', {
        'form': form,
        'title': 'Edit Jadwal'
    })

@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    schedule.delete()
    messages.success(request, 'Jadwal berhasil dihapus.')
    return redirect('penjadwalan:schedule')
