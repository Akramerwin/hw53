from django.db import models
from django.urls import reverse


# Create your models here.

class Projects(models.Model):
    s_date = models.DateField(verbose_name='s_date')
    e_date = models.DateField(verbose_name='e_date', blank=True, null=True)
    title = models.CharField(verbose_name='title', max_length=30)
    desc = models.TextField(verbose_name='desc', max_length=300)

    def __str__(self):
        return f'{self.title[:20]}, {self.desc[:20]}, {self.s_date}, {self.e_date}'

    def get_absolute_url(self):
        return reverse('view_p', kwargs={'pk': self.pk})

class Type(models.Model):
    type_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='type_name')
    def __str__(self):
        return f'{self.type_name}'

class Status(models.Model):
    status_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='status_name')
    def __str__(self):
        return f'{self.status_name}'

class Todo(models.Model):
    short_description = models.CharField(max_length=20, null=False, blank=False, verbose_name="short_description")
    description = models.TextField(max_length=150, null=True, blank=True, verbose_name="Description")
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, verbose_name="Status", related_name="status")
    type = models.ManyToManyField('webapp.Type', verbose_name='Type', related_name="type")
    date_of_create = models.DateTimeField(verbose_name="Date_of_Create", auto_now_add=True)
    date_of_update = models.DateTimeField(verbose_name='Date_of_Update', auto_now=True)
    p_id = models.ForeignKey('webapp.Projects', on_delete=models.CASCADE, related_name='p_id',
                                verbose_name="p_id")
    def get_absolute_url(self):
        return reverse('view', kwargs={'pk': self.pk})


   # def __str__(self):
        #return f'{self.short_description[:20]}, {self.description[:20]}, {self.status}, {self.type}, {self.date_of_create}, {self.date_of_update}, {self.p_id}'
