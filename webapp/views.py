from django.shortcuts import render


def home(request):
    return render(request, 'webapp/home.html')

def about(request):
    return render(request, 'webapp/about.html')

def categories(request):
    return render(request, 'webapp/categories.html')

def feedback(request):
    return render(request, 'webapp/feedback.html')

def contact(request):
    return render(request, 'webapp/contact.html')

def privacy_policy(request):
    return render(request, 'webapp/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'webapp/terms_conditions.html')
