from django.shortcuts import redirect
from .serializers import AppSerializer,TaskSubmitSerializer,TaskSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import App,AppCategory,SubCategory,Task,UserProfile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

# I am using messages framework to globally pass the messages.
# This view returns both the home page and the app detail page.
# I am using an id as an argument to be passed in the url to return detail page.

class AppView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id=None,format=None):
        # Here i am making a query to get a particular app.
        if id:
            data=App.objects.get(id=id)
            serializer = AppSerializer(data)
            return Response({"data":serializer.data},template_name="webapp/detail.html")
        
        # Here i am making a query to get all the apps.
        data = App.objects.all()
        serializer = AppSerializer(data,many=True)

        return Response({"data":serializer.data},template_name="webapp/home.html")


# This is the view used to upload the screenshot task, the user will be able to drag and drop screenshot and post the data
class TaskUploadView(LoginRequiredMixin,APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data=request.data
        data_={
            "app":int(data.get("app")),
            "user":int(data.get("user")),
            "image":data.get("image"),
        }
        app=data.get("app")

        # If the user has already uploaded the task and tries to upload it again, They get a message as follows:
        if Task.objects.filter(app=app,user=request.user).exists():
            messages.warning(request,"You have already submitted your screenshot.")
        else:
            serializer = TaskSubmitSerializer(data=data_)
            if serializer.is_valid():
                task = serializer.save()
                task.is_completed = True 
                task.save()
                messages.success(request,"You have successfully completed your task.")
            else:
                messages.warning(request,f"Error - {serializer.errors}")
        return redirect("applications")
        print(data)
        return redirect("applications")

# It is a simple profile view where user can see their username and tasks completed.
class ProfileView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id,format=None):
        
        profile=UserProfile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        return Response({"profile":serializer.data}, template_name="webapp/profile.html")

# This is the Point list view. It will show all the points that a particular user has earned  
class UserPointsView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id,format=None):

        # userApps = Task.objects.values("id","image",username="user__username",app_points="app__points",app_name="app__app_name").filter(user=user_id).select_related("app","user")
        userApps = Task.objects.filter(is_completed=True,user=request.user).select_related("app","user")
        
        # I am aggregating the sum of all the points
        points = userApps.aggregate(sum=Sum("app__points"))

        serializer = TaskSerializer(userApps,many=True)        
        return Response({"data":serializer.data, "points":points['sum']},template_name = "webapp/points.html")
    

# This is the Task list view. It will show all the tasks that a particular user has completed     
class UserTaskView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self,request,format=None):
        tasks = Task.objects.filter(is_completed=True,user=self.request.user).select_related("app","user")
        print(tasks)
        # I am aggregating the sum of all the points
        points = tasks.aggregate(sum=Sum("app__points"))

        serializer = TaskSerializer(tasks,many=True)
        return Response({"data":serializer.data,"points":points["sum"]},template_name = "webapp/tasks.html")





# Admin panel. This view will be responsible to upload new application and its point. 
class AdminPanel(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self,request,format=None):

        subcategories = {key:value for (key,value) in SubCategory}
        appcategory = {key:value for (key,value) in AppCategory}
        
        return Response({"subcategory":subcategories, "appcategory":appcategory},template_name="webapp/admin/admin.html")
    
    def post(self,request,format=None):
        data = request.data
        serializer = AppSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request,"App successfully added")
        else:
            messages.success(request,f"Error - {serializer.errors}")
        return redirect("/")