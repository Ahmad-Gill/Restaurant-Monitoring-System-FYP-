# Importing necessary modules for handling HTTP requests and rendering templates
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse
import base64
from django.core.files import File
import ast
from django.db.models import ExpressionWrapper
from django.db.models import Count
from django.db.models import F
from django.db.models import DurationField
from django.utils.timezone import now
from django.db.models import Sum
from django.http import StreamingHttpResponse
import time
from django.db.models import Count, Max
from .forms import ContactForm
from .models import Visitor


# Importing models for database interactions
from .models import GeneratedValue, Categories, CustomerOrderWaitingTime,CustomerOrderSummary



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
from django.core.mail import send_mail
from roboflow import Roboflow
from collections import defaultdict





# **************************************************************

# helping Functions


# **************************************************************




# --------------------------------------------Draw general rectanges around the person or food---------------------
def draw_predictions(image_path: str, predictions: dict, output_folder: str):
    img = cv2.imread(image_path)
    if img is None:
        return None
    for prediction in predictions.get('predictions', []):
        class_name = prediction['class']
        confidence = prediction['confidence'] * 100
        if (class_name == "meal" and confidence > 50) or (class_name == "people"):  # we have set the confidence level for meels 
            x, y, w, h = prediction['x'], prediction['y'], prediction['width'], prediction['height']
            x1, y1 = int(x - w / 2), int(y - h / 2)
            x2, y2 = int(x + w / 2), int(y + h / 2)
            color = (0, 255, 0) if class_name == "meal" else (255, 0, 0)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            label = f"{class_name}: {confidence:.2f}%"
            font, font_scale, thickness = cv2.FONT_HERSHEY_SIMPLEX, 2.5, 4
            (label_width, label_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            y_label = max(y1 - 10, label_height + 10)
            cv2.rectangle(img, (x1, y_label - label_height - baseline), (x1 + label_width, y_label + baseline), color, cv2.FILLED)
            cv2.putText(img, label, (x1, y_label), font, font_scale, (0, 0, 0), thickness)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, img)    
    return output_path



# --------------------------------------------Draw Specific rectangles around the food---------------------
def draw_food_boxes_on_image(image_path, predictions):
    print(f"Drawing food boxes on image: {image_path}")
    img = cv2.imread(image_path)
    for p in predictions['predictions']:
        class_name = p['class']
        x1, y1, x2, y2 = int(p['x'] - p['width'] / 2), int(p['y'] - p['height'] / 2), int(p['x'] + p['width'] / 2), int(p['y'] + p['height'] / 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name}: {p['confidence'] * 100:.2f}%"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - label_size[1] - 5), (x1 + label_size[0], y1 + 5), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return img



# ----------------------------------------------------------------how many times each class appears in the image------------
def process_food_image(image_path, model):
    predictions = model.predict(image_path, confidence=10, overlap=30).json()
    if not predictions['predictions']:
        return None, None
    results = defaultdict(int)
    for p in predictions['predictions']:
        results[p['class']] += 1
    return results, predictions




# ---------------------------------------------------Check if the new image has higher count for a certain food item than the existing image------------
def should_update_best_food_image(existing_results, new_results):
    if not existing_results:
        return True 
    for food_item, new_count in new_results.items():
        if new_count > existing_results.get(food_item, 0):
            return True
    return False



# -----------------------------------------------------------------Main function for food detection------------
def food_detection_main(folder_path):
    rf = Roboflow(api_key="mT8SBwz3f0nxhicDovAc")
    project = rf.workspace().project("food_detection-pwh9v")
    model = project.version(1).model
    if not os.path.exists(folder_path):
        return
    date_match = re.search(r"(\d{8})", folder_path)                                                                   #extract date from path 
    if not date_match:
        return
    folder_date = date_match.group(1)
    best_food_results = defaultdict(int)
    best_food_image_path = None
    best_food_predictions = None
    best_food_output_path = os.path.join(folder_path, f"best_food_output_{folder_date}.jpg")
    for filename in sorted(os.listdir(folder_path), reverse=True):                                                     # sort like it cecks images in a order 
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            processed_results, predictions = process_food_image(image_path, model)                                     #call the predictions
            if processed_results and should_update_best_food_image(best_food_results, processed_results):              #should contain only the best image
                best_food_results = {k: max(best_food_results.get(k, 0), v) for k, v in processed_results.items()}
                best_food_image_path = image_path
                best_food_predictions = predictions
                processed_image = draw_food_boxes_on_image(best_food_image_path, best_food_predictions)
                cv2.imwrite(best_food_output_path, processed_image)
    print(f"Final food detection results: {dict(best_food_results)}")
    print("Food detection complete.")
    return dict(best_food_results)

