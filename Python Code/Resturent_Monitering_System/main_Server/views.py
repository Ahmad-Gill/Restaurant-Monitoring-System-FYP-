from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.urls import reverse
from .models import GeneratedValue,Categories,CustomerOrderWaitingTime  # Adjust based on your project structure
from django.http import JsonResponse
from .models import GeneratedValue
from python_code.generate_random_value import generate_random_value


# main page
def main(request):
    context={
        "count":2,
        "time":"kahdsl",
    }
    return render(request, "HtmlFiles/main.html",context)

# Categories Section
def categories(request):
    if request.user.is_anonymous:
        return redirect("/login")
    categories_list = Categories.objects.all()

    # Pass the categories to the template
    return render(request, 'HtmlFiles/categories.html', {'categories': categories_list})
# Login / logout
def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user) 
            messages.success(request, f"You logged in as {username}")
            return redirect('categories')  # Redirecting to categories
        else:
            messages.error(request, "Incorrect Username or password")
    
    return render(request, 'HtmlFiles/login.html')
def logoutUser(request):
    logout(request)
    return redirect(reverse('main')) 

# Sample Gineratio py function
def generate_value_view(request):
    generated_value = generate_random_value()  # Call your function to generate a random value
    return render(request, 'your_template.html', {'generated_value': generated_value})  # Replace 'your_template.html' with your actual template name

def analytics_review(request):
    context = {
        "count": 2,
        "time": "kahdsl",
    }
    return render(request, "HtmlFiles/analytics.html", context)

def checks(request):
    context = {
        "time": "kahdsl",
    }
    return render(request, "HtmlFiles/check.html", context)

def staff_info(request):
    context = {
        "time": "kahdsl",
    }
    return render(request, "HtmlFiles/staff.html", context)

def monitoring(request):
    context = {
        "time": "kahdsl",
    }
    return render(request, "HtmlFiles/monitoring.html", context)

# COstomer Waiting Time for Order 

def customer_waiting_time_for_order(request):
    waiting_times = CustomerOrderWaitingTime.objects.all()  # Fetch all records
    context = {
        'waiting_times': waiting_times,
        'active_page': 'statistics', 
    }
    return render(request, 'HtmlFiles/customer_waiting_time_for_order.html', context)
def customer_waiting_time_for_order_Visualization(request):
    waiting_times = CustomerOrderWaitingTime.objects.all()
    context = {
        'waiting_times': waiting_times,
        'active_page': 'Visualization', 
    }
    return render(request, 'HtmlFiles/customer_waiting_time_for_order_Visualization.html', context)