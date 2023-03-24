import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .generate_report import generate_report

@csrf_exempt
def generate_report_view(request):
    if request.method == 'POST':
        # Get the JSON data from the request
        json_data = request.body.decode('utf-8')
        student_data = json.loads(json_data)

        # Generate the PDF report using the report generator
        pdf = generate_report(student_data)

        # Send the PDF report back as a response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pdf.output(response, 'F')

        return response
    else:
        return HttpResponse('Invalid request method.')