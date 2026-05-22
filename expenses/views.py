from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum

from .models import Expense, Budget
from .supabase_utils import upload_receipt


# SIGNUP

def signup(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("expense_list")

    else:

        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {
            "form": form
        }
    )


# DASHBOARD / EXPENSE LIST

@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total = expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    budget_obj = Budget.objects.filter(
        user=request.user
    ).first()

    budget = 0

    if budget_obj:

        budget = budget_obj.monthly_budget

    remaining = budget - total

    return render(

        request,

        "expense_list.html",

        {

            "expenses": expenses,
            "total": total,
            "budget": budget,
            "remaining": remaining,

        }
    )


# ADD EXPENSE

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

    return render(
        request,
        "add_expense.html"
    )


# SET MONTHLY BUDGET

@login_required
def set_budget(request):

    if request.method == "POST":

        amount = request.POST.get("budget")

        Budget.objects.update_or_create(

            user=request.user,

            defaults={
                'monthly_budget': amount
            }
        )

        return redirect("expense_list")

    return render(
        request,
        "set_budget.html"
    )