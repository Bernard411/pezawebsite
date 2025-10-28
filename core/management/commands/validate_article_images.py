from django.core.management.base import BaseCommand
from core.models import Article
import requests

class Command(BaseCommand):
    help = 'Validate all images in article content'

    def handle(self, *args, **options):
        articles = Article.objects.all()
        
        for article in articles:
            images = article.get_content_images()
            
            print(f"\nArticle: {article.title}")
            print(f"Total images: {len(images)}")
            
            for img_url in images:
                try:
                    response = requests.head(img_url, timeout=5)
                    if response.status_code == 200:
                        print(f"  ✓ {img_url}")
                    else:
                        print(f"  ✗ {img_url} (Status: {response.status_code})")
                except Exception as e:
                    print(f"  ✗ {img_url} (Error: {str(e)})")