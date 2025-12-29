"""
Service untuk mengolah data statistik dengan berbagai filter
"""
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth, TruncYear, TruncDate
from datetime import datetime, timedelta
from decimal import Decimal
from manajemen.models import Transaksi, JenisSampah, BankSampah


class StatistikService:
    """Service untuk analisis statistik sampah"""
    
    @staticmethod
    def get_filter_params(filter_type, year=None, month=None):
        """
        Generate filter parameter berdasarkan tipe filter
        
        Args:
            filter_type: 'all', 'yearly', 'monthly'
            year: Tahun untuk filter (int)
            month: Bulan untuk filter (int 1-12)
        
        Returns:
            dict dengan start_date dan end_date
        """
        now = datetime.now()
        
        if filter_type == 'monthly' and year and month:
            # Filter per bulan tertentu
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        elif filter_type == 'yearly' and year:
            # Filter per tahun tertentu
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)
        
        else:
            # Filter all time (1 tahun terakhir sebagai default)
            start_date = now - timedelta(days=365)
            end_date = now
        
        return {
            'start_date': start_date,
            'end_date': end_date
        }
    
    @staticmethod
    def get_summary_stats(start_date=None, end_date=None, user=None):
        """
        Ambil ringkasan statistik utama
        
        Returns:
            dict dengan total_sampah, total_transaksi, total_pendapatan, dll
        """
        queryset = Transaksi.objects.filter(status='selesai')
        
        if user:
            queryset = queryset.filter(user=user)
        
        if start_date and end_date:
            queryset = queryset.filter(
                tanggal_transaksi__gte=start_date,
                tanggal_transaksi__lte=end_date
            )
        
        stats = queryset.aggregate(
            total_berat=Sum('berat'),
            total_transaksi=Count('id'),
            total_pendapatan=Sum('total_harga'),
            rata_berat=Avg('berat')
        )
        
        # Hitung CO2 reduction (asumsi: 1kg sampah = 0.5kg CO2 berkurang)
        co2_reduction = (stats['total_berat'] or Decimal('0')) * Decimal('0.5')
        
        # Hitung poin (asumsi: 1kg = 20 poin)
        total_points = (stats['total_berat'] or Decimal('0')) * 20
        
        return {
            'total_sampah': round(stats['total_berat'] or Decimal('0'), 2),
            'total_transaksi': stats['total_transaksi'] or 0,
            'total_pendapatan': round(stats['total_pendapatan'] or Decimal('0'), 2),
            'rata_berat': round(stats['rata_berat'] or Decimal('0'), 2),
            'co2_reduction': round(co2_reduction, 2),
            'total_points': int(total_points),
        }
    
    @staticmethod
    def get_trend_data(start_date, end_date, group_by='month', user=None):
        """
        Ambil data trend pengumpulan sampah
        
        Args:
            group_by: 'month', 'day', 'year'
        
        Returns:
            list of dict dengan periode dan total_berat
        """
        queryset = Transaksi.objects.filter(
            status='selesai',
            tanggal_transaksi__gte=start_date,
            tanggal_transaksi__lte=end_date
        )
        
        if user:
            queryset = queryset.filter(user=user)
        
        if group_by == 'month':
            trend = queryset.annotate(
                periode=TruncMonth('tanggal_transaksi')
            ).values('periode').annotate(
                total_berat=Sum('berat'),
                jumlah_transaksi=Count('id')
            ).order_by('periode')
            
        elif group_by == 'day':
            trend = queryset.annotate(
                periode=TruncDate('tanggal_transaksi')
            ).values('periode').annotate(
                total_berat=Sum('berat'),
                jumlah_transaksi=Count('id')
            ).order_by('periode')
            
        else:  # year
            trend = queryset.annotate(
                periode=TruncYear('tanggal_transaksi')
            ).values('periode').annotate(
                total_berat=Sum('berat'),
                jumlah_transaksi=Count('id')
            ).order_by('periode')
        
        return list(trend)
    
    @staticmethod
    def get_waste_type_distribution(start_date, end_date, user=None):
        """
        Ambil distribusi jenis sampah
        
        Returns:
            list of dict dengan jenis_sampah dan total_berat
        """
        queryset = Transaksi.objects.filter(
            status='selesai',
            tanggal_transaksi__gte=start_date,
            tanggal_transaksi__lte=end_date
        )
        
        if user:
            queryset = queryset.filter(user=user)
        
        distribution = queryset.values(
            'jenis_sampah__nama'
        ).annotate(
            total_berat=Sum('berat'),
            jumlah_transaksi=Count('id')
        ).order_by('-total_berat')
        
        return list(distribution)
    
    @staticmethod
    def get_bank_sampah_ranking(start_date, end_date, limit=10):
        """
        Ambil ranking bank sampah berdasarkan total transaksi
        
        Returns:
            list of dict dengan bank_sampah dan total_berat
        """
        ranking = Transaksi.objects.filter(
            status='selesai',
            tanggal_transaksi__gte=start_date,
            tanggal_transaksi__lte=end_date
        ).values(
            'bank_sampah__nama',
            'bank_sampah__id'
        ).annotate(
            total_berat=Sum('berat'),
            jumlah_transaksi=Count('id'),
            total_pendapatan=Sum('total_harga')
        ).order_by('-total_berat')[:limit]
        
        return list(ranking)
    
    @staticmethod
    def get_recent_transactions(limit=10, user=None):
        """
        Ambil transaksi terbaru
        
        Returns:
            QuerySet Transaksi
        """
        queryset = Transaksi.objects.select_related(
            'user', 'bank_sampah', 'jenis_sampah'
        ).order_by('-tanggal_transaksi')
        
        if user:
            queryset = queryset.filter(user=user)
        
        return queryset[:limit]
    
    @staticmethod
    def get_available_years():
        """
        Ambil daftar tahun yang tersedia di database
        
        Returns:
            list of years (int)
        """
        years = Transaksi.objects.dates('tanggal_transaksi', 'year', order='DESC')
        return [year.year for year in years]
    
    @staticmethod
    def get_monthly_comparison(year):
        """
        Perbandingan data per bulan dalam 1 tahun
        
        Returns:
            dict dengan data per bulan
        """
        months = []
        for month in range(1, 13):
            filter_params = StatistikService.get_filter_params('monthly', year, month)
            stats = StatistikService.get_summary_stats(
                filter_params['start_date'],
                filter_params['end_date']
            )
            months.append({
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'stats': stats
            })
        
        return months
