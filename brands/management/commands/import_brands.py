from django.core.management.base import BaseCommand
from brands.models import Brand  # Substitua 'myapp' pelo nome do seu aplicativo
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa várias marcas de suplementos'

    def handle(self, *args, **kwargs):
        brands_data = [
            {'name': 'Optimum Nutrition', 'description': 'Uma das marcas líderes em suplementos nutricionais, conhecida por sua proteína de alta qualidade e outros produtos de fitness.'},
            {'name': 'Vital Proteins', 'description': 'Especializada em colágeno e suplementos de saúde e bem-estar.'},
            {'name': 'Dymatize', 'description': 'Marca famosa por suas proteínas, aminoácidos e outros produtos para melhorar o desempenho esportivo.'},
            {'name': 'BSN', 'description': 'Conhecida por seus suplementos energéticos e proteínas de rápida absorção.'},
            {'name': 'MuscleTech', 'description': 'Uma das marcas mais renomadas no mundo do fisiculturismo, oferecendo uma vasta gama de suplementos.'},
            {'name': 'Cellucor', 'description': 'Popular por seus produtos de pré-treino, proteínas e suplementos de aminoácidos.'},
            {'name': 'MyProtein', 'description': 'Marca britânica conhecida por oferecer uma ampla gama de suplementos de alta qualidade a preços acessíveis.'},
            {'name': 'GNC', 'description': 'Líder mundial em suplementos nutricionais e vitaminas, com uma vasta linha de produtos.'},
            {'name': 'MusclePharm', 'description': 'Famosa por seus suplementos voltados para desempenho atlético e bem-estar geral.'},
            {'name': 'R1 Protein', 'description': 'Marca que oferece proteína de alta qualidade com foco em ingredientes puros e eficazes.'},
            {'name': 'Herbalife', 'description': 'Conhecida por seus produtos de nutrição e controle de peso, incluindo shakes e suplementos.'},
            {'name': 'NOW Foods', 'description': 'Oferece uma vasta linha de suplementos nutricionais e produtos naturais.'},
            {'name': 'Kaged Muscle', 'description': 'Marca que oferece suplementos premium com foco em ingredientes naturais e qualidade superior.'},
            {'name': 'Jym Supplement Science', 'description': 'Marca criada por Jim Stoppani, conhecida por seus suplementos de alta performance.'},
            {'name': 'Garden of Life', 'description': 'Focada em suplementos orgânicos e naturais, incluindo vitaminas, proteínas e probióticos.'},
            {'name': 'Legion Athletics', 'description': 'Marca que oferece suplementos naturais, como proteínas, pré-treinos e aminoácidos.'},
            {'name': 'Animal Pak', 'description': 'Conhecida por suas fórmulas de suplementos para fisiculturistas, com ênfase em pacotes de multivitamínicos.'},
            {'name': 'BPI Sports', 'description': 'Famosa por seus pré-treinos, proteínas e suplementos voltados para a perda de peso.'},
            {'name': 'Redcon1', 'description': 'Marca popular por seus suplementos de desempenho, incluindo pré-treinos e proteínas.'},
            {'name': 'Evlution Nutrition', 'description': 'Oferece suplementos focados em melhorar o desempenho atlético e a recuperação.'},
            {'name': 'Cellucor C4', 'description': 'Uma linha de suplementos de pré-treino, incluindo o famoso C4, um dos mais vendidos no mercado.'},
            {'name': 'Nutrex Research', 'description': 'Conhecida pelos seus suplementos de termogênicos e produtos para melhorar a performance física.'},
            {'name': 'Primeval Labs', 'description': 'Marca especializada em suplementos de alta performance e fórmulas científicas.'},
            {'name': 'Beverly International', 'description': 'Focada em suplementos premium para fisiculturistas e entusiastas do fitness.'},
            {'name': 'SIS (Science in Sport)', 'description': 'Especializada em suplementos esportivos de alta performance, como géis energéticos e isotônicos.'},
            {'name': 'PEScience', 'description': 'Marca que oferece suplementos para emagrecimento, ganho muscular e pré-treinos.'},
            {'name': 'Quest Nutrition', 'description': 'Famosa por seus snacks de proteínas, barras de proteínas e suplementos para dietas específicas.'},
            {'name': 'Kirkland Signature', 'description': 'Marca da Costco, oferece uma variedade de suplementos nutricionais a preços competitivos.'},
            {'name': 'Bodybuilding.com Signature Series', 'description': 'Linha de suplementos oferecida pela famosa loja de suplementos Bodybuilding.com.'},
            {'name': 'Biosynergy', 'description': 'Marca especializada em suplementos para performance e saúde geral.'},
            {'name': 'MHP (Maximum Human Performance)', 'description': 'Oferece suplementos para atletas e fisiculturistas com foco em ganhos musculares e recuperação.'},
            {'name': 'USN (Ultimate Sports Nutrition)', 'description': 'Marca global de suplementos, com produtos focados no aumento de desempenho e ganho muscular.'},
            {'name': 'ANIMAL', 'description': 'Marca com uma linha de suplementos de desempenho atlético, especialmente focada em fisiculturismo.'},
            {'name': 'True Nutrition', 'description': 'Oferece suplementos personalizados para atender às necessidades nutricionais individuais.'},
            {'name': 'ProSupps', 'description': 'Marca focada em suplementos de alta performance, incluindo pré-treinos e proteínas.'},
            {'name': 'Swanson', 'description': 'Marca conhecida por seus suplementos naturais, vitaminas e produtos de saúde geral.'},
            {'name': 'Labrada', 'description': 'Oferece uma linha de suplementos voltada para a construção muscular e perda de gordura.'},
            {'name': 'BULK Natural', 'description': 'Focada em suplementos naturais e orgânicos para performance e saúde.'},
            {'name': 'Rogue Fitness', 'description': 'Além de equipamentos de ginástica, também oferece suplementos focados em performance esportiva.'},
            {'name': 'Probiotics.com', 'description': 'Marca especializada em suplementos probióticos e de saúde digestiva.'},
            {'name': 'Youtheory', 'description': 'Marca focada em suplementos para saúde da pele, articulações e bem-estar geral.'},
        ]

        # Criação das instâncias de Brand
        brands = [Brand(name=brand['name'], description=brand['description']) for brand in brands_data]

        # Inserção em massa
        Brand.objects.bulk_create(brands)

        self.stdout.write(self.style.SUCCESS('Marcas importadas com sucesso!'))
