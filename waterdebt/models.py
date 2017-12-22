from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    briefContent = models.CharField(max_length=255, default='Some content')
    content = models.TextField()
    image = models.CharField(max_length=255, default='static/img/dj.jpg')
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + ' - ' + self.briefContent

    def __unicode__(self):
        return u'{}'.format(self.title)
