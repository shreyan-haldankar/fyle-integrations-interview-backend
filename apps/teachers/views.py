from xml.dom import ValidationErr
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from apps.teachers.serializers import TeacherAssignmentSerializer

from .models import Teacher

from apps.students.models import Assignment, Student, GRADE_CHOICES
# Create your views here.

# class DraftError():
#     pass

class TeacherAssignmentView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id
        
        # Add this somewhere
        # if assignment.state != "DRAFT":
        

        try:
            assignment = Assignment.objects.get(pk=request.data['id'], teacher__user = request.user)
            if 'grade' in request.data:
                if request.data['grade'] in GRADE_CHOICES:
                    if assignment.state == 'SUBMITTED':
                        assignment.state = "GRADED"
            # if assignment.state == "DRAFT":
            #     raise DraftError
            # if assignment.state == "GRADED":
            #     raise AssertionError
        except Assignment.DoesNotExist:
            return Response(
                data = {'error': 'Assignment does not exist/ permission denied'},
                status = status.HTTP_400_BAD_REQUEST
        
            )
        except Assignment.DraftError(assignment):
            return Response(
                data = {'error': "SUBMITTED assignments can only be graded"},
                status = status.HTTP_400_BAD_REQUEST
            )

            
        # except AssertionError:
        #     return Response(
        #         data = {"SUBMITTED assignments can only be graded"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # except assignment.state == "DRAFT":
        #     return Response(
        #         data = {'error': "SUBMITTED assignments can only be graded"},
        #         status = status.HTTP_400_BAD_REQUEST
        #     )

        serializer = self.serializer_class(assignment, data = request.data, partial = True)

        # if assignment.state == "DRAFT" or assignment.state == "GRADED":
        #     # print(assignment.state)
        #     state = assignment.state
        #     raise serializer._errors(serializer,state)    
            
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data = serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )