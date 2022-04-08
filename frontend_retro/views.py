from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_backend.models import Pager, PrivateMessage

from .forms import PrivateMessageForm


def home(request):
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            subscriber_number = form.cleaned_data['subscriber_number']
            message = form.cleaned_data['message']

            try:
                pager = Pager.objects.get(subscriber_number=subscriber_number)
                PrivateMessage.objects.create(pager=pager, message=message)
            except Pager.DoesNotExist:
                pass

            return HttpResponseRedirect('/retropanel/')

    else:
        form = PrivateMessageForm()

    return render(request, 'frontend_retro/index.html', {'form': form})
