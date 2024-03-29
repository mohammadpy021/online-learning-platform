from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.core.validators import FileExtensionValidator




def video_path(instance, filename):
    return f'videos/{instance.course.slug}/{filename})'

VIDEO_VALIDATOR = [FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])]


class Videos(models.Model):
    
    def course_slug(self):
        return str(self.course.slug)

    # def video_path(self):
    #     return (str(self.course.slug))
        # return osjoin(str(self.category), filename)
    
    position = models.FloatField(verbose_name=_("ترتیب "), default=1, blank=True, null=True)
    episode = models.IntegerField(verbose_name=_("قسمت"), default=1, blank=True, null=True)
    season = models.IntegerField(verbose_name=_("فصل"), default=1, blank=True, null=True)
    title= models.CharField(max_length=255, verbose_name=_("عنوان فیلم"))
    Video_Description= models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=255) 
    publish = models.BooleanField(default=False, verbose_name=_(" انتشار")) 
    is_free = models.BooleanField(default=False, verbose_name=_(" رایگان"))
    course = models.ForeignKey("article.Course",verbose_name=_("دوره"), on_delete=models.CASCADE, related_name="videos")
    videofile= models.FileField(upload_to=video_path, null=True, verbose_name="ویدیو", validators=VIDEO_VALIDATOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse ("deploy:detail", kwargs={"slug":self.slug})

    class Meta:
        verbose_name =("ویدیو")
        verbose_name_plural = ("ویدیو ها ")
    def __str__(self):
        return self.title
    

