from django.db import models

from django.utils.translation import gettext_lazy as _


class HomePage(models.Model):
    """ home page and image and description of home page"""
    title= models.CharField(max_length=255, verbose_name=_("عنوان فیلم"))
    image = models.ImageField(_("تصویر header"), upload_to='homepageheader/')
    description = models.TextField(verbose_name=_("عنوان فیلم"))
    
    #banner 1
    banner_title= models.CharField(max_length=255, verbose_name=_("عنوان بنر"), blank=True, null=True)
    banner_image = models.ImageField(_("تصویر header"), upload_to='banner/', blank=True, null=True)
    banner_course = models.ForeignKey("course", verbose_name=_(" دوره دو"), related_name="banner_1", on_delete=models.CASCADE, blank=True, null=True)
    
    #banner 2
    banner2_title= models.CharField(max_length=255, verbose_name=_("عنوان بنر"), blank=True, null=True)
    banner2_image = models.ImageField(_("تصویر header"), upload_to='banner/', blank=True, null=True)
    banner2_course = models.ForeignKey("course", verbose_name=_("دوره یک "),related_name="banner_2", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name =("خانه")
        verbose_name_plural =("خانه")
        
    def __str__(self):
        return self.title
    