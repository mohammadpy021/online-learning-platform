from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField 
from .models.managers import CourseManager


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
VIDEO_VALIDATOR = [FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])]
class Course(models.Model):
    C =  "completed"
    I = "inprogress"
    STATUS = [
    (C , "تکمیل شده"),
    (I , "درحال تکمیل"),
]
    title = models.CharField(_("عنوان دوره"), max_length=250)
    description = models.TextField(verbose_name = "توضیحات", blank=True, null=True)

    publish_status = models.CharField(_("وضعیت انتشار دوره"),choices=STATUS, max_length=15, default=I)
    is_active = models.BooleanField(_("دوره منتشر شود"))
    author = models.ForeignKey(get_user_model(),verbose_name=_("مدرس"), on_delete=models.CASCADE, related_name="articles")
    is_free = models.BooleanField(_("دوره رایگان است"), default=False)
    price = models.PositiveIntegerField(_("هزینه دوره"),help_text="به تومان", blank=True, null=True)
    #TODO:discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR, blank=True, null=True)  
    image = models.ImageField(_("تصویر"), upload_to='thumbnails/') # 400 * 225
    # video = models.FileField(upload_to='videos_uploaded/',blank=True, validators= VIDEO_VALIDATOR)
    slug  =  models.SlugField(_("نامک"), unique=True,  help_text = "slug")
    prerequisite = models.TextField(_("پیش نیاز های دوره"), blank=True, null=True)

    
    time_of_course = models.DurationField(_("مدت زمان دوره"), help_text = "HH:MM")
    category = models.ManyToManyField("Category",  verbose_name=_("دسته بندی"), related_name="articles")
    SuggestedCourses = models.ManyToManyField("self", blank=True, verbose_name=_("دوره پیشنهادی"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(blank=True, default=timezone.now ) 
    #TODO: comments
       
    objects = CourseManager()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'دوره '
        verbose_name_plural = 'دوره ها'

@receiver(post_delete, sender=Course)
def delete_associated_files(sender, instance, **kwargs):
    """Remove all files of an article after deletion."""
    try:
        image_path = instance.image.name
        video_path = instance.videos.name
        if image_path:
            default_storage.delete(image_path)
        if video_path:
            default_storage.delete(video_path)
    except:
        pass

class Category(models.Model):
    title= models.CharField(max_length=255)
    position = models.IntegerField(verbose_name=_("پوزیشن"), default=1)
    slug = models.SlugField(max_length=255, unique=True) 
    status = models.BooleanField(default=False, verbose_name=_("وضعیت انتشار"))

    class Meta:
        verbose_name =("دسته‌بندی")
        verbose_name_plural = ("دسته‌بندی ها ")
        ordering = ["position"]
    def __str__(self):
        return self.title


def video_path(instance, filename):
    return f'videos/{instance.course.slug}/{filename})'
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
    course = models.ForeignKey(Course,verbose_name=_("دوره"), on_delete=models.CASCADE, related_name="videos")
    videofile= models.FileField(upload_to=video_path, null=True, verbose_name="ویدیو")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse ("deploy:detail", kwargs={"slug":self.slug})

    class Meta:
        verbose_name =("ویدیو")
        verbose_name_plural = ("ویدیو ها ")
    def __str__(self):
        return self.title

#TODO:
# class SuggestedCourses(models.Model):
#     ''' suggested courses in the bottom of the page'''
    

# class Question(models.Model):
#     question = models.CharField(max_length=200,null=True)
#     op1 = models.CharField(max_length=200,null=True)
#     op2 = models.CharField(max_length=200,null=True)
#     op3 = models.CharField(max_length=200,null=True)
#     op4 = models.CharField(max_length=200,null=True)
#     ans = models.CharField(max_length=200,null=True)
    
#     def __str__(self):
#         return self.question
    


    