# -----------------------------------------------------------------person dection--------------
def perform_detection(model, image_path: str):
    predictions = model.predict(image_path, confidence=10, overlap=30).json()
    return predictions




# ----------------------------------------------------------------COunt people and food --------------------------------
def count_classes(predictions: dict):
    person_count = 0
    meal_count = 0
    for prediction in predictions.get('predictions', []):
        class_name = prediction['class']
        confidence = prediction['confidence'] * 100  # Convert confidence to percentage
        if class_name == "people":
            person_count += 1
        elif class_name == "meal" and confidence > 50:  # Count only if confidence > 50%
            meal_count += 1
    return person_count, meal_count



# -----------------------------------------------------------------sort Image Paths --------------------------------
def natural_sort_key(path):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', os.path.basename(path))]




# -----------------------------------------------------------------initialize Person dection model --------------------------------
def initialize_model(api_key: str, project_name: str, version: int):
    rf = Roboflow(api_key=api_key)
    project = rf.workspace().project(project_name)
    model = project.version(version).model
    return model


#----------------------------main function taht controll both person and food dectons and combine them together------------------------------------------------
def process_folder(input_folder: str, output_folder: str):
    print(f"Processing folder: {input_folder}")
    total_frame_count = 0
    frame_count_for_meal = 0
    max_people = 0
    tracking_active = False
    food_folder_created = False
    num_of_party=False
    new_entry_id = 1  
    hour_mapping = {f"{h:02}": f"{(h-1)%12+1}{'AM' if h < 12 else 'PM'}" for h in range(24)}       #to extract time from image paths 
    hour_mapping["00"] = "12AM" 
    model = initialize_model(api_key="mT8SBwz3f0nxhicDovAc", project_name="person_detection-efko2", version=1)
    image_paths = [os.path.join(input_folder, img) for img in os.listdir(input_folder) if img.endswith(".png")]
    image_paths.sort(key=natural_sort_key)  # Ensure numerical sorting
    if not image_paths:
        return 
    #make relevent directories to store preprocessed images after detection
    food_folder = os.path.join(os.path.dirname(input_folder), os.path.basename(input_folder) + "_food")
    os.makedirs(food_folder, exist_ok=True)
    predictions_folder = os.path.join(output_folder, os.path.basename(input_folder) + "_predictions")
    os.makedirs(predictions_folder, exist_ok=True)
    json_file = os.path.join(os.path.dirname(input_folder), f"{os.path.basename(input_folder)}.json")
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            existing_data = json.load(f)
            new_entry_id = len(existing_data) + 1
    else:
        existing_data = {}
    max_person_per_hour = defaultdict(int)
    for idx, image_path in enumerate(image_paths):
        if not num_of_party:                       #only for testing either this code runs for entire day with separate jsons for every new customer
            print("No party detected yet. Waiting for a party...",new_entry_id)
            print("waiting for party...")
            print("total_frame_count",total_frame_count)
            print("frame_count_for_meal",frame_count_for_meal)
            print("max_people",max_people)
            print("tracking_active",tracking_active)
            print("food_folder_created ",food_folder_created )
        predictions = perform_detection(model, image_path)      #call the function to predict
        person_count, meal_count = count_classes(predictions)   #function to count
        match = re.search(r"frame_\d{8}(\d{2})\d{4}_\d+", image_path) #xtract time from iamge path
        if match:
                hour = match.group(1) 
                readable_hour = hour_mapping.get(hour, hour) 
                max_person_per_hour[readable_hour] = max(max_person_per_hour[readable_hour], person_count)
        print(f"Person: {person_count} Meal Count: {meal_count}")
        if person_count >= 2 or tracking_active:       #this code only works whne there is a person in in the frame or we are already in a tracking phase 
            num_of_party=True                          #this code shos that we found the party and it will count time untill this party leaves 
            max_people = max(max_people, person_count)
            if person_count >= 2 and meal_count >= 1 and not tracking_active:          #tracting is only active when there is a meal available and also a person this also use when there is a left behind meal after party leaves
                tracking_active = True
                food_folder_created = True
            if tracking_active:                                                 # if tracking  is active
                shutil.copy(image_path, food_folder)
                if person_count <= 1:             #complete one round like one part leaves the table 
                    result = food_detection_main(food_folder)   #starts food detectionon entire duration for food 

                    existing_data[new_entry_id] = {        #save data for one party 
                        "total_time": (total_frame_count * 30) / 60,
                        "time_before_meal": (frame_count_for_meal * 30) / 60,
                        "meal": result,
                        "total_people": max_people,
                        "total_people_per_hour": dict(max_person_per_hour) 
                    }

                    with open(json_file, "w") as f:
                        json.dump(existing_data, f, indent=4)

                        #Reset all settings for next party 
                    total_frame_count = 0
                    num_of_party=False
                    new_entry_id+=1
                    frame_count_for_meal = 0
                    max_people = 0
                    tracking_active = False
                    food_folder_created = False
            if not tracking_active and person_count > 1:   # if there is no already party having (no tracking) then this  code workd  and start counter
                frame_count_for_meal += 1
                total_frame_count=frame_count_for_meal
            if tracking_active:                            # it only counts the total time like when the people sits in the able to when they leave 
                total_frame_count += 1
        prediction_image_path = draw_predictions(image_path, predictions, predictions_folder)    #save all the images only for testing 
    if food_folder_created:           #this only  work when there no person in the entire data then this code runs and made the json file 
        with open(json_file, "w") as f:
            json.dump(existing_data, f, indent=4)
        print(f"Final JSON saved at {json_file}.")
    print("All frames processed successfully. Exiting.")



