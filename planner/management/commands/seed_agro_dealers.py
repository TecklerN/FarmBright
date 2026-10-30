from django.core.management.base import BaseCommand
from planner.models import AgroDealer


class Command(BaseCommand):
    help = "Populate FarmBright with Zimbabwe agro-dealers"

    def handle(self, *args, **kwargs):

        dealers = [

            # =========================
            # HARARE
            # =========================

            {
                "name": "Farm & City Centre",
                "latitude": -17.8292,
                "longitude": 31.0522,
                "city": "Harare",
                "province": "Harare Metropolitan",
                "address": "1 Wynne Street corner South Avenue, Harare",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment, livestock supplies",
            },

            {
                "name": "Prime Agro Zimbabwe",
                "latitude": -17.8216,
                "longitude": 31.0535,
                "city": "Harare",
                "province": "Harare Metropolitan",
                "address": "5 Bodle Avenue, Harare",
                "dealer_type": "Agro-input Supplier",
                "products": "Seeds, fertilizers, agrochemicals, crop protection products",
            },

            {
                "name": "Profarmer Factory Shop",
                "latitude": -17.8445,
                "longitude": 31.0385,
                "city": "Harare",
                "province": "Harare Metropolitan",
                "address": "82 Woolwich Road, Harare",
                "dealer_type": "Agricultural Supplier",
                "products": "Seed, fertilizer, stock feed, agricultural inputs",
            },

            {
                "name": "ProFeeds City",
                "latitude": -17.8298,
                "longitude": 31.0528,
                "city": "Harare",
                "province": "Harare Metropolitan",
                "address": "149 Robert Mugabe Road, Harare",
                "dealer_type": "Farm & Livestock Supplier",
                "products": "Stock feed, livestock products, farm inputs",
            },

            {
                "name": "Red Dane Agri Solutions",
                "latitude": -17.7660,
                "longitude": 30.9980,
                "city": "Harare",
                "province": "Harare Metropolitan",
                "address": "17.5 km Peg, Lomagundi Road, Harare",
                "dealer_type": "Agricultural Supplier",
                "products": "Agricultural inputs, farm supplies",
            },

            # =========================
            # MASVINGO
            # =========================

            {
                "name": "PROfarmer PROfeeds Masvingo",
                "latitude": -20.0725,
                "longitude": 30.8320,
                "city": "Masvingo",
                "province": "Masvingo",
                "address": "18 Bradburn Street, Masvingo",
                "dealer_type": "Agricultural & Livestock Supplier",
                "products": "Seeds, fertilizers, stock feed, livestock products",
            },

            {
                "name": "ETG Agri Inputs Masvingo",
                "latitude": -20.0745,
                "longitude": 30.8290,
                "city": "Masvingo",
                "province": "Masvingo",
                "address": "Shed 43, Masvingo Train Station",
                "dealer_type": "Agro-input Supplier",
                "products": "Seeds, fertilizers, crop inputs, agricultural supplies",
            },

            {
                "name": "National Tested Seeds Farmshop",
                "latitude": -20.0755,
                "longitude": 30.8270,
                "city": "Masvingo",
                "province": "Masvingo",
                "address": "Josiah Tongogara Road, Masvingo",
                "dealer_type": "Seed Supplier",
                "products": "Certified seed, crop seed, agricultural inputs",
            },

            # =========================
            # BULAWAYO
            # =========================

            {
                "name": "ETG Agri Inputs Bulawayo",
                "latitude": -20.1500,
                "longitude": 28.5800,
                "city": "Bulawayo",
                "province": "Bulawayo Metropolitan",
                "address": "28 Josiah Chinamano Road, Bulawayo",
                "dealer_type": "Agro-input Supplier",
                "products": "Seeds, fertilizers, crop inputs, agricultural supplies",
            },

            {
                "name": "PROfeeds PROfarmer Bulawayo",
                "latitude": -20.1580,
                "longitude": 28.5840,
                "city": "Bulawayo",
                "province": "Bulawayo Metropolitan",
                "address": "62 Herbert Chitepo Street, Bulawayo",
                "dealer_type": "Agricultural & Livestock Supplier",
                "products": "Stock feed, seeds, fertilizers, livestock products",
            },

            {
                "name": "Farm & City Centre Bulawayo",
                "latitude": -20.1540,
                "longitude": 28.5845,
                "city": "Bulawayo",
                "province": "Bulawayo Metropolitan",
                "address": "10th Avenue / Jason Moyo Avenue, Bulawayo",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, farm equipment, agricultural supplies",
            },

            {
                "name": "Farmeazy Farming Solutions",
                "latitude": -20.1800,
                "longitude": 28.5700,
                "city": "Bulawayo",
                "province": "Bulawayo Metropolitan",
                "address": "Unit 2, 15 Plumtree Road, Bulawayo",
                "dealer_type": "Agricultural Supplier",
                "products": "Farm inputs, agricultural supplies, farming solutions",
            },

            # =========================
            # GWERU
            # =========================

            {
                "name": "Farm & City Centre Gweru",
                "latitude": -19.4550,
                "longitude": 29.8170,
                "city": "Gweru",
                "province": "Midlands",
                "address": "Gweru",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # MUTARE
            # =========================

            {
                "name": "Farm & City Centre Mutare",
                "latitude": -18.9707,
                "longitude": 32.6709,
                "city": "Mutare",
                "province": "Manicaland",
                "address": "Mutare",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # CHINHOYI
            # =========================

            {
                "name": "Farm & City Centre Chinhoyi",
                "latitude": -17.3660,
                "longitude": 30.2000,
                "city": "Chinhoyi",
                "province": "Mashonaland West",
                "address": "Chinhoyi",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # BINDURA
            # =========================

            {
                "name": "Farm & City Centre Bindura",
                "latitude": -17.3019,
                "longitude": 31.3306,
                "city": "Bindura",
                "province": "Mashonaland Central",
                "address": "Bindura",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # CHIREDZI
            # =========================

            {
                "name": "Farm & City Centre Chiredzi",
                "latitude": -21.0500,
                "longitude": 31.6667,
                "city": "Chiredzi",
                "province": "Masvingo",
                "address": "Chiredzi",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # CHIPINGE
            # =========================

            {
                "name": "Farm & City Centre Chipinge",
                "latitude": -20.1883,
                "longitude": 32.6236,
                "city": "Chipinge",
                "province": "Manicaland",
                "address": "Chipinge",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },

            # =========================
            # GOKWE
            # =========================

            {
                "name": "Farm & City Centre Gokwe",
                "latitude": -18.2048,
                "longitude": 28.9349,
                "city": "Gokwe",
                "province": "Midlands",
                "address": "Gokwe",
                "dealer_type": "Agricultural & Hardware Supplier",
                "products": "Seeds, fertilizers, agricultural chemicals, farm equipment",
            },
        ]

        created = 0
        updated = 0

        for dealer in dealers:
            obj, was_created = AgroDealer.objects.update_or_create(
                name=dealer["name"],
                city=dealer["city"],
                defaults=dealer
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Agro-dealer database loaded successfully! "
                f"Created: {created}, Updated: {updated}"
            )
        )