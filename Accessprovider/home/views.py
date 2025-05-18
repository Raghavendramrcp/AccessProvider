from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Fyers_Access_Token, Fyers_Auth_Inputs
from .forms import Fyers_Access_TokenForm
# Create your views here.



from fyers_apiv3 import fyersModel



class HomePageView(TemplateView):
    template_name = 'home/homepage.html'


class AccessTokenView(View):

    """ Generate Access Toke with class based view  """

    form_class = Fyers_Access_TokenForm
    template_name = 'home/accesstoken.html'

    def get_queryset(self):
        self.app_inputs = get_object_or_404(
            Fyers_Auth_Inputs, user_ass_id=self.kwargs['pk'])
        return self.app_inputs

    def get(self, request, pk):
        client_id = self.get_queryset().client_id
        secret_key = self.get_queryset().secret_id
        redirect_url = self.get_queryset().redirect_url

        grant_type = "authorization_code"
        response_type = "code"
        state = "sample"

        appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_url,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)

        generateTokenUrl = appSession.generate_authcode()

        form = self.form_class

        return render(request, self.template_name, {'access_form': form, 'response': generateTokenUrl})

    def post(self, request, pk):

        if request.method == 'POST':
            client_id = self.get_queryset().client_id
            secret_key = self.get_queryset().secret_id
            redirect_url = self.get_queryset().redirect_url

            grant_type = "authorization_code"
            response_type = "code"
            state = "sample"

            appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_url,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)

            access_form = Fyers_Access_TokenForm(request.POST)

            if access_form.is_valid():
                user_ass = access_form.cleaned_data.get('app_ass')
                auth_code = access_form.cleaned_data.get('auth_code')

                appSession.set_token(auth_code)

                access_token = appSession.generate_token()["access_token"]

                object = Fyers_Access_Token(
                    app_ass=user_ass, auth_code=access_token)
                object.save()

                return redirect('homepage')

        form = Fyers_Access_TokenForm()
        return render(request, self.template_name, {'access_token': form})

# Deleting Access Token


def delete_auth_code(request, pk):
    """ Delete the Access Token with this function """

    if request.method == 'POST':
        accesstoken = Fyers_Access_Token.objects.filter(app_ass_id=pk)
        accesstoken.delete()
        return redirect('homepage')



@api_view(['GET'])
def fyers_user_details_api(request, pk):
    app_inputs = get_object_or_404(Fyers_Auth_Inputs, user_ass_id=pk)
    access_token_obj = get_object_or_404(Fyers_Access_Token, app_ass_id=pk)

    response_data = {
        'client_id': app_inputs.client_id,
        'access_token': access_token_obj.auth_code,
        'redirect_uri': app_inputs.redirect_url,
    }

    return Response(response_data, status=status.HTTP_200_OK)