from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from internshala_scraper import InternShalaScraper
from credentials import internshala_credentials
from . import tasks
from .models import AppliedJobs
from .serializers import AppliedJobsSerializer,ApplyJobSerializer
internshala_bot = None

def get_scraper():
    global internshala_bot
    if internshala_bot is None:
        username = internshala_credentials['email']
        password = internshala_credentials['password']
        token = internshala_credentials['token']
        internshala_bot = InternShalaScraper(username=username, password=password,gimini_token =token,save_cookie=True)
    return internshala_bot

class GetMatchingJobsView(APIView):
    def get(self, request):
        bot=get_scraper()
    
        jobs_list=bot.get_maching_jobs()
        if jobs_list:
            return Response({"response":jobs_list,"error":""}, status=status.HTTP_200_OK)
        return Response({"response":[],"message":"eroor"}, status=status.HTTP_200_OK)

class SearchQueryView(APIView):
    def get(self, request, query):
        if not query:
            return Response({"message": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        bot=get_scraper()
        jobs_list=bot.search_internship_or_job(query=query)
        if jobs_list:
            return Response({
                "response": jobs_list,
                "error":"error"
            }, status=status.HTTP_200_OK)
        
        return Response({"response":[],"message":"eroor"}, status=status.HTTP_200_OK)
class ApplyJobsView(APIView):
    
    def post(self, request):
        serializer = ApplyJobSerializer(data=request.data, many=True)

        if serializer.is_valid():
            job_data = serializer.validated_data
            print("Received jobs to apply:", job_data)

            task=tasks.apply_jobs_in_background.delay(internshala_credentials['email'],internshala_credentials['password'],internshala_credentials['token'],job_data)
            return Response({"message": "jobs applying proroccess is started","task_id":task.task_id,"status":task.status}, status=status.HTTP_202_ACCEPTED)
            # print(serializer.validated_data)
            # return Response({'messge':'parsial data'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppliedJobsView(viewsets.ReadOnlyModelViewSet):
    queryset = AppliedJobs.objects.all()
    serializer_class = AppliedJobsSerializer
