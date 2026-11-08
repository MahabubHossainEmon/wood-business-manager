import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Customer, Sale, Payment, WoodType
from .forms import CustomerForm, SaleForm, PaymentForm, WoodTypeForm

@login_required
def dashboard(request):
    customers = Customer.objects.all()
    sales_total = Sale.objects.aggregate(v=Sum("total_amount"))["v"] or Decimal("0")
    paid_total = Payment.objects.aggregate(v=Sum("amount"))["v"] or Decimal("0")
    due_total = sales_total - paid_total
    context = {
        "customer_count": customers.count(), "sales_total": sales_total,
        "paid_total": paid_total, "due_total": due_total,
        "wood_types": WoodType.objects.all(),
        "recent_sales": Sale.objects.select_related("customer")[:6],
        "recent_payments": Payment.objects.select_related("customer")[:6],
        "top_due": sorted(customers, key=lambda c: c.due, reverse=True)[:8],
    }
    return render(request, "accounts/dashboard.html", context)

@login_required
def customer_list(request):
    return render(request, "accounts/customer_list.html", {"customers": Customer.objects.all()})

@login_required
def customer_add(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "কাস্টমার যোগ হয়েছে।")
        return redirect("customer_list")
    return render(request, "accounts/form.html", {"form": form, "title": "নতুন কাস্টমার"})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "accounts/customer_detail.html", {
        "customer": customer, "sales": customer.sales.all(), "payments": customer.payments.all()
    })

@login_required
def sale_add(request):
    form = SaleForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic():
            sale = form.save(commit=False)
            if sale.wood_type and sale.quantity > 0:
                wood = WoodType.objects.select_for_update().get(pk=sale.wood_type_id)
                if wood.quantity < sale.quantity:
                    form.add_error("quantity", f"স্টকে পর্যাপ্ত কাঠ নেই। বর্তমান মজুত: {wood.quantity} {wood.unit}")
                    return render(request, "accounts/form.html", {"form": form, "title": "নতুন বিক্রি"})
                wood.quantity -= sale.quantity
                wood.save()
                if not sale.unit:
                    sale.unit = wood.unit
            sale.save()
        messages.success(request, "বিক্রির হিসাব যোগ হয়েছে।")
        return redirect("dashboard")
    return render(request, "accounts/form.html", {"form": form, "title": "নতুন বিক্রি"})

@login_required
def payment_add(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save()
        messages.success(request, "টাকা জমার হিসাব যোগ হয়েছে।")
        return redirect("customer_detail", pk=payment.customer_id)
    return render(request, "accounts/form.html", {"form": form, "title": "টাকা জমা নিন"})

@login_required
def stock_list(request):
    if request.method == "POST":
        form = WoodTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "কাঠের স্টক যোগ হয়েছে।")
            return redirect("stock_list")
    else:
        form = WoodTypeForm()
    return render(request, "accounts/stock.html", {"woods": WoodType.objects.all(), "form": form})

@login_required
def reports(request):
    sales = Sale.objects.select_related("customer").all()
    payments = Payment.objects.select_related("customer").all()
    return render(request, "accounts/reports.html", {
        "sales": sales[:100], "payments": payments[:100],
        "sales_total": sales.aggregate(v=Sum("total_amount"))["v"] or Decimal("0"),
        "paid_total": payments.aggregate(v=Sum("amount"))["v"] or Decimal("0"),
        "due_total": (sales.aggregate(v=Sum("total_amount"))["v"] or Decimal("0")) - (payments.aggregate(v=Sum("amount"))["v"] or Decimal("0")),
    })

@login_required
def backup_json(request):
    if not request.user.is_superuser:
        return HttpResponse("শুধু Admin ব্যাকআপ নিতে পারবেন।", status=403)
    payload = {
        "created_at": timezone.now().isoformat(),
        "customers": list(Customer.objects.values()),
        "wood_types": list(WoodType.objects.values()),
        "sales": list(Sale.objects.values()),
        "payments": list(Payment.objects.values()),
    }
    response = HttpResponse(json.dumps(payload, ensure_ascii=False, default=str, indent=2), content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="wood_business_backup.json"'
    return response
