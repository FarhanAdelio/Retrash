from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class StatistikView(LoginRequiredMixin, TemplateView):
    template_name = 'statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dummy data untuk contoh
        context.update({
            'total_waste': 1250,
            'recycled_waste': 875,
            'total_points': 2500,
            'co2_reduction': 625,
            'dates': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
            'weights': [120, 150, 180, 200, 170, 190],
            'waste_types': ['Plastik', 'Kertas', 'Logam', 'Kaca', 'Organik'],
            'waste_amounts': [300, 250, 200, 150, 350],
            'collection_history': [
                {
                    'date': '2024-03-15',
                    'waste_type': 'Plastik',
                    'weight': 5.5,
                    'points': 110,
                    'location': 'Bank Sampah Bersih'
                },
                {
                    'date': '2024-03-14',
                    'waste_type': 'Kertas',
                    'weight': 3.2,
                    'points': 64,
                    'location': 'Bank Sampah Hijau'
                },
                {
                    'date': '2024-03-13',
                    'waste_type': 'Logam',
                    'weight': 2.8,
                    'points': 84,
                    'location': 'Bank Sampah Sehat'
                }
            ]
        })
        
        return context 