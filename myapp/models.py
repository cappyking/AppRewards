from distutils.command.upload import upload
from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from . import scraper
# Create your models here.


class AppLib(models.Model):
    title = models.CharField(max_length=50,unique=True)
    point = models.IntegerField()
    category = models.CharField(max_length=50, null=True, blank=True)
    applink = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Application'

    def AppLib_pre_save(sender, instance, *args, **kwargs):
        scrapdata = scraper.linkgen(instance.title)
        instance.category = scrapdata[1]
        instance.applink = scrapdata[0]
        users = User.objects.all()
        for i in users:
            task = MasterTaskHolder(
                title=instance.title, point=instance.point, category=instance.category, user=i)
            task.save()


pre_save.connect(AppLib.AppLib_pre_save, sender=AppLib)


class MasterTaskHolder(models.Model):
    status_code = [
        ('C', 'Completed'),
        ('P', 'Pending'),
    ]
    title = models.CharField(max_length=50)
    point = models.IntegerField()
    category = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=2, choices=status_code, default='P')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="imageproof/")

    def __str__(self):
        return (f'{self.user} - '+(f'{self.title}'))

    class Meta:
        verbose_name = 'Master Task Holder'
        verbose_name_plural = 'Master Task Holder'

    def User_post_save(sender, instance, *args, **kwargs):
        if not (MasterTaskHolder.objects.filter(user=instance)):
            apps = AppLib.objects.all()
            for app in apps:
                task = MasterTaskHolder(
                    title=app.title, point=app.point, category=app.category, user=instance)
                print(task)
                task.save()

    def App_delete(sender, instance, *args, **kwargs):
        MasterTaskHolder.objects.filter(title=instance.title).delete()

    def User_delete(sender, instance, *args, **kwargs):
        MasterTaskHolder.objects.filter(user=instance).delete()


post_delete.connect(MasterTaskHolder.App_delete, sender=AppLib)
post_delete.connect(MasterTaskHolder.User_delete, sender=User)
post_save.connect(MasterTaskHolder.User_post_save, sender=User)
