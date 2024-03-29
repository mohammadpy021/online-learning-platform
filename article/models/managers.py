from django.db import models

class CourseManager(models.Manager):
    def publish_completed(self):
        return self.filter(publish_status='completed')
    def active(self):
        return self.filter(is_active=True)