# ----------------------------------------------------------------Check the fame quality in terms of brightness,sharpnessand contrast----------
def calculate_frame_quality(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_frame, cv2.CV_64F).var()  # Sharpness
    brightness = np.mean(frame)  # Brightness
    contrast = np.std(frame)  # Contrast
    quality_score = laplacian_var * 0.5 + brightness * 0.3 + contrast * 0.2
    return quality_score

# -----------------------------------------------------------------Select the best frame for each minute in the video-----------
def convert_video_to_one_best_frame_per_minute(frames, output_folder=None):
    if not frames:
        return None
    # Randomly select 50 frames if there are more than 50 frames available
    selected_frames = random.sample(frames, min(len(frames), 10))
    best_frame = None
    best_quality_score = -1  
    for frame in selected_frames:
        quality_score = calculate_frame_quality(frame)  #call the function to check the quality, it return a score 
        if quality_score > best_quality_score:
            best_quality_score = quality_score
            best_frame = frame
    if best_frame is None:
        return None
    return best_frame


# -----------------------------------------------------------------Crop the frames to create a grid frames-----------
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

    # try:                                    code to delete the previous input folder to reduce memory usage
    #     shutil.rmtree(input_folder)
    # except Exception as e:
    #     pass

    return output_folder



# -----------------------------------------------------------------resize 6 times greater the images using OpenCV-----------
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
    # try:                            code to delete the previous input folder to reduce memory usage
    #     shutil.rmtree(input_folder)
    # except Exception as e:
    #     pass
    
    return output_folder



# -----------------------------------------------------------------Extract date from video-----------
def extract_date_from_video_path(video_path):
    filename = os.path.basename(video_path)
    date_pattern = re.compile(r"_(\d{8})(\d{6})_")
    match = date_pattern.search(filename)
    if match:
        return match.group(1)
    return "unknown_date"




