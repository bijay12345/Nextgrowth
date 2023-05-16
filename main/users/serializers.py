from users.models import NewUser
from rest_framework import serializers

    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser 
        fields = ["user_name","email","password"]
        
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance