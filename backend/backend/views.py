from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
# from .models import Question
# from .serializers import QuestionSerializer
from .pdfparser.formatter import main

@api_view(['GET'])
def question(request):
    question = request.query_params.get('question', None)
    print("Got request: ", request.query_params)
    print("Got question: ", question)
    # TODO: Send the question to the model and get the answer
    # For now, just return the question
    if question:
        return Response({'answer': "A: " + question}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def set_file(request):
    print("Got request: ", request)
    try: 
        file = request.FILES['file']
        main(file)
    except:
        file = None
    print("Got file: ", file)
    if file:
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
