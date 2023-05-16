from rest_framework import serializers
from users.models import NewUser
from .models import App,Task,AppCategory,SubCategory,UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields=["user_name","email"]
    

class AppSerializer(serializers.ModelSerializer):
    app_image = serializers.ImageField(
    allow_null=True,max_length=None, use_url=True
    )
    app_category = serializers.ChoiceField(choices=AppCategory,default="EN")
    sub_category = serializers.ChoiceField(choices=SubCategory,default="SM")

    class Meta:
        model = App 
        fields = "__all__"

    
class TaskSubmitSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
    allow_null=True,max_length=None, use_url=True
    )
    app = serializers.PrimaryKeyRelatedField(queryset=App.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all())

    class Meta:
        model = Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
    allow_null=True,max_length=None, use_url=True
    )
    app=AppSerializer()
    user = UserSerializer()

    class Meta:
        model = Task
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
    allow_null=True,max_length=None, use_url=True
    )
    user = UserSerializer()
    class Meta:
        model = UserProfile  
        fields = "__all__"    
