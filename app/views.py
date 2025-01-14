from django.shortcuts import redirect


def toggle_theme(request):
    if 'light' in request.session['theme']:
        request.session['theme'] = 'dark'
        request.session['toggle'] = 'off'
    else:
        request.session['theme'] = 'light'
        request.session['toggle'] = 'on'
    return redirect('dashboard')