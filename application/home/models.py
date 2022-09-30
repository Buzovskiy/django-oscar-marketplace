import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class HomeBanner(models.Model):
    image_left = models.FileField(upload_to='images/home-banners/')
    image_right = models.FileField(upload_to='images/home-banners/')
    description = models.TextField(blank=True, null=True)
    section_id_selector = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=False,
        help_text=_('Enter the id selector of banner section without # '
                    'or leave the field empty to create id automatically')
    )
    priority = models.PositiveIntegerField(
        verbose_name=_('Position control'),
        default=0,
        blank=False,
        null=False,
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.section_id_selector:
            num = HomeBanner.objects.all().count() + 1
            self.section_id_selector = f'homeBannerIdSelector{str(num)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.section_id_selector

    class Meta:
        ordering = ['priority']


@receiver(post_delete, sender=HomeBanner)
def post_delete_image_country(sender, instance, *args, **kwargs):
    """When we delete HomeBanner instance, delete old image file """
    try:
        instance.image_left.delete(save=False)
        instance.image_right.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=HomeBanner)
def pre_save_image_country(sender, instance, *args, **kwargs):
    """When update HomeBanner, delete old image file.Instance old image file will delete from os """
    try:
        old_image_left = instance.__class__.objects.get(pk=instance.pk).image_left.path
        try:
            new_image_left = instance.image_left.path
        except:
            new_image_left = None
        if new_image_left != old_image_left:
            if os.path.exists(old_image_left):
                os.remove(old_image_left)
    except:
        pass

    try:
        old_image_right = instance.__class__.objects.get(pk=instance.pk).image_right.path
        try:
            new_image_right = instance.image_right.path
        except:
            new_image_right = None
        if new_image_right != old_image_right:
            if os.path.exists(old_image_right):
                os.remove(old_image_right)
    except:
        pass
