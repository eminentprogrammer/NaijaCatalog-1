from apps.catalogue.models import Book
from django.contrib.sitemaps import Sitemap

class Sitemap(Sitemap):
    changefreq = "daily"  # Set the change frequency (daily, weekly, etc.)
    priority = 0.5  # Set the priority (0.0 to 1.0)

    def items(self):
        obj = Book.objects.all()
        return obj

    def title(self, obj):
        return obj.title  # Replace with the actual field in your model
