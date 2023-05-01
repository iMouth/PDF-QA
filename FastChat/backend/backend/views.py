from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .pdfparser.controller import main, get_message, get_anwser
from django.http import StreamingHttpResponse
import requests

@api_view(['GET'])
def question(request):
    question = request.query_params.get('question', None)
    print("Got request: ", request.query_params)
    print("Got question: ", question)
    if question:
        context = get_message(question)
        params = {
            "model": "vicuna-13b-v1.1",  # Replace with your desired model name
            "prompt": context,
            "temperature": 0.5,
            "max_new_tokens": 250,
            "stop": "###",  # You can modify the stop condition if necessary
        }
        response = requests.post("http://FastChat:21002/worker_generate_stream", json=params, stream=True)

        def response_stream():
            for chunk in response.iter_content(chunk_size=None):
                yield chunk

        return StreamingHttpResponse(response_stream())

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def return_message(request):
    question = request.query_params.get('question', None)
    print("Got request: ", request.query_params)
    print("Got question: ", question)
    if question:
        context = get_message(question)
        return Response({"message": context})
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
    
