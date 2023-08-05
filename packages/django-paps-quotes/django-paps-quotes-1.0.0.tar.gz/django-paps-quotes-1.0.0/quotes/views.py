from django.shortcuts import render
from rest_framework.response import Response
from quotes.models import *
from quotes.serializers import *
import requests
from django.conf import settings
# Create your views here.



class PapsquotesView(generics.CreateAPIView):
    permission_classes = (

    )
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    
    def post(self, request, format=None):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            origin = request.POST.get('origin',None)
            destination = request.POST.get('destination',None)
            dimension = request.POST.get('dimension',None)
            url = settings.PAPS_API_URL+""+settings.PAPS_API_KEY+"&?test=true&origin="+origin+"&destination="+destination+"&packageSize="+dimension
            response = requests.request("GET", url)
            datas = response.json()
            if(response.status_code == 200):
                fp = float(datas['data']['quote'])  
                return Response({"message":"les frais de livraison de votre colis allant de "+str(origin)+" à "+str(origin)+" est de : "+str(fp)}, status=200)
            elif(response.status_code == 402):
                return Response({"message":datas['content']}, status=402)
            elif(response.status_code == 400):
                return Response({"message":datas['message']}, status=400)  
        return Response(serializer.errors, status=400)