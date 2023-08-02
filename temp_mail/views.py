from django.views.generic import ListView
from django.shortcuts import redirect, get_object_or_404, render
from .models import TempMail
from django.views import View
import requests
from django.utils import timezone
from datetime import timedelta
import uuid
from django.http import HttpResponseRedirect

# Create your views here.
class TempMailList(ListView):
    model = TempMail
    template_name = 'temp_mail_list.html'
    context_object_name = 'q'

    def get_queryset(self):

        if self.request.user.is_superuser:
            q = TempMail.objects.all().order_by('-created_at')
            return q
        
        if not self.request.session.get('user'):
            self.request.session['user'] = str(uuid.uuid4())[0:40]
            
        q = TempMail.objects.filter(user=self.request.session.get('user')).order_by('-created_at')
        return q

class TempMessageDetailView(View):
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        message_id = kwargs.get('message_id')
        
        if request.user.is_superuser:
            user_email = get_object_or_404(TempMail, id=id)
        else:
            user_email = get_object_or_404(TempMail, id=id, user=request.session.get('user'))

        obj = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={user_email.get_login()}&domain={user_email.get_domain()}&id={message_id}").json()
        return render(request, 'temp_mail_messages_detail.html', {"object": obj, "user_email": user_email.id })

    def post(self, request, *args, **kwargs):
        filename = request.POST.get("filename")

        id = kwargs.get('id')

        if request.user.is_superuser:
            user_email = get_object_or_404(TempMail, id=id)
        else:
            user_email = get_object_or_404(TempMail, id=id, user=request.session.get('user'))

        message_id = kwargs.get('message_id')
        url = f"https://www.1secmail.com/api/v1/?action=download&login={user_email.get_login()}&domain={user_email.get_domain()}&id={message_id}&file={filename}"
        return HttpResponseRedirect(url)
  
class TempMessagesList(ListView):
    template_name = 'temp_mail_messages_list.html'
    context_object_name = 'q'

    def get_queryset(self):
        id = self.kwargs.get('id')

        if self.request.user.is_superuser:
            user_email = get_object_or_404(TempMail, id=id)
        else:
            user_email = get_object_or_404(TempMail, id=id, user=self.request.session.get('user'))
        
        messages = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={user_email.get_login()}&domain={user_email.get_domain()}").json()
        return messages
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')

        if self.request.user.is_superuser:
            user_email = get_object_or_404(TempMail, id=id)
        else:
            user_email = get_object_or_404(TempMail, id=id, user=self.request.session.get('user'))
        
        context['mail'] = user_email
        return context

class GenerateTempMail(View):
    def get(self, request, *args, **kwargs):
        email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox").json()[0]
        
        if request.user.is_superuser:
            TempMail.objects.create(
                email = email,
                user="1",
                expiration_date = timezone.now() + timedelta(minutes=10)
            )
        else:
            TempMail.objects.create(
                email = email,
                user=request.session.get('user'),
                expiration_date = timezone.now() + timedelta(minutes=10)
            )

        return redirect(to="index")

class Logout(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            del request.session["user"]
        return redirect(to="index")