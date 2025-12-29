from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from .services import StatistikService
import json


class StatistikView(LoginRequiredMixin, TemplateView):
    template_name = 'statistik/statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil parameter filter dari GET request
        filter_type = self.request.GET.get('filter', 'yearly')  # all, yearly, monthly
        year = self.request.GET.get('year', datetime.now().year)
        month = self.request.GET.get('month')
        
        try:
            year = int(year)
            month = int(month) if month else None
        except (ValueError, TypeError):
            year = datetime.now().year
            month = None
        
        # Tentukan apakah user biasa atau admin
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        user_filter = None if is_admin else self.request.user
        
        # Get filter parameters
        filter_params = StatistikService.get_filter_params(filter_type, year, month)
        
        # Ambil data statistik
        summary = StatistikService.get_summary_stats(
            filter_params['start_date'],
            filter_params['end_date'],
            user_filter
        )
        
        # Ambil data trend
        group_by = 'day' if filter_type == 'monthly' else 'month'
        trend_data = StatistikService.get_trend_data(
            filter_params['start_date'],
            filter_params['end_date'],
            group_by,
            user_filter
        )
        
        # Ambil distribusi jenis sampah
        waste_distribution = StatistikService.get_waste_type_distribution(
            filter_params['start_date'],
            filter_params['end_date'],
            user_filter
        )
        
        # Ambil ranking bank sampah (hanya untuk admin)
        bank_ranking = []
        if is_admin:
            bank_ranking = StatistikService.get_bank_sampah_ranking(
                filter_params['start_date'],
                filter_params['end_date']
            )
        
        # Ambil transaksi terbaru
        recent_transactions = StatistikService.get_recent_transactions(10, user_filter)
        
        # Ambil daftar tahun yang tersedia
        available_years = StatistikService.get_available_years()
        if not available_years:
            available_years = [datetime.now().year]
        
        # Format data untuk Chart.js
        trend_labels = []
        trend_values = []
        for item in trend_data:
            if filter_type == 'monthly':
                trend_labels.append(item['periode'].strftime('%d %b'))
            else:
                trend_labels.append(item['periode'].strftime('%b %Y'))
            trend_values.append(float(item['total_berat']))
        
        waste_labels = []
        waste_values = []
        waste_colors = [
            '#198754', '#0d6efd', '#ffc107', '#dc3545', '#20c997',
            '#6610f2', '#fd7e14', '#0dcaf0', '#6f42c1', '#d63384'
        ]
        for item in waste_distribution:
            waste_labels.append(item['jenis_sampah__nama'])
            waste_values.append(float(item['total_berat']))
        
        context.update({
            # Summary stats
            'total_sampah': summary['total_sampah'],
            'total_transaksi': summary['total_transaksi'],
            'total_pendapatan': summary['total_pendapatan'],
            'total_points': summary['total_points'],
            'co2_reduction': summary['co2_reduction'],
            'rata_berat': summary['rata_berat'],
            
            # Chart data (JSON string untuk JavaScript)
            'trend_labels': json.dumps(trend_labels),
            'trend_values': json.dumps(trend_values),
            'waste_labels': json.dumps(waste_labels),
            'waste_values': json.dumps(waste_values),
            'waste_colors': json.dumps(waste_colors[:len(waste_values)]),
            
            # Other data
            'recent_transactions': recent_transactions,
            'bank_ranking': bank_ranking,
            
            # Filter parameters
            'current_filter': filter_type,
            'current_year': year,
            'current_month': month,
            'available_years': available_years,
            'months': [
                {'value': i, 'name': datetime(2000, i, 1).strftime('%B')}
                for i in range(1, 13)
            ],
            
            # User info
            'is_admin': is_admin,
        })
        
        return context


class StatistikAPIView(View):
    """API endpoint untuk data statistik real-time"""
    
    def get(self, request):
        filter_type = request.GET.get('filter', 'yearly')
        year = int(request.GET.get('year', datetime.now().year))
        month = request.GET.get('month')
        month = int(month) if month else None
        
        is_admin = request.user.is_staff or request.user.is_superuser
        user_filter = None if is_admin else request.user
        
        filter_params = StatistikService.get_filter_params(filter_type, year, month)
        
        summary = StatistikService.get_summary_stats(
            filter_params['start_date'],
            filter_params['end_date'],
            user_filter
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_sampah': float(summary['total_sampah']),
                'total_transaksi': summary['total_transaksi'],
                'total_pendapatan': float(summary['total_pendapatan']),
                'total_points': summary['total_points'],
                'co2_reduction': float(summary['co2_reduction']),
            }
        }) 