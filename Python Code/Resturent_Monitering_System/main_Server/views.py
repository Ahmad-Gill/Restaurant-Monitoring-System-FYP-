# Importing necessary modules for handling HTTP requests and rendering templates
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse

# Importing models for database interactions
from .models import GeneratedValue, Categories, CustomerOrderWaitingTime

# Importing modules for generating and handling data
from python_code.generate_random_value import generate_random_value

# Modules for image processing and visualization
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Modules for file handling and storage
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings

# Modules for miscellaneous tasks such as creating unique IDs, handling JSON data, etc.
import uuid
import json
import random
import re

# Modules for file and directory management
import os
import shutil

# Subprocess module for running system commands if required
import subprocess





# **************************************************************

# helping Functions


# **************************************************************












def apply_grids(frame, grid_size=(20, 20)):
    h, w = frame.shape[:2]
    cell_h, cell_w = h // grid_size[0], w // grid_size[1]
    
    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            tl_x, tl_y = col * cell_w, row * cell_h
            br_x, br_y = tl_x + cell_w, tl_y + cell_h
            cv2.rectangle(frame, (tl_x, tl_y), (br_x, br_y), (255, 0, 0), 2)
            grid_num = row * grid_size[1] + col + 1
            cv2.putText(frame, f'Grid {grid_num}', (tl_x + 5, tl_y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    return frame

def display_frame_with_grids(video_path, grid_size=(20, 20)):
    if not os.path.isfile(video_path):
        print(f"Error: {video_path} not found.")
        return None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Failed to read the first frame.")
        return None

    frame_with_grids = apply_grids(frame, grid_size)
    output_path = os.path.join(os.getcwd(), 'output_frame_with_grids.png')
    try:
        cv2.imwrite(output_path, frame_with_grids)
        print(f"Frame saved at: {output_path}")
        cap.release()
        return output_path
    except Exception as e:
        print(f"Error saving the frame: {e}")
        return None

def get_first_video(folder_path, valid_extensions=(".dav", ".mp4", ".avi", ".mkv")):
    files = [f for f in os.listdir(folder_path) if f.endswith(valid_extensions)]
    if not files:
        print("No video files found in the folder.")
        return None
    first_video = sorted(files)[0]
    return os.path.join(folder_path, first_video)




# **************************************************************

# Main Functions


# **************************************************************


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



# main page
def main(request):
    url_ = "/"  
    link_text = "Home"
    context = {
        "count": 2,
        "time": "kahdsl",
        "url_": url_, 
        "link_text": link_text, 
    }

    return render(request, "HtmlFiles/main.html", context)

# Categories Section
def categories(request):
    if request.user.is_anonymous:
        return redirect("/login")  
    
    url_ = "/categories/"  
    link_text = "Categories"
    
    categories_list = Categories.objects.all() 
    context = {
        'categories': categories_list,
        'url_': url_,
        'link_text': link_text, 
    }

    return render(request, 'HtmlFiles/categories.html', context)


# Select Vidoes 

def select_video(request):
    is_uploaded = False
    print(f"Request method: {request.method}")

    url_ = "/categories/"
    link_text = "Categories"
    video_paths = []
    video_urls = []
    frame_images = []
    video_folder = os.path.join(settings.MEDIA_ROOT, 'videos', 'uploaded_videos')
    urls_file_path = os.path.join(video_folder, 'video_urls.txt')

    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    if request.method == 'POST' and request.FILES.getlist('videos'):
        print("Handling video upload...")
        videos = request.FILES.getlist('videos')

        for filename in os.listdir(video_folder):
            file_path = os.path.join(video_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        open(urls_file_path, 'w').close()

        processed_videos = set()

        with open(urls_file_path, 'w') as url_file:
            for video in videos:
                if video.name in processed_videos:
                    continue

                processed_videos.add(video.name)

                fs = FileSystemStorage(location=video_folder, base_url='/media/videos/uploaded_videos/')
                video_path = fs.save(video.name, video)
                video_full_path = fs.path(video.name)

                video_paths.append(video_path)
                video_url = fs.url(video.name)
                video_urls.append(video_url)

                url_file.write(video_url + '\n')
                print(f"Saved video: {video.name} at {video_url}")
                is_uploaded = True

    for filename in os.listdir(video_folder):
        if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_full_path = os.path.join(video_folder, filename)

    print(f"Upload status: {is_uploaded}")

    return render(request, 'HtmlFiles/Add_Video.html', {
        'video_paths': video_paths,
        'is_uploaded': is_uploaded,
        'video_urls': video_urls,
        'url_': url_,
        'link_text': link_text,
    })



# Preprocesing 
def preprocessing(request):
    url_ = "/categories/"  
    link_text = "Categories"
    if request.method == 'POST':
        video_folder = os.path.join(os.getcwd(), 'media', 'videos', 'uploaded_videos')
        raw_folder = get_first_video(video_folder)

        if not raw_folder or not os.path.isfile(raw_folder):
            return render(request, 'HtmlFiles/preprocessing.html', {'frame_rgb': None,"url_": url_, "link_text": link_text,})

        # Extract frame with grids
        frame_rgb_path = display_frame_with_grids(raw_folder, (20, 20))

        if frame_rgb_path:
            try:
                with open(frame_rgb_path, "rb") as img_file:
                    frame_data = img_file.read()
                    frame_base64 = base64.b64encode(frame_data).decode('utf-8')
                return render(request, 'HtmlFiles/preprocessing.html', {'frame_rgb': frame_base64,"url_": url_, "link_text": link_text,})
            except Exception as e:
                print(f"Error encoding frame: {e}")
        return render(request, 'HtmlFiles/preprocessing.html', {'frame_rgb': None,"url_": url_, "link_text": link_text,})
    else:
        return render(request, 'HtmlFiles/preprocessing.html', {'frame_rgb': None,"url_": url_, "link_text": link_text,})







# Second Preprocessing
def preprocessing_1(request):
    url_ = "/categories/"
    link_text = "Categories"
    video_folder = os.path.join(os.getcwd(), 'media', 'videos')
    os.makedirs(video_folder, exist_ok=True)
    file_path = os.path.join(video_folder, 'grids.txt')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            grids = data.get('grids', [])
            with open(file_path, 'w') as file:
                file.write(json.dumps(grids) + '\n')
            return render(request, 'HtmlFiles/preprocessing_1.html', {'grids': grids})
        except (json.JSONDecodeError, KeyError) as e:
            return render(request, 'HtmlFiles/preprocessing_1.html', {'error': 'Invalid data format'})
        except Exception as e:
            return render(request, 'HtmlFiles/preprocessing_1.html', {'error': 'An error occurred while processing your request'})
    elif request.method == 'GET':
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    grids = [json.loads(line.strip()) for line in file.readlines()]
            else:
                grids = []
            return render(request, 'HtmlFiles/preprocessing_1.html', {'grids': grids, "url_": url_, "link_text": link_text})
        except Exception as e:
            return render(request, 'HtmlFiles/preprocessing_1.html', {'error': 'Could not read grids', "url_": url_, "link_text": link_text})

    return render(request, 'HtmlFiles/preprocessing_1.html', {'error': 'Invalid request method', "url_": url_, "link_text": link_text})





def analytics_review(request):
    url_ = "/categories/"  
    link_text = "Categories"
    context = {
        'url_': url_,
        'link_text': link_text, 
         'active_page': 'Visualization',
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
    url_ = "/categories/"  
    link_text = "Categories"
    context = {
        'active_page': 'statistics', 
        'url_': url_,
        'link_text': link_text, 
    }
    return render(request, 'HtmlFiles/analytics_tables.html',context)

def checks(request):
    url_ = "/categories/"  
    link_text = "Categories"
    context = {
        'active_page': 'statistics', 
        'url_': url_,
        'link_text': link_text, 
    }
    return render(request, "HtmlFiles/check.html",context)

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
    url_ = "/categories/"  
    link_text = "Categories"
    waiting_times = CustomerOrderWaitingTime.objects.all()  # Fetch all records
    context = {
        'url_': url_,
        'link_text': link_text, 
        'waiting_times': waiting_times,
        'active_page': 'statistics', 
    }
    return render(request, 'HtmlFiles/customer_waiting_time_for_order.html', context)
def customer_waiting_time_for_order_Visualization(request):
    # Get all waiting times
    waiting_times = CustomerOrderWaitingTime.objects.all()
    url_ = "/categories/"  
    link_text = "Categories"
    
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
                'url_': url_,
        'link_text': link_text,
        'waiting_time_data': waiting_time_data,
        'total_waiting_time_data': total_waiting_time_data,  # Add total waiting time data to context
        'active_page': 'Visualization',
    }
    
    return render(request, 'HtmlFiles/customer_waiting_time_for_order_Visualization.html', context)