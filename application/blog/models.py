from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    image_preview = models.ImageField(upload_to='blog/image-preview/%Y/%m', null=True, blank=True)
    image = models.ImageField(upload_to='blog/image/%Y/%m', null=True, blank=True)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)
    popularity = models.PositiveIntegerField(_('Manage Popularity'), default=0, blank=False, null=False)

    objects = models.Manager()
    published = PublishedPostsManager()

    class Meta:
        ordering = ['popularity']

    def __str__(self):
        return self.title

    @property
    def admin_image_preview(self):
        if self.image_preview:
            return mark_safe('<img src="{url}" height="50px" />'.format(url=self.image_preview.url))
        return ""


@receiver(post_delete, sender=Post)
def post_delete_blog(sender, instance, *args, **kwargs):
    """When we delete Blog instance, delete old image files """
    try:
        instance.image.delete(save=False)
        instance.image_preview.delete(save=False)
    except:
        pass


def pre_save_image_field(sender, instance, image_field):
    try:
        old_img = getattr(instance.__class__.objects.get(id=instance.id), image_field).path
        try:
            new_img = getattr(instance, image_field).path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


@receiver(pre_save, sender=Post)
def pre_save_image_country(sender, instance, *args, **kwargs):
    """When update Country, delete old image file.Instance old image file will delete from os """
    pre_save_image_field(sender, instance, image_field='image')
    pre_save_image_field(sender, instance, image_field='image_preview')
