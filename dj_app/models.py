import warnings
from django.db import models
warnings.filterwarnings('ignore')


class Company(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    company = models.ForeignKey('Company', on_delete=models.SET_NULL,
                                related_name='transactions', null=True)
    txn_date = models.DateTimeField()
    qty = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total = self.qty * self.rate
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.company.name} - {self.qty}'
