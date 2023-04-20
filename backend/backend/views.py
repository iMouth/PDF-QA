from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .pdfparser.controller import main, get_message, get_anwser

@api_view(['GET'])
def question(request):
    question = request.query_params.get('question', None)
    print("Got request: ", request.query_params)
    print("Got question: ", question)
    if question:
        context = get_message(question)
        answer = get_anwser(context)
        return Response({'answer': "A: " + answer}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def set_file(request):
    print("Got request: ", request)
    try: 
        f = request.FILES['file']
        main(f)
    except Exception as e:
        print(e)
        f = None
    print("Got file: ", f)
    if f:
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
