from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    
        """
        커스터 마이징한 코드. 주석에 해당하는 코드가 속도 빠름

        # user = User.objects.create_user(
        #     email = validated_data['email'],
        #     nickname = validated_data['nickname'],
        #     name = validated_data['name'],
        #     password = validated_data['password']
        # )

        """
        password = serializers.CharField(write_only=True)
        
        class Meta:
            model = get_user_model()
            fields = ('id', 'email', 'gender', 'password', 'name' )

    