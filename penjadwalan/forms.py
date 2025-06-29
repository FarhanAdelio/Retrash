from django import forms
from .models import CollectionSchedule, CollectionRecord, Schedule

class CollectionScheduleForm(forms.ModelForm):
    class Meta:
        model = CollectionSchedule
        fields = ['location', 'scheduled_date', 'assigned_collector', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class CollectionRecordForm(forms.ModelForm):
    class Meta:
        model = CollectionRecord
        fields = ['actual_collection_date', 'collected_weight', 'notes']
        widgets = {
            'actual_collection_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['tanggal', 'waktu', 'lokasi', 'jenis_sampah', 'berat_perkiraan', 'catatan']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'waktu': forms.TimeInput(attrs={'type': 'time'}),
            'catatan': forms.Textarea(attrs={'rows': 3}),
        } 