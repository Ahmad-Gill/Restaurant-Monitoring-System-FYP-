from django.shortcuts import render



# main page
def main(request):
    context={
        "count":2,
        "time":"kahdsl",
    }
    return render(request, "HtmlFiles/main.html",context)

# Categories Section
def categories(request):
    return render(request, 'HtmlFiles/categories.html')
