from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from jsonfield import JSONField

class Question(models.Model):
    OPTIONS= [
    ( 'op1' , "گزینه اول "),
    ( 'op2' , "گزینه دوم "),
    ( 'op3' , "گزینه سوم "),
    ( 'op4' , "گزینه چهارم "),
]
    position = models.FloatField(verbose_name=_("ترتیب سوالات "), default=1, blank=True, null=True)
    question = models.TextField(null=True, verbose_name=_("سوال"))
    op1 = models.CharField(max_length=200,null=True, verbose_name=_("گزینه اول"))
    op2 = models.CharField(max_length=200,null=True, verbose_name=_("گزینه دوم"))
    op3 = models.CharField(max_length=200,null=True, verbose_name=_("گزینه سوم"))
    op4 = models.CharField(max_length=200,null=True, verbose_name=_("گزینه چهارم"))
    ans = models.CharField(max_length=200,null=True, choices=OPTIONS,  verbose_name=_("پاسخ") )
    publish = models.BooleanField(_('آیا منتشر شود'), default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quiz = models.ForeignKey("article.quiz", verbose_name=("آزمون"),related_name="question", on_delete=models.CASCADE, )
    
    def __str__(self):
        return self.question
    class Meta:
        verbose_name =("سوال")
        verbose_name_plural = ("سوال ها ")


class Quiz(models.Model):
    
    position = models.FloatField(verbose_name=_("ترتیب آزمون "), default=1, blank=True, null=True)
    title= models.CharField(max_length=255, verbose_name=_("عنوان آزمون"), null=True, blank=True)
    course = models.ForeignKey("article.Course",
                               verbose_name=_("دوره"), on_delete=models.CASCADE,
                               related_name="quizes", blank=True, null=True)
    slug = models.SlugField(max_length=255) 
    type = models.CharField(_("نوع"), default="quiz", max_length=10, editable=False)
    publish = models.BooleanField(_('آیا منتشر شود'), default=True, null=False)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name =("آزمون")
        verbose_name_plural = ("آزمون ها ")
    
class QuizProfile(models.Model):
    quiz = models.ForeignKey("Quiz", verbose_name=("آزمون"), on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name=_("کاربر") , on_delete=models.CASCADE)
    corrects = models.PositiveIntegerField(_("درست ها"), default=0)
    incorrects = models.PositiveIntegerField(_("درست ها"), default=0)
    total_score = models.PositiveIntegerField(_('امتیاز کل'), default=0) # in percent
    is_done = models.BooleanField(_("آزمون انجام شده است؟"), default= False)
    choices = JSONField(_("گزینه های انتخاب شده توسط کاربر"), null=True, blank=True)#postgre sql needs sth different
    def __str__(self):
        return str(self.quiz)


# class MyTestClass(models.Model):
#     choices = JSONField(("گزینه های انتخاب شده توسط کاربر"), null=True, blank=True)
    
#     def __str__(self):
#         return str(self.choices)