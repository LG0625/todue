from django.shortcuts import redirect, render
from django.conf import settings
from urllib.parse import urlencode
from .models import Assignment, Exam

def add_to_google_calendar(request, event_type, event_id):
    if event_type == 'assignment':
        event = Assignment.objects.get(id=event_id)
    elif event_type == 'exam':
        event = Exam.objects.get(id=event_id)
    else:
        return render(request, 'error.html', {'error': 'Invalid event type'})

    # Create URL for Google Calendar event creation
    url = 'https://calendar.google.com/calendar/r/eventedit'
    params = {
        'text': event.title,
        'details': event.description,
        'location': '',  # Optional
        'st': event.due_date.isoformat(),  # Convert to ISO format
        'et': event.due_date.isoformat(),  # Convert to ISO format
        'sf': 'true',  # Allow edit on creation
    }
    if event.due_time:
        params['st'] += 'T' + event.due_time.isoformat()
        params['et'] += 'T' + event.due_time.isoformat()
    url += '?' + urlencode(params)

    # Redirect user to Google Calendar event creation page
    return redirect(url)
