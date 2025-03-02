from django.db import models

# Create your models here.
class GeneratedValue(models.Model):
    conan_id = models.CharField(max_length=100, null=True, blank=True)  # Nullable field for Conan ID
    description = models.TextField(null=True, blank=True)                # Nullable field for description
    some_text = models.CharField(max_length=255, null=True, blank=True)  # Nullable field for some text
    image = models.ImageField(upload_to='images/', null=True, blank=True) # Nullable field to store images

    def __str__(self):
        return self.conan_id if self.conan_id else "No Conan ID"
class Categories(models.Model): 

    conan_id = models.CharField(max_length=100, null=True, blank=True) 
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)  
    description = models.TextField(null=True, blank=True)               
    some_text = models.CharField(max_length=255, null=True, blank=True)  
    URL= models.CharField(max_length=255, null=True, blank=True)  
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)                
    updated_at = models.DateTimeField(auto_now=True)                    

    def __str__(self):
        return self.name if self.name else "No Name"  
class CustomerOrderWaitingTime(models.Model):
    table_number = models.IntegerField(null=True, blank=True)
    time_before_meal = models.FloatField(default=0.0)
    total_time = models.FloatField(default=0.0)
    total_people=models.FloatField(default=0.0)
    date = models.DateField()
    visual_representation = models.ImageField(upload_to="order_images/", null=True, blank=True)  

    def __str__(self):
        return f"Table {self.table_number} - {self.date}"
class CustomerOrderSummary(models.Model):
    table_number = models.IntegerField()
    total_people = models.IntegerField()
    people_per_hour = models.JSONField(default=dict)  # Stores per-hour people count
    meals = models.JSONField(default=dict)  # Stores meal counts
    date = models.DateField()
    meal_image = models.ImageField(upload_to="meal_images/", null=True, blank=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.date}"



class Visitor(models.Model):
    name = models.CharField(max_length=100)  
    visit_time = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class CustomerOrderServingTime(models.Model):
    table_number = models.IntegerField(null=True, blank=True) 
    start_time = models.DateTimeField()  # When the order is confirmed
    end_time = models.DateTimeField()    # When the order is served to the customer
    date = models.DateField(auto_now_add=True)  # Automatically set to now when created
    looks_of_food = models.TextField()  # Description of the food's appearance
    visual_representation = models.ImageField(upload_to='images/serving_time/', blank=True, null=True)  # Only image

    def __str__(self):
        return f"Order served from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} on {self.date}"