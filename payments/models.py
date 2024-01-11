from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255)
    ratio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"Order #{self.pk}"

    def calculate_total_amount(self):
        total_amount = 0

        for item in self.items.all():
            discount_ratio = self.discount.ratio if self.discount and self.discount.ratio is not None else 0
            tax_rate = self.tax.rate if self.tax and self.tax.rate is not None else 0

            item_price = item.price * (1 - discount_ratio) * (1 + tax_rate)
            total_amount += item_price

        self.total_amount = total_amount
        self.save()
