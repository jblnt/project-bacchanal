from django.db import models

class Articles(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=256, null=False, default='none')
    slug = models.CharField(max_length=256, null=False, default='none')
    content = models.TextField(null=True)
    tag = models.CharField(max_length=128, null=True)
    source = models.CharField(max_length=128, null=False, default='none')
    date = models.DateField(null=True)
    images = models.TextField(null=False, default='none')

    class Meta:
        db_table = 'articles'
        #managed = False
        ordering = ['source']