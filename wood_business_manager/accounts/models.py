from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField("নাম", max_length=150)
    phone = models.CharField("মোবাইল", max_length=30, blank=True)
    address = models.TextField("ঠিকানা", blank=True)
    notes = models.TextField("নোট", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "কাস্টমার"
        verbose_name_plural = "কাস্টমার"

    def __str__(self):
        return self.name

    @property
    def total_sales(self):
        return self.sales.aggregate(v=Sum("total_amount"))["v"] or Decimal("0.00")

    @property
    def total_paid(self):
        return self.payments.aggregate(v=Sum("amount"))["v"] or Decimal("0.00")

    @property
    def due(self):
        return self.total_sales - self.total_paid

class WoodType(models.Model):
    name = models.CharField("কাঠের নাম/ধরন", max_length=120, unique=True)
    unit = models.CharField("একক (CFT/পিস/টন)", max_length=20, default="CFT")
    quantity = models.DecimalField("বর্তমান মজুত", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    purchase_rate = models.DecimalField("গড় ক্রয়দর", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "কাঠের স্টক"
        verbose_name_plural = "কাঠের স্টক"

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales", verbose_name="কাস্টমার")
    wood_type = models.ForeignKey(WoodType, on_delete=models.PROTECT, null=True, blank=True, related_name="sales", verbose_name="কাঠের ধরন")
    quantity = models.DecimalField("পরিমাণ", max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    unit = models.CharField("একক", max_length=20, blank=True)
    total_amount = models.DecimalField("মোট টাকা", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    details = models.TextField("বিবরণ", blank=True)
    date = models.DateField("তারিখ", default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]
        verbose_name = "বিক্রি"
        verbose_name_plural = "বিক্রি"

    def __str__(self):
        return f"{self.customer} - ৳{self.total_amount}"

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="payments", verbose_name="কাস্টমার")
    amount = models.DecimalField("জমার পরিমাণ", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    date = models.DateField("জমার তারিখ", default=timezone.localdate)
    method = models.CharField("মাধ্যম", max_length=30, default="নগদ")
    note = models.CharField("নোট/রেফারেন্স", max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]
        verbose_name = "টাকা জমা"
        verbose_name_plural = "টাকা জমা"

    def __str__(self):
        return f"{self.customer} - ৳{self.amount}"
