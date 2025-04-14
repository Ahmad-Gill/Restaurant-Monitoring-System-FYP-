from django.contrib import admin
import markupsafe
from .models import CustomerOrderWaitingTime, CustomerOrderServingTime,CustomerOrderSummary,DressCodeEntry,TableCleanliness
from .models import Categories  

class GeneratedValueAdmin(admin.ModelAdmin):
    # -----------------Register Categories--------------------
    admin.site.register(Categories) 
    admin.site.register(CustomerOrderWaitingTime)
    admin.site.register(CustomerOrderServingTime)
    admin.site.register(CustomerOrderSummary)
    admin.site.register(DressCodeEntry)
    admin.site.register(TableCleanliness)
    