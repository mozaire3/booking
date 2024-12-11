from django.shortcuts import get_object_or_404
import datetime,jwt
from rest_framework.response import Response
from rest_framework import  status,generics
from .serializer import UserSerializer, HotelsSerializer, RoomsSerializer,PayemntSerializer
from .models import PayementModel, UserModel,HotelModel,RoomsModel
import requests




class Users(generics.GenericAPIView):
    serializer_class = UserSerializer
    def get(self,request):
        try:
            user = UserModel.objects.all()
            serializer = UserSerializer(user,many=True)
            return Response(serializer.data)
        except:
            return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    def post(self,request):
        email = request.data['email']
        user = UserModel.objects.filter(email=email).first()
        if user:
           return Response({"error":"user already exists"},status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
class User(generics.GenericAPIView):
    
    serializer_class = UserSerializer 
    def get(self,request, pk):
        # user = get_object_or_404(UserModel, pk=pk)
        user = UserModel.objects.filter(pk=pk).first()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
    def patch(self,request, pk):
        print(request.data)
        user = get_object_or_404(UserModel, pk=pk) 
       
        print(user)
        serializer = UserSerializer(instance=user, data=request.data)
        print("arrive")
        # return Response({"test","alex test"},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
 
    def delete(self,request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        if user:
            try:
                user.delete()
                return Response({"succes":"deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"error":"unable to delete"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error":"user don't exist"},status=status.HTTP_400_BAD_REQUEST)


class Register(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self,request):
        email = request.data['email']
        user = UserModel.objects.filter(email=email).first()
        if user:
           return Response({"error":"user already exists"},status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Login(generics.GenericAPIView):
    serializer_class = UserSerializer 
    def post(self,request):
        print(request.data['email'])
        email = request.data['email']
        password = request.data['password']     
        user = UserModel.objects.filter(email=email).first()
        serializer = UserSerializer(user, many=False)
        
        if user is None:
            return Response({"error":"user not found"},status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({"error":"Incorrect password"},status.HTTP_400_BAD_REQUEST)
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat':datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload,'secret',algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            "jwt":token,
            "user":serializer.data
        }
        
        return response
    

    
    
class auth2(generics.GenericAPIView):
    serializer_class = UserSerializer 
    def post(self,request):
        
        email = request.data['email']
        # send_mail(
        #         "Subject here",
        #         "Here is the message.",
        #         "alex-russel.kouawou@epitech.eu",
        #         [email],
        #     fail_silently=False,
        # )
        user = UserModel.objects.filter(email=email).first()
        if user:
            serializer = UserSerializer(user, many=False)
            payload = {
                'id':user.id,
                'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat':datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload,'secret',algorithm='HS256')
            
            response = Response()
            response.set_cookie(key='jwt',value=token, httponly=True)
            response.data = {
                "jwt":token,
                "user":serializer.data
            }
            
            return response
        
        
        
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                
                payload = {
                    'id':serializer.data.id,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat':datetime.datetime.utcnow()
                }
                
                token = jwt.encode(payload,'secret',algorithm='HS256')
                
                response = Response()
                response.set_cookie(key='jwt',value=token, httponly=True)
                response.data = {
                    "jwt":token,
                    "user":serializer.data
                }
                
                
                return response
            except:
                return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
            
            

class Logout(generics.GenericAPIView):
    def post(self,request):
        response =  Response()
        response.delete_cookie('jwt')
        response.data = {
            'logout':'success'
        }
        
        return response
  

##########CRUD COURSE##############
class Hotels(generics.GenericAPIView):
    serializer_class = HotelsSerializer
    def get(self,request):
        course = HotelModel.objects.all()
        if course:
            serializer = HotelsSerializer(course, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        datas = request.data
        titre = datas["titre"]
        desc = datas["description"]
        try:
            translated_titre = requests.post("https://api-ai-fon-translate.vercel.app/create_fon",json = {"texts":titre} )
            translated_desc = requests.post("https://api-ai-fon-translate.vercel.app/create_fon",json = {"texts":desc} )
            translated_titre_json = translated_titre.json()
            translated_desc_json = translated_desc.json()
        except:
            Response({"error":"api error"},status=status.HTTP_400_BAD_REQUEST)
            
        datas["titre_fon"] = translated_titre_json["data"]
        datas['description_fon'] =translated_desc_json["data"] 
        serializer = HotelsSerializer(data = datas)
       
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class Hotel(generics.GenericAPIView):
    serializer_class = HotelsSerializer
    def get(self,request, pk):
        course = get_object_or_404(HotelModel, pk=pk)
        serializer = HotelsSerializer(course, many=False)
        return Response(serializer.data)

    def patch(self,request, pk):
        print("ici",request.data)
        datas = request.data.copy()
        titre = datas["titre"]
        desc = datas["description"]
        
        try:
            translated_titre = requests.post("https://api-ai-fon-translate.vercel.app/create_fon",json = {"texts":titre} )
            translated_desc = requests.post("https://api-ai-fon-translate.vercel.app/create_fon",json = {"texts":desc} )
            translated_titre_json = translated_titre.json()
            translated_desc_json = translated_desc.json()
 
        except:
            Response({"error":"api error"},status=status.HTTP_400_BAD_REQUEST)
       
        datas["titre_fon"] = translated_titre_json ["data"]
        datas['description_fon'] = translated_desc_json ["data"]
        serializer = HotelsSerializer(data = datas)
        course = get_object_or_404(HotelModel, pk=pk)
        
        serializer = HotelsSerializer(instance=course, data=datas)
        print(serializer.initial_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"data":serializer.data,"status":200},status.HTTP_201_CREATED)
            except:
               return Response({"error":"database error","status":500},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors":serializer.errors,"status":401}, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request, pk):
        print(request.data)
        course = get_object_or_404(HotelModel, pk=pk)
        
        serializer = HotelsSerializer(instance=course, data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"data":serializer.data,"status":200},status.HTTP_201_CREATED)
            except:
               return Response({"error":"database error","status":500},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors":serializer.errors,"status":401}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        course = get_object_or_404(HotelModel, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#######################"Payement################
class Payment(generics.GenericAPIView):
    serializer_class = PayemntSerializer
    def get(self,request, pk):
        payement = get_object_or_404(PayementModel, pk=pk)
        serializer = PayemntSerializer(payement, many=False)
        return Response(serializer.data)
    
class Payments(generics.GenericAPIView):
    serializer_class = PayemntSerializer
    def get(self,request):
        payement = PayementModel.objects.all()
        if payement:
            serializer = PayemntSerializer(payement, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        serializer = PayemntSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response({"error":"database error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    







########################CRUD COURSECONTENT #######################
class Rooms(generics.GenericAPIView):
    serializer_class = RoomsSerializer
    def get(self, request):
        content = RoomsModel.objects.all()
        if content:
            serializer = RoomsSerializer(content, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
   
class Room(generics.GenericAPIView):
    def get(self,request, pk):
        content  = get_object_or_404(RoomsModel, pk=pk)
        serializer = RoomsSerializer(content, many=False)
        return Response(serializer.data)

    def put(self,request, pk):
        print(request.data,pk)
        content = get_object_or_404(RoomsModel, pk=pk)
        serializer = RoomsSerializer(instance=content, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data,status.HTTP_201_CREATED)
            except:
                return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        content = get_object_or_404(RoomsSerializer, pk=pk)
        content.delete()
        
#####
class RoomsOne(generics.GenericAPIView):
    serializer_class = RoomsSerializer
    def get(self, request,courseId):
        content = RoomsModel.objects.filter(hotelID=courseId)
        if content:
            serializer = RoomsSerializer(content, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


