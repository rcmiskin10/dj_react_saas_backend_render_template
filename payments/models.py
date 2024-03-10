from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    tier = models.IntegerField(null=False, blank=False)
    stripe_product_id = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return str(self.name)


# Create your models here.
class ProductDescriptionItem(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="descriptions"
    )
    description = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return str(self.description)


# Create your models here.
class ProductPrice(models.Model):
    # payment interval enum
    class Interval(models.IntegerChoices):
        DAILY = 1, "DAILY"
        WEEKLY = 2, "WEEKLY"
        MONTHLY = 3, "MONTHLY"
        QUARTERLY = 4, "QUARTERLY"
        SEMI = 5, "SEMI"
        YEARLY = 6, "YEARLY"

    # usage type enum
    class Type(models.IntegerChoices):
        RECURRING_PAYMENT = 1, "RecurringPayment"
        ONE_TIME_PAYMENT = 2, "OneTimePayment"

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="prices"
    )
    price = models.DecimalField(max_digits=19, decimal_places=2)
    interval = models.PositiveSmallIntegerField(
        choices=Interval.choices, null=True, blank=True
    )
    type = models.PositiveSmallIntegerField(
        choices=Type.choices, default=Type.RECURRING_PAYMENT
    )
    stripe_price_id = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return str(self.product.name)
