from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal

from Product.models import Category, Product


class Command(BaseCommand):
    help = "Seed initial categories and products for development/demo. Safe to run multiple times."

    def handle(self, *args, **options):
        # Create categories
        electronics, _ = Category.objects.get_or_create(
            slug="electronics",
            defaults={
                "title": "Electronics",
                "keywords": "electronics,gadgets",
                "description": "Electronics category",
                "status": "True",
            },
        )
        laptops, _ = Category.objects.get_or_create(
            slug="laptops",
            defaults={
                "title": "Laptops",
                "keywords": "laptops,notebooks",
                "description": "Laptops and notebooks",
                "status": "True",
                "parent": electronics,
            },
        )
        desktops, _ = Category.objects.get_or_create(
            slug="desktops",
            defaults={
                "title": "Desktops",
                "keywords": "desktops,pcs",
                "description": "Desktop PCs",
                "status": "True",
                "parent": electronics,
            },
        )

        def upsert_product(title, category, price, image, description):
            slug = slugify(title)
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "title": title,
                    "keywords": title.lower(),
                    "description": description[:255],
                    "image": image,
                    "price": Decimal(str(price)),
                    "amount": 20,
                    "minamount": 1,
                    "variant": "None",
                    "detail": f"<p>{description}</p>",
                    "status": "True",
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {title}"))
            else:
                # Ensure core fields are up to date if already existed
                changed = False
                if product.category_id != category.id:
                    product.category = category
                    changed = True
                if product.price != Decimal(str(price)):
                    product.price = Decimal(str(price))
                    changed = True
                if product.image.name != image:
                    product.image = image
                    changed = True
                if changed:
                    product.save(update_fields=["category", "price", "image"])  # minimal update
                    self.stdout.write(self.style.WARNING(f"Updated product: {title}"))
                else:
                    self.stdout.write(f"Unchanged product: {title}")

        upsert_product(
            title="HP 15" ,
            category=laptops,
            price=799.99,
            image="images/hp_laptop.jpg",
            description="HP 15-inch laptop with Intel processor and 8GB RAM.",
        )
        upsert_product(
            title="ASUS VivoBook",
            category=laptops,
            price=699.00,
            image="images/asus_laptop.jpg",
            description="ASUS VivoBook with sleek design, 256GB SSD, 8GB RAM.",
        )
        upsert_product(
            title="Desktop PC",
            category=desktops,
            price=599.50,
            image="images/desktop.jpg",
            description="Powerful desktop PC suitable for home and office.",
        )
        upsert_product(
            title="HP Desktop Tower",
            category=desktops,
            price=549.00,
            image="images/hp-dektop1.png",
            description="HP desktop tower with ample storage and reliable performance.",
        )
        upsert_product(
            title="Workstation Pro",
            category=desktops,
            price=899.00,
            image="images/desktop1.jfif",
            description="High-performance workstation for creators and professionals.",
        )
        upsert_product(
            title="UltraBook 14",
            category=laptops,
            price=999.00,
            image="images/hp_laptop.jpg",
            description="Thin and light 14-inch ultrabook with long battery life.",
        )

        self.stdout.write(self.style.SUCCESS("Seeding completed."))
