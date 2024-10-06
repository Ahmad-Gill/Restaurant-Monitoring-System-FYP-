from django.shortcuts import redirect, render
import json
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.urls import reverse
from .models import GeneratedValue,Categories,CustomerOrderWaitingTime  # Adjust based on your project structure
from django.http import JsonResponse
from .models import GeneratedValue
from django.db.models import DurationField, F, ExpressionWrapper, Sum, Avg
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
        "top_dishes": [
            {"name": "Pizza", "count": 3000},
             {"name": "Pizza", "count": 3000},
              {"name": "Piza", "count": 3000},
               {"name": "Pia", "count": 3000},
                {"name": "Pizza", "count": 3000},
                 {"name": "Pizza", "count": 3000},
                  {"name": "Pizza", "count": 3000},
                   {"name": "Pizza", "count": 3000},

            {"name": "Burger", "count": 250},
            {"name": "Pasta", "count": 200},
            {"name": "Salad", "count": 150},
            {"name": "Steak", "count": 100},
            {"name": "coffee", "count": 20},
            {"name": "chai", "count": 10},
            {"name": "doodh", "count": 100}
        ],
        "customer_count": [
            {"date": "Mon", "customer": 5000},
            {"date": "Tue", "customer": 5500},
            {"date": "Wed", "customer": 6000},
            {"date": "Thu", "customer": 5800},
            {"date": "Fri", "customer": 7000},
            {"date": "Sat", "customer": 8000},
            {"date": "Sun", "customer": 7500}
        ],
        "peak_hours": [
            {"time": "11am", "count": 20},
            {"time": "12pm", "count": 40},
            {"time": "1pm", "count": 60},
            {"time": "2pm", "count": 50},
            {"time": "3pm", "count": 30},
            {"time": "4pm", "count": 35},
            {"time": "5pm", "count": 45},
            {"time": "6pm", "count": 70},
            {"time": "7pm", "count": 80},
            {"time": "8pm", "count": 60}
        ],
        "satisfaction": [
            {"rating": "Excellent", "count": 60},
            {"rating": "Good", "count": 25},
            {"rating": "Average", "count": 10},
            {"rating": "Poor", "count": 5}
        ]
    }
    return render(request, "HtmlFiles/analytics.html", context)

def analytics_tables(request):
    return render(request, 'HtmlFiles/analytics_tables.html')

def checks(request):
    return render(request, "HtmlFiles/check.html")

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
    # Get all waiting times
    waiting_times = CustomerOrderWaitingTime.objects.all()
    
    # Calculate individual waiting times
    waiting_time_data = [
        {
            "table_number": time.table_number,
            "waiting_time": (time.end_time - time.start_time).total_seconds() / 60,  # Convert to minutes
            "date": time.end_time.strftime("%Y-%m-%d")                                  # Use end_time for individual entries
        }
        for time in waiting_times
    ]

    # Calculate total waiting time by end date
    total_waiting_time_by_end_date = (
        CustomerOrderWaitingTime.objects
        .annotate(
            waiting_time=ExpressionWrapper(
                F('end_time') - F('start_time'),
                output_field=DurationField()
            )
        )
        .annotate(end_date=F('end_time__date'))  # Extract only the date from end_time
        .values('end_date')
        .annotate(total_waiting_time=Sum('waiting_time'))
        .order_by('end_date')
    )

    # Prepare the total waiting time data
    total_waiting_time_data = [
        {
            "date": entry['end_date'].strftime("%Y-%m-%d"),  # Format end_date
            "total_waiting_time": entry['total_waiting_time'].total_seconds() / 60  # Convert to minutes
        }
        for entry in total_waiting_time_by_end_date
    ]

    # Prepare context with both waiting time data and total waiting time data
    context = {
        'waiting_time_data': waiting_time_data,
        'total_waiting_time_data': total_waiting_time_data,  # Add total waiting time data to context
        'active_page': 'Visualization',
    }
    
    return render(request, 'HtmlFiles/customer_waiting_time_for_order_Visualization.html', context)