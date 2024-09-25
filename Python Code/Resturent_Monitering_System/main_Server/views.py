from django.shortcuts import render

def main(request):
    context={
        "count":2,
        "time":"kahdsl",
    }
    return render(request, "HtmlFiles/main.html",context)