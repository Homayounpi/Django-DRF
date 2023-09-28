from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.renderers import JSONRenderer

# class Home(APIView):
#     def get(self, request):
#         name = request.query_params['name']
#         return Response({'name': name})
#     def post(self, request):
#         name = request.data['name']
#         return Response({'name': name})


class Home(APIView):
    permission_classes = [IsAuthenticated, ]
    # throttle_classes = [AnonRateThrottle, ]

    def get(self, request):

        person = Person.objects.all()
        ser_data = PersonSerializer(instance=person, many=True)
        return Response(data=ser_data.data)


class QuestionListView(APIView):
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_scope = 'questions'
    renderer_classes = [JSONRenderer]

    def get(self, request):

        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """
        create new questions
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = QuestionSerializer

    def post(self, request):
        srz_data = QuestionSerializer(data=request.POST)
        # srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        srz_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request,question)
        question.delete()
        return Response({'message': 'question delete'}, status=status.HTTP_200_OK)

