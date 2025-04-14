from django.db import models

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
    people_per_hour = models.JSONField(default=dict) 
    meals = models.JSONField(default=dict)
    date = models.DateField()
    meal_image = models.ImageField(upload_to="meal_images/", null=True, blank=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.date}"


class DressCodeEntry(models.Model):
    date_key = models.CharField(max_length=20, unique=True) 
    data = models.JSONField()
    def __str__(self):
        return f"Dress Code Entry for {self.date_key}"
    
class TableCleanliness(models.Model):
    date = models.DateField(unique=True) 
    data = models.JSONField(default=dict) 

    def __str__(self):
        return f"{self.date} - {self.data}"

class CustomerOrderServingTime(models.Model):
    table_number = models.IntegerField(null=True, blank=True) 
    start_time = models.DateTimeField()  
    end_time = models.DateTimeField()    
    date = models.DateField(auto_now_add=True) 
    looks_of_food = models.TextField() 
    visual_representation = models.ImageField(upload_to='images/serving_time/', blank=True, null=True) 

    def __str__(self):
        return f"Order served from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} on {self.date}"