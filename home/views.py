from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from API.Parse import *
from .models import UploadedXLSX
import json

def upload(request):
    if request.method == "POST":
        xlsx_file = request.FILES.get("xlsx_file")
        client_ip = request.META.get("REMOTE_ADDR")
        
        # Check if an entry from the same client already exists
        existing_entry = UploadedXLSX.objects.filter(client_ip=client_ip).first()

        if xlsx_file:
            if existing_entry:
                # If an entry already exists, update the xlsx_file field
                existing_entry.xlsx_file = xlsx_file
                existing_entry.save()
            else:
                # If no entry exists, create a new instance of the UploadedXLSX model
                uploaded_xlsx = UploadedXLSX(xlsx_file=xlsx_file, client_ip=client_ip)
                uploaded_xlsx.save()

            # Redirect to a success page or return a response as needed
            return redirect('/result')  # Replace 'success_page' with your success page URL

    # Handle GET requests or display the upload form
    return render(request, "upload_form.html")

def process(request):
    client_ip = request.META.get("REMOTE_ADDR")
    
    # Assuming you want to get the latest UploadedXLSX object for the client's IP
    file = UploadedXLSX.objects.get(client_ip=client_ip)
    
    if file:
        pp = BankStatementProcessor(file.xlsx_file)
    
        pie_data = pp.create_monthly_graph()
    
        # Convert the pie_data JSON to a Python dictionary
        pie_data_dict = json.loads(pie_data)
    
        return JsonResponse(pie_data_dict)  # Return a JSON response
    return JsonResponse({"lol"})

def result(request):
    return render(request, "upload_xlsx.html")


# Create your views here.
def home(request):
    return render(request, "index.html")
