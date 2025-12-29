"""
Management command untuk generate data dummy statistik
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from manajemen.models import BankSampah, JenisSampah, Transaksi
from datetime import datetime, timedelta
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate data dummy untuk testing statistik'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus data lama sebelum generate',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Menghapus data lama...')
            Transaksi.objects.all().delete()
            BankSampah.objects.all().delete()
            JenisSampah.objects.all().delete()

        # Buat Jenis Sampah
        self.stdout.write('Membuat jenis sampah...')
        jenis_sampah_data = [
            {'nama': 'Plastik', 'deskripsi': 'Sampah plastik', 'harga_per_kg': Decimal('2000')},
            {'nama': 'Kertas', 'deskripsi': 'Sampah kertas', 'harga_per_kg': Decimal('1500')},
            {'nama': 'Logam', 'deskripsi': 'Sampah logam', 'harga_per_kg': Decimal('5000')},
            {'nama': 'Kaca', 'deskripsi': 'Sampah kaca', 'harga_per_kg': Decimal('1000')},
            {'nama': 'Organik', 'deskripsi': 'Sampah organik', 'harga_per_kg': Decimal('500')},
        ]
        
        jenis_sampah_list = []
        for data in jenis_sampah_data:
            jenis, created = JenisSampah.objects.get_or_create(
                nama=data['nama'],
                defaults={
                    'deskripsi': data['deskripsi'],
                    'harga_per_kg': data['harga_per_kg']
                }
            )
            jenis_sampah_list.append(jenis)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {jenis.nama}'))

        # Buat Bank Sampah
        self.stdout.write('\nMembuat bank sampah...')
        bank_sampah_data = [
            {
                'nama': 'Bank Sampah Bersih',
                'alamat': 'Jl. Mawar No. 123',
                'telepon': '08123456789',
                'email': 'bersih@banksampah.id',
                'jam_operasional': 'Senin-Jumat 08:00-16:00',
                'deskripsi': 'Bank sampah terpercaya',
                'latitude': -6.2088,
                'longitude': 106.8456,
            },
            {
                'nama': 'Bank Sampah Hijau',
                'alamat': 'Jl. Melati No. 456',
                'telepon': '08198765432',
                'email': 'hijau@banksampah.id',
                'jam_operasional': 'Senin-Sabtu 09:00-17:00',
                'deskripsi': 'Peduli lingkungan',
                'latitude': -6.2146,
                'longitude': 106.8451,
            },
            {
                'nama': 'Bank Sampah Sehat',
                'alamat': 'Jl. Kenanga No. 789',
                'telepon': '08112345678',
                'email': 'sehat@banksampah.id',
                'jam_operasional': 'Setiap hari 08:00-18:00',
                'deskripsi': 'Untuk masa depan lebih baik',
                'latitude': -6.2195,
                'longitude': 106.8467,
            },
        ]
        
        bank_sampah_list = []
        for data in bank_sampah_data:
            bank, created = BankSampah.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                # Tambahkan semua jenis sampah
                bank.jenis_sampah.set(jenis_sampah_list)
            bank_sampah_list.append(bank)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {bank.nama}'))

        # Get atau buat user
        self.stdout.write('\nMencari user...')
        users = list(User.objects.all()[:5])
        if not users:
            self.stdout.write(self.style.WARNING('  ! Tidak ada user, skip generate transaksi'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Ditemukan {len(users)} user'))

        # Generate Transaksi untuk 1 tahun terakhir
        self.stdout.write('\nGenerate transaksi...')
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        total_generated = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Random 1-5 transaksi per hari
            transaksi_per_hari = random.randint(0, 5)
            
            for _ in range(transaksi_per_hari):
                user = random.choice(users)
                bank = random.choice(bank_sampah_list)
                jenis = random.choice(jenis_sampah_list)
                berat = Decimal(str(round(random.uniform(1.0, 20.0), 2)))
                total_harga = berat * jenis.harga_per_kg
                
                # Random waktu dalam hari tersebut
                random_hour = random.randint(8, 17)
                random_minute = random.randint(0, 59)
                tanggal_transaksi = current_date.replace(
                    hour=random_hour,
                    minute=random_minute
                )
                
                transaksi = Transaksi.objects.create(
                    user=user,
                    bank_sampah=bank,
                    jenis_sampah=jenis,
                    berat=berat,
                    total_harga=total_harga,
                    status='selesai',
                    tanggal_transaksi=tanggal_transaksi
                )
                total_generated += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Berhasil generate {total_generated} transaksi'))
        self.stdout.write(self.style.SUCCESS(f'✅ Periode: {start_date.strftime("%d %b %Y")} - {end_date.strftime("%d %b %Y")}'))
