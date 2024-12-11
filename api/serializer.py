from rest_framework import serializers
from .models import UserModel
from .models import HotelModel
from .models import RoomsModel,PayementModel




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = UserModel
        fields=['id','name','email','full_name','role','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self,instance,validated_data):
        print("are we here")
        
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Utilise la méthode Django pour hacher le mot de passe
        instance.save()
        return instance
      
class HotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelModel
        fields = '__all__'
    
        

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomsModel
        fields = '__all__'

class PayemntSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayementModel
        fields = '__all__'
        