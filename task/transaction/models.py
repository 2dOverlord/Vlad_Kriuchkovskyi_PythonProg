from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


MONTH_CHOICES = (
    ("JANUARY", "January"),
    ("FEBRUARY", "February"),
    ("MARCH", "March"),
    ("APRIL", "April"),
    ("MAY", "May"),
    ("JUNE", "June"),
    ("JULY", "July"),
    ("AUGUST", "August"),
    ("SEPTEMBER", "September"),
    ("OCTOBER", "October"),
    ("NOVEMBER", "November"),
    ("DECEMBER", "December"),
)


class TRANSACTION(models.Model):
    payer_name = models.CharField(max_length=256, )
    card_number = models.PositiveBigIntegerField(default=1000100010001000,
                                                 validators=[MinValueValidator(1000000000000000),
                                                             MaxValueValidator(9999999999999999)])
    month = models.CharField(max_length=9,
                             choices=MONTH_CHOICES,
                             default="JANUARY")
    year = models.PositiveIntegerField(default=2022, validators=[MinValueValidator(2021), MaxValueValidator(2030)])
    CVC = models.PositiveIntegerField(default=111, validators=[MinValueValidator(100), MaxValueValidator(9999)])
    payment_date = models.DateField()
    amount = models.PositiveIntegerField()
