# Importing necessary modules for handling HTTP requests and rendering templates
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse
import base64
import ast
from django.db.models import ExpressionWrapper
from django.db.models import F
from django.db.models import DurationField
from django.db.models import Sum



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




def calculate_frame_quality(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_frame, cv2.CV_64F).var()  # Sharpness
    brightness = np.mean(frame)  # Brightness
    contrast = np.std(frame)  # Contrast
    
    quality_score = laplacian_var * 0.5 + brightness * 0.3 + contrast * 0.2
    return quality_score

def convert_video_to_one_best_frame_per_minute(frames, output_folder=None):
    if not frames:
        return None

    # Randomly select 50 frames if there are more than 50 frames available
    selected_frames = random.sample(frames, min(len(frames), 10))

    best_frame = None
    best_quality_score = -1  

    for frame in selected_frames:
        quality_score = calculate_frame_quality(frame)
        if quality_score > best_quality_score:
            best_quality_score = quality_score
            best_frame = frame

    if best_frame is None:
        return None

    return best_frame

def create_cropped_grid_video(input_folder, grid_numbers=[1, 2, 3], grid_size=(20, 20)):
    input_folder = Path(input_folder).resolve()
    output_folder = input_folder.parent / f"{input_folder.name}_cropped"
    output_folder.mkdir(exist_ok=True)

    for filename in os.listdir(input_folder):
        file_path = input_folder / filename
        if not file_path.is_file():
            continue
        
        frame = cv2.imread(str(file_path))
        if frame is None:
            continue

        frame_height, frame_width, _ = frame.shape
        num_rows, num_cols = grid_size
        cell_h = frame_height // num_rows
        cell_w = frame_width // num_cols

        grid_positions = [((num - 1) // num_cols, (num - 1) % num_cols) for num in grid_numbers]
        min_row = min(row for row, _ in grid_positions)
        max_row = max(row for row, _ in grid_positions)
        min_col = min(col for _, col in grid_positions)
        max_col = max(col for _, col in grid_positions)

        tl_y = min_row * cell_h
        br_y = (max_row + 1) * cell_h
        tl_x = min_col * cell_w
        br_x = (max_col + 1) * cell_w
        cropped_frame = frame[tl_y:br_y, tl_x:br_x]

        output_path = output_folder / filename
        cv2.imwrite(str(output_path), cropped_frame)
        with open("output_path.txt", "w") as file:
            file.write(str(output_folder))

    # try:
    #     shutil.rmtree(input_folder)
    # except Exception as e:
    #     pass

    return output_folder



def process_images(input_folder):
    input_folder = Path(input_folder).resolve()
    output_folder = input_folder.parent / f"{input_folder.name}_enhancement1"
    output_path_file = input_folder.parent / "output_path.txt"
    with open(output_path_file, "w") as file:
        file.write(str(output_folder))
    
    output_folder.mkdir(exist_ok=True)
    
    for filename in os.listdir(input_folder):
        file_path = input_folder / filename
        if file_path.is_file():
            image = cv2.imread(str(file_path), cv2.IMREAD_COLOR)
            if image is None:
                continue
            doubled_frame = cv2.resize(image, None, fx=6, fy=6, interpolation=cv2.INTER_LINEAR)
            output_path = output_folder / filename
            cv2.imwrite(str(output_path), doubled_frame)
    
    # try:
    #     shutil.rmtree(input_folder)
    # except Exception as e:
    #     pass
    
    return output_folder
def extract_date_from_video_path(video_path):
    filename = os.path.basename(video_path)
    date_pattern = re.compile(r"_(\d{8})(\d{6})_")
    match = date_pattern.search(filename)
    if match:
        return match.group(1)
    return "unknown_date"


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

def get_video_paths_by_time(raw_folder_path):
    video_files = [f for f in os.listdir(raw_folder_path) if f.endswith(('.mp4', '.avi', '.mkv', '.dav'))]
    pattern = re.compile(r"_(\d{8})(\d{6})_")

    videos_with_time = [
        (match.group(2), os.path.join(raw_folder_path, f))
        for f in video_files if (match := pattern.search(f))
    ]

    if not videos_with_time:
        return {}, None

    videos_with_time.sort(key=lambda x: x[0])
    video_dict = {i + 1: path for i, (_, path) in enumerate(videos_with_time)}

    first_date = pattern.search(video_files[0]).group(1)
    formatted_date = f"{first_date[6:8]}_{first_date[4:6]}_{first_date[0:4]}"

    json_filename = f"{formatted_date}_dictionary.json"
    with open(json_filename, "w") as file:
        json.dump(video_dict, file, indent=4)

    return video_dict, formatted_date
def process_all_videos_and_save_frames(video_paths):
    all_selected_frames = []

    # Set the output directory to the current directory
    output_folder = os.getcwd()
    frame_count = 1  # Counter to name frames uniquely

  # Create an empty file

    for video_path in video_paths:
        print(f"Processing video: {video_path}")

        # Extract date and create a folder named after the date
        date_folder_name = extract_date_from_video_path(video_path)
        date_folder_path = os.path.join(output_folder, date_folder_name)
        os.makedirs(date_folder_path, exist_ok=True)
        with open("output_path.txt", "w") as file:  # "w" mode clears the file before writing
            file.write(date_folder_path)

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Could not open video {video_path}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames_per_chunk = int(fps * 30)  # 30 seconds worth of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        best_frames = []

        chunk_number = 1
        while True:
            frames = []
            # Capture frames for one 30-second chunk or remaining frames
            for i in range(total_frames_per_chunk):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)

            # If no frames were captured, we are at the end of the video
            if not frames:
                break

            # Process the current chunk
            best_frame = convert_video_to_one_best_frame_per_minute(frames)
            best_frames.append(best_frame)

            print(f"Processed chunk {chunk_number} from video {video_path}")
            chunk_number += 1

            # Save the processed frame
            frame_path = os.path.join(date_folder_path, f"frame_{frame_count}.png")
  # Save as PNG for better quality
            plt.imshow(cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.savefig(frame_path, bbox_inches='tight', pad_inches=0)
            print(f"Saved frame {frame_count} at {frame_path}")
            frame_count += 1

        # Check if there are leftover frames and process them
        remaining_frames = total_frames % total_frames_per_chunk
        if remaining_frames > 0:
            print(f"Processing remaining {remaining_frames} frames for video {video_path}")
            leftover_frames = []
            for _ in range(remaining_frames):
                ret, frame = cap.read()
                if ret:
                    leftover_frames.append(frame)
            if leftover_frames:
                best_frame = convert_video_to_one_best_frame_per_minute(leftover_frames)
                best_frames.append(best_frame)

                # Save the leftover frame
                frame_path = os.path.join(date_folder_path, f"frame_{frame_count}.png")
                plt.imshow(cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB))
                plt.axis('off')
                plt.savefig(frame_path, bbox_inches='tight', pad_inches=0)
                print(f"Saved leftover frame {frame_count} at {frame_path}")
                frame_count += 1

        # Release video capture for the current video
        cap.release()

        # Store all best frames from the current video
        all_selected_frames.extend(best_frames)



    print(f"Frames saved successfully in folder: {output_folder}")
    return output_folder


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

def preprocessing_2(request):
    url_ = "/categories/"
    link_text = "Categories"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    raw_folder = r"D:\FYP - Copy\preprocessing\Video Preprocessing\New folder"
    video_dict, formatted_date = get_video_paths_by_time(raw_folder)
    if not video_dict:
        return
    output_folder=process_all_videos_and_save_frames(list(video_dict.values()))
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()
    print(saved_path)
    output_folder=process_images(saved_path)
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()
    grids_folder = os.path.join(os.getcwd(), 'media', 'videos')
    grids_file_path = os.path.join(grids_folder, 'grids.txt')
    with open(grids_file_path, 'r') as file:
        grids_data_str = file.read().strip()
    grids_data_str = grids_data_str.strip("'")
    grids_data = ast.literal_eval(grids_data_str)
    grid_numbers = [int(num) for num in grids_data]
    output_folder=create_cropped_grid_video(saved_path, grid_numbers=grid_numbers)
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()

    output_folder=process_images(saved_path)
    context = {
        'title': 'Preprocessing Completed - Congratulations!',
        'preprocessing': True,
        'url_': url_,
        'link_text': link_text,
    }
    return render(request, 'HtmlFiles/preprocessing_2.html', context)
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