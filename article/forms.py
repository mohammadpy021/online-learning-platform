from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django.utils.translation import gettext_lazy as _
from .models import Course, Videos


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #only date without time
        self.fields['publish_at'] = JalaliDateField(label=_('publish_at'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget # optional, to use default datepicker
        )
        # self.fields['author'].label_from_instance = lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
        # you can added a "class" to this field for use your datepicker!
        # self.fields['publish_at'].widget.attrs.update({'class': 'jalali_date-date'})

        # self.fields['publish_at'] = SplitJalaliDateTimeField(label=_('publish_at'), 
        #     widget=AdminSplitJalaliDateTime # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
        # )


        

