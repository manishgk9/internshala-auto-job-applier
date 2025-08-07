from rest_framework import serializers
from .models import AppliedJobs

class AppliedJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJobs
        fields = '__all__'



class ApplyJobSerializer(serializers.Serializer):
    job_id = serializers.CharField(max_length=100)
    job_title = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255)
    url=serializers.CharField(max_length=355)