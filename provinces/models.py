from django.db import models


# Create your models here.
class Province(models.Model):
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.CASCADE, related_name='province_circumscription_set'
    )
    ds = models.CharField(max_length=100)
    prefix_cp = models.CharField(max_length=2)

    def __str__(self):
        return self.ds

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
