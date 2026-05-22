from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Expense
from .supabase_utils import upload_receipt

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("expense_list")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(exp.amount for exp in expenses)

    return render(request, "expense_list.html", {
        "expenses": expenses,
        "total": total
    })


@login_required
def add_expense(request):
    if request.method == "POST":
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        receipt = request.FILES.get("receipt")

        receipt_url = None
        if receipt:
            receipt_url = upload_receipt(receipt)

        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            receipt_url=receipt_url
        )

        return redirect("expense_list")

    return render(request, "add_expense.html")