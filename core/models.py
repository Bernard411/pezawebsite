from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils import timezone
from bs4 import BeautifulSoup
import re


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(help_text="Use HTML or Markdown for content, including <img> tags for inline images using their URLs.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = TaggableManager(blank=True)
    read_time = models.PositiveIntegerField(help_text="Estimated read time in minutes")
    is_tutorial = models.BooleanField(default=False, help_text="Check if this is a tutorial article")
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, help_text="Check to feature on homepage")

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def banner_image(self):
        """Get banner image from ArticleImage model"""
        banner = self.images.filter(is_banner=True).first()
        return banner.image_url if banner else None
    
    # NEW METHODS FOR IMAGE EXTRACTION
    
    def get_content_images(self):
        """
        Extract all image URLs from the article content
        Returns a list of image URLs
        """
        if not self.content:
            return []
        
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            img_tags = soup.find_all('img')
            return [img.get('src') for img in img_tags if img.get('src')]
        except:
            # Fallback to regex if BeautifulSoup fails
            return self.get_images_regex()
    
    def get_images_regex(self):
        """
        Extract image URLs using regex (fallback method)
        Returns a list of image URLs
        """
        if not self.content:
            return []
        
        pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        matches = re.findall(pattern, self.content, re.IGNORECASE)
        return matches
    
    def get_first_content_image(self):
        """
        Get the first image from article content
        Returns the first image URL or None
        """
        images = self.get_content_images()
        return images[0] if images else None
    
    @property
    def featured_image(self):
        """
        Get the featured image - prioritizes banner, falls back to first content image
        This is the main method to use for displaying article images
        """
        # First check for banner image from ArticleImage model
        if self.banner_image:
            return self.banner_image
        
        # Fall back to first content image
        first_img = self.get_first_content_image()
        return first_img if first_img else None
    
    def has_images(self):
        """
        Check if article has any images (banner or content)
        Returns True/False
        """
        return bool(self.banner_image or self.get_first_content_image())
    
    def count_content_images(self):
        """
        Count the number of images in content
        Returns integer count
        """
        return len(self.get_content_images())
    
    def get_images_with_metadata(self):
        """
        Get images with their alt text and other attributes
        Returns a list of dictionaries with image metadata
        """
        if not self.content:
            return []
        
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            img_tags = soup.find_all('img')
            
            images = []
            for img in img_tags:
                image_data = {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                }
                images.append(image_data)
            
            return images
        except:
            return []
    
    def get_all_images(self):
        """
        Get all images from both banner and content (unique only)
        Returns a list of unique image URLs
        """
        images = []
        
        # Add banner image if exists
        if self.banner_image:
            images.append(self.banner_image)
        
        # Add content images
        content_images = self.get_content_images()
        images.extend(content_images)
        
        # Return unique images only
        return list(set(images))
    
    def get_excerpt(self, length=150):
        """
        Get a plain text excerpt without HTML tags
        Useful for meta descriptions and previews
        """
        if not self.content:
            return ''
        
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            text = soup.get_text()
            # Clean up whitespace
            text = ' '.join(text.split())
            # Truncate to length
            if len(text) > length:
                return text[:length].rsplit(' ', 1)[0] + '...'
            return text
        except:
            return self.content[:length] + '...' if len(self.content) > length else self.content


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_banner = models.BooleanField(default=False, help_text="Check if this is the banner image; others can be referenced in the article content via their URLs.")

    class Meta:
        ordering = ['-is_banner']

    def __str__(self):
        return f"Image for {self.article.title} (Banner: {self.is_banner})"


class Tool(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tools')
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='resources')
    file_url = models.URLField(blank=True, null=True, help_text="URL to the external file.")
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name