# -----------------------------------------------------------------Main function for vidoe to frames conversion Process all videos and save frames-----------
def process_all_videos_and_save_frames(video_paths):
    all_selected_frames = []
    output_folder = os.getcwd()
    frame_count = 1 
    for video_path in video_paths:
        match = re.search(r"[^\\]+_(\d{14})_", video_path)
        if match:
            timestamp = match.group(1) 
        else:
            timestamp = "unknown"
        print(f"Processing video: {video_path}")
        date_folder_name = extract_date_from_video_path(video_path)
        date_folder_path = os.path.join(output_folder, date_folder_name)
        os.makedirs(date_folder_path, exist_ok=True)
        with open("output_path.txt", "w") as file:                           #clears the file before writing
            file.write(date_folder_path)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            continue
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames_per_chunk = int(fps * 30)                                  # 30 seconds worth of frames    
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        best_frames = []
        chunk_number = 1
        while True:
            frames = []
                                                             # Capture frames for one 30-second chunk 
            for i in range(total_frames_per_chunk):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            if not frames:
                break
            best_frame = convert_video_to_one_best_frame_per_minute(frames)    #CALL function to get best frames from all 30*15 frames 
            best_frames.append(best_frame)
            chunk_number += 1                                                                                    
            frame_path = os.path.join(date_folder_path, f"frame_{timestamp}_{frame_count}.png")# Save the processed frame
            plt.imshow(cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.savefig(frame_path, bbox_inches='tight', pad_inches=0)
            print(f"Saved frame {frame_count} at {frame_path}")
            frame_count += 1

        # Check if there are leftover frames and process them
        remaining_frames = total_frames % total_frames_per_chunk
        if remaining_frames > 0:             # in case there is a less fames then 30*15 then use this code 
            leftover_frames = []
            for _ in range(remaining_frames):
                ret, frame = cap.read()
                if ret:
                    leftover_frames.append(frame)
            if leftover_frames:
                best_frame = convert_video_to_one_best_frame_per_minute(leftover_frames)
                best_frames.append(best_frame)
                frame_path = os.path.join(date_folder_path, f"frame_{frame_count}.png")
                plt.imshow(cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB))
                plt.axis('off')
                plt.savefig(frame_path, bbox_inches='tight', pad_inches=0)
                print(f"Saved leftover frame {frame_count} at {frame_path}")
                frame_count += 1
        cap.release()
        all_selected_frames.extend(best_frames)
    print(f"Frames saved successfully in folder: {output_folder}")
    return output_folder




# -----------------------------------draw 20*20 grids with index --------------------------------
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





# -----------------------------------------------------------------Display frame with grids-----------
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
    frame_with_grids = apply_grids(frame, grid_size)        #USE HELPTING FUNCTION TO CALL AND APPLY GRIDS 
    output_path = os.path.join(os.getcwd(), 'output_frame_with_grids.png')
    try:
        cv2.imwrite(output_path, frame_with_grids)
        cap.release()
        return output_path
    except Exception as e:
        print(f"Error saving the frame: {e}")
        return None




# ---------------------extract only first video to varify thhat the selected vidoe is same----------------------------------------------------------------
def get_first_video(folder_path, valid_extensions=(".dav", ".mp4", ".avi", ".mkv")):
    files = [f for f in os.listdir(folder_path) if f.endswith(valid_extensions)]
    if not files:
        print("No video files found in the folder.")
        return None
    first_video = sorted(files)[0]
    return os.path.join(folder_path, first_video)



# ---------------------extract date from video path  and save paths in a directory ----------------------------------------------------------------
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



#----------------------------------------------------------------Extract frame from fram a video to show -----
def extract_frame(video_path, output_image_path):
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return False
    success, frame = video_capture.read()
    if success:
        cv2.imwrite(output_image_path, frame)
        video_capture.release()
        return True
    else:
        video_capture.release()
        return False

# **************************************************************

# Main Functions


# **************************************************************




#----   1 Step:

# -----------------------------Loading page to load all the things properly --------------------------------
def loading_view(request):
    return render(request, 'HtmlFiles/loading.html')

#    2 Step:
# -----------------------------  Any one can accesss this main page  --------------------------------
def main(request):
    success = False
    error = False
    ip_address = request.META.get('REMOTE_ADDR')
    visitor_name = f"Visitor IP Adress {ip_address}"
    Visitor.objects.create(name=visitor_name, visit_time=now())
    visitors = Visitor.objects.values('name').annotate(
        count=Count('name'),
        latest_visit_time=Max('visit_time')
    ).order_by('latest_visit_time')
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    subject,  
                    message,  
                    email,   
                    ['recipient@example.com'], 
                    fail_silently=False,
                )
                success = True 
            except Exception as e:
                error = True 
        else:
            error = True 
    else:
        form = ContactForm()
    context = {
        'form': form,
        'success': success,
        'error': error,
        "count": 2,
        "time": "kahdsl",
        "url_": "/home/", 
        "link_text": "Home",
         'visitors': visitors,
    }
    return render(request, 'HtmlFiles/main.html', context)


#     3 Step:

# -----------------------------Login / logout--------------------------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            messages.success(request, f"You logged in as {username}")
            return redirect('categories')                                        # -------------------------Redirecting to categories page 
        else:
            messages.error(request, "Incorrect Username or password")
    return render(request, 'HtmlFiles/login.html')
def logoutUser(request):
    logout(request)
    return redirect(reverse('main')) 


#        4 Step:
# ------------------------------Categories Section  ------------------------------
def categories(request):
    if request.user.is_anonymous:
        return redirect("/login")  
    url_ = "/categories/"  
    link_text = "Categories"
    categories_list = Categories.objects.all()        #retrive all categories from data base 
    context = {
        'categories': categories_list,
        'url_': url_,
        'link_text': link_text, 
    }

    return render(request, 'HtmlFiles/categories.html', context)

#     5  Step:


# ------------------------------Chuse people / cheff category for preprocessing   ------------------------------
def cheff_and_people(request):
    url_ = "/categories/"  
    link_text = "Categories"
    context = {
        'url_': url_,
        'link_text': link_text, 
    }
    return render(request, 'HtmlFiles/Cheff&people.html',context)



#     6  Step:
#----------------------------------------------------------------Cheff Preprocessing   ----------------------------------------------------------------
def chef_preprocessing(request):
    url_ = "/categories/"
    link_text = "Categories"
    chef_videos_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'chef_videos')   # Path to the chef_videos directory and the video_paths.txt file
    video_paths_file = os.path.join(chef_videos_path, 'video_paths.txt')
    if request.method == "POST" and request.FILES.get('Kitchenvideos'):
        video_files = request.FILES.getlist('Kitchenvideos')
        if os.path.exists(chef_videos_path):                                                             
            for f in os.listdir(chef_videos_path):     # Delete all existing files in the directory
                file_path = os.path.join(chef_videos_path, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        if os.path.exists(video_paths_file):
            os.remove(video_paths_file)
        os.makedirs(chef_videos_path, exist_ok=True)
        video_urls = []
        for video_file in video_files:
            fs = FileSystemStorage(location=chef_videos_path)
            filename = fs.save(video_file.name, video_file)
            video_url = fs.url(filename)             # Get the URL of the saved video file
            video_urls.append(video_url)
            with open(video_paths_file, 'a') as file:
                file.write(f"{video_url}\n")
        context = {
            'url_': url_,
            'link_text': link_text,
            'is_uploaded': True,
            'video_urls': video_urls
        }
    else:
        context = {
            'url_': url_,
            'link_text': link_text,
            'is_uploaded': False
        }

    return render(request, 'HtmlFiles/chef_preprocessing.html', context)



#     7  Step:


# ------------------------------Not finalized in progress    ------------------------------
def final_chef_preprocessing1(request):
    url_ = "/categories/"
    link_text = "Categories"
    chef_videos_folder = os.path.join(settings.MEDIA_ROOT, 'videos', 'chef_videos')      # Path to the chef_videos folder inside media
    valid_video_extensions = ['.mp4', '.avi', '.mov', '.dav']
    video_files = [f for f in os.listdir(chef_videos_folder)
                   if os.path.isfile(os.path.join(chef_videos_folder, f)) and 
                   any(f.lower().endswith(ext) for ext in valid_video_extensions)]
    if not video_files:
        frame_image = None
    else:
        video_filename = video_files[0]
        video_path = os.path.join(chef_videos_folder, video_filename)
        frame_folder = os.path.join(settings.MEDIA_ROOT, 'frames')
        os.makedirs(frame_folder, exist_ok=True)
        frame_image_path = os.path.join(frame_folder, 'extracted_frame.jpg')
        if extract_frame(video_path, frame_image_path):
            frame_image = f"/media/frames/{os.path.basename(frame_image_path)}"
        else:
            frame_image = None

    context = {
        'url_': url_,
        'link_text': link_text,
        'frame_image': frame_image, 
    }
    return render(request, 'HtmlFiles/finalCheffPreprocessing1.html', context)

# step 8
def final_chef_preprocessing2(request):
    url_ = "/categories/"
    link_text = "Categories"
    context = {
            'url_': url_,
            'link_text': link_text,
            'is_uploaded': False
        }
    return render(request, 'HtmlFiles/finalCheffPreprocessing2.html',context )



#   step 9 

# ------------------------------Select Vidoes  (upload  people vidoes ) ------------------------------
def select_video(request):
    is_uploaded = False
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
        videos = request.FILES.getlist('videos')
        for filename in os.listdir(video_folder):
            file_path = os.path.join(video_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
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
    return render(request, 'HtmlFiles/Add_Video.html', {
        'video_paths': video_paths,
        'is_uploaded': is_uploaded,
        'video_urls': video_urls,
        'url_': url_,
        'link_text': link_text,
    })


#  step 10
#  ----------------------  Preprocesing    get frame of first vidoe and display it with grids --------------------
def preprocessing(request):
    url_ = "/categories/"  
    link_text = "Categories"
    if request.method == 'POST':
        video_folder = os.path.join(os.getcwd(), 'media', 'videos', 'uploaded_videos')
        raw_folder = get_first_video(video_folder)
        if not raw_folder or not os.path.isfile(raw_folder):
            return render(request, 'HtmlFiles/preprocessing.html', {'frame_rgb': None,"url_": url_, "link_text": link_text,})
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


#  step 11 
# ---------------Save grids nuebrs ----------------------------------------------
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


# step 12 
#----------------------------------------------------------------Triger the main preprocesing view --------------------------------
def start_preprocessing(request):
    if request.method == "POST":
        preprocessing = True
        preprocessing_2(request) 
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




# step 13
#-----------------  Main Preprocesing fnctions --------------------------------
def preprocessing_2(request):
    date_file_path = os.path.abspath("date_record.txt")
    url_ = "/categories/"
    link_text = "Categories"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    raw_folder = r"D:\FYP - Copy\preprocessing\Video Preprocessing\New folder"
    video_dict, formatted_date = get_video_paths_by_time(raw_folder)
    if not video_dict:
        return
    output_folder=process_all_videos_and_save_frames(list(video_dict.values()))    # call to convert video to frame 
    with open("output_path.txt", "r") as file: 
        saved_path = file.read().strip()
    output_folder=process_images(saved_path)
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()
    grids_folder = os.path.join(os.getcwd(), 'media', 'videos')
    grids_file_path = os.path.join(grids_folder, 'grids.txt')      #get save grids 
    with open(grids_file_path, 'r') as file:
        grids_data_str = file.read().strip()
    grids_data_str = grids_data_str.strip("'")
    grids_data = ast.literal_eval(grids_data_str)
    grid_numbers = [int(num) for num in grids_data]
    output_folder=create_cropped_grid_video(saved_path, grid_numbers=grid_numbers)   # use that grids to crop the video 
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()

    output_folder=process_images(saved_path)      #enhance the frames 
    with open("output_path.txt", "r") as file:
        saved_path = file.read().strip()
    input_folder = "20241126_enhancement1_cropped_enhancement1"
    preprocessed_folder = os.path.join(os.getcwd(), 'media', 'preprocessed')
    if os.path.exists(preprocessed_folder):
        shutil.rmtree(preprocessed_folder)                  # Deletes the entire folder and its contents
    os.makedirs(preprocessed_folder, exist_ok=True)
    process_folder(input_folder, preprocessed_folder)


    # ------------------Save the data in Tables ----------------------------------------------------
    json_file_path = os.path.abspath("20241126_enhancement1_cropped_enhancement1.json")
    image_folder = os.path.abspath("20241126_enhancement1_cropped_enhancement1_food")

    if os.path.exists(json_file_path):   #read the json file that made after applying model
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        match = re.search(r"(\d{8})", os.path.basename(json_file_path))
        if match:
            date_str = match.group(1)
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"    #store the date in a formate of date time 
        with open(date_file_path, "w") as date_file:
            date_file.write(formatted_date)
        if os.path.exists(date_file_path):
            with open(date_file_path, "r") as date_file:
                saved_date = date_file.read().strip()

        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for key, value in data.items():
            table_number = int(key)
            time_before_meal_value = value.get("time_before_meal", 0.0)
            total_time = value.get("total_time", 0.0)
            total_people = value.get("total_people", 0.0)
                                                                 #Store customer waiting time for meal 
            order = CustomerOrderWaitingTime.objects.create(
                table_number=table_number,
                total_time=total_time,
                total_people=total_people,
                time_before_meal=time_before_meal_value,
                date=saved_date
            )

            if image_files:
                random_image = random.choice(image_files)
                image_path = os.path.join(image_folder, random_image)
                with open(image_path, "rb") as img_file:
                    order.visual_representation.save(random_image, File(img_file))  #for feature selection of image storage 
            order.save()
        total_people = 0
        people_per_hour = {}
        meals = {}
    for table_id, details in data.items():
        table_number = int(table_id)
        total_people += details.get("total_people", 0)

        for hour, count in details.get("total_people_per_hour", {}).items():
            people_per_hour[hour] = people_per_hour.get(hour, 0) + count   #get all the people per hours for entire day 

        for meal, count in details.get("meal", {}).items():
            meals[meal] = meals.get(meal, 0) + count    #get all the meal   for entire day 


    image_path = None
    if os.path.exists(image_folder):
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        selected_image = next((img for img in image_files if f"best_food_output_{date_str}.jpg" in img), None) #for feature selection of image storage 
        if not selected_image and image_files:
            selected_image = random.choice(image_files)
        if selected_image:
            image_path = os.path.join(image_folder, selected_image)
 #Store General Analytics
    order_summary = CustomerOrderSummary.objects.create(
        table_number=table_number,
        total_people=total_people,   #total people in entire day
        people_per_hour=people_per_hour,   #total people according to hour in entire day
        meals=meals,   #total meal  in entire day
        date=formatted_date
    )

    if image_path:
        with open(image_path, "rb") as img_file:
            order_summary.meal_image.save(random_image, File(img_file))


        
    context = {
        'title': 'Preprocessing Completed - Congratulations!',
        'preprocessing': True,
        'url_': url_,
        'link_text': link_text,
    }
    return render(request, 'HtmlFiles/preprocessing_2.html', context)

# step 14

#------------  Function to show General  Informations --------------------------------
def analytics_review(request):
    url_ = "/categories/"  
    link_text = "Categories"
    context = {
        'url_': url_,
        'link_text': link_text, 
         'active_page': 'Visualization',
        "top_dishes": [
            {"name": "Pizza", "count": 300},
             {"name": "Pizza", "count": 300},
              {"name": "Piza", "count": 300},
               {"name": "Pia", "count": 300},
                {"name": "Pizza", "count": 300},
                 {"name": "Pizza", "count": 300},
                  {"name": "Pizza", "count": 300},
                   {"name": "Pizza", "count": 300},

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


# step 15 

#----function to show how many time a customer ait for fod --------------------------------
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
    waiting_times = CustomerOrderWaitingTime.objects.all()

    # Group data by date
    data_by_date = defaultdict(lambda: {"waiting_times_before_meal": [], "total_times": []})
    available_dates = set()  # Store available dates

    for time in waiting_times:
        date_str = time.date.strftime("%Y-%m-%d")
        available_dates.add(date_str)
        data_by_date[date_str]["waiting_times_before_meal"].append(time.time_before_meal)
        data_by_date[date_str]["total_times"].append(time.total_time)

    # Convert to JSON-friendly format
    grouped_data = [{"date": date, "data": data} for date, data in data_by_date.items()]
    grouped_data_json = json.dumps(grouped_data)  # Convert to JSON

    # Handle selected date filtering
    selected_date = request.GET.get("date")
    filtered_data = next((entry for entry in grouped_data if entry["date"] == selected_date), None)

    context = {
        "grouped_data": grouped_data_json,  # JSON Data
        "available_dates": sorted(available_dates),  # All Dates
        "selected_date": selected_date,  # Current Selected Date
        "active_page": "Visualization",
    }
    return render(request, "HtmlFiles/customer_waiting_time_for_order_Visualization.html", context)


#-------------TO be used later  --------------------------------
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

 