# Create your views here.
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
# rest api to read file and save it
from rest_framework.views import APIView
from api.mapper.algos.harmonizationWithSuggestionService import SampleBasedHarmonizationService
import pandas as pd
from api.mapper.models import File
from api import settings


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)

    def post(self, request, format=None):
        file_obj1 = request.FILES['file1']
        file1 = File(file=file_obj1)

        file_obj2 = request.FILES['file2']
        file2 = File(file=file_obj2)
        option = request.data['option']
        output = File.merge(file1, file2, option)
        # print("Output", output)
        return Response(output)
    
class SampleBasedHarmonization(APIView):
    def post(self, request, format=None):
        file_obj1 = request.FILES['file1']
        file1 = File(file=file_obj1)
        file_field1=file1.file
        data1 = pd.read_csv(file_field1)
        file_obj2 = request.FILES['file2']
        file2 = File(file=file_obj2)
        file_field2=file2.file
        data2 = pd.read_csv(file_field2)
        file_obj3 = request.FILES['sample']
        sample_data = File(file=file_obj3)
        sample_file_field=sample_data.file
        sample = pd.read_csv(sample_file_field)

        output= SampleBasedHarmonizationService(settings.OPENAI_KEY).invoke(sample,data1,data2)
        return Response(output)
