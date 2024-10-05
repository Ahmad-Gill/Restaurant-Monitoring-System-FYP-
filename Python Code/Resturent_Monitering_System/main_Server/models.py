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
    start_time = models.DateTimeField()  # When the customer arrives
    end_time = models.DateTimeField()    # When the waiter comes to take the order
    date = models.DateField(auto_now_add=True)  # Automatically set to now when created
    visual_representation = models.ImageField(upload_to='images/waiting_time/', blank=True, null=True)  # Only image


    def __str__(self):
       return f"Order served from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} on {self.date}"


class CustomerOrderServingTime(models.Model):
    table_number = models.IntegerField(null=True, blank=True) 
    start_time = models.DateTimeField()  # When the order is confirmed
    end_time = models.DateTimeField()    # When the order is served to the customer
    date = models.DateField(auto_now_add=True)  # Automatically set to now when created
    looks_of_food = models.TextField()  # Description of the food's appearance
    visual_representation = models.ImageField(upload_to='images/serving_time/', blank=True, null=True)  # Only image

    def __str__(self):
        return f"Order served from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} on {self.date}"