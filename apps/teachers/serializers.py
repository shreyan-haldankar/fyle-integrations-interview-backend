from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment
from rest_framework import generics, status
from rest_framework.response import Response

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    # Teacher Assignment Serializer
    class Meta:
        model = Assignment
        fields = '__all__'
    
    def validate(self, attrs):
        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')

        if 'student' in attrs and attrs['student']:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')
        
        id = attrs['id']

        if self.state == "DRAFT":
            raise serializers.ValidationError("SUBMITTED assignments can only be graded")
        elif self.state == "GRADED":
            raise serializers.ValidationError("GRADED assignments cannot be graded again")
        # assignment 

    #     if 'id' in attrs and attrs['id']:
    #         assignment = Assignment.objects.get(pk='id')
            
    # #         if assignment.state == "DRAFT":
    #             raise serializers.ValidationError("SUBMITTED assignments can only be graded")
    #         elif assignment.state == "GRADED":
    #             raise serializers.ValidationError("GRADED assignments cannot be graded again")
    # # if 'state' in attrs and attrs
        # if 'grade' in attrs:
        #     if attrs['state'] == 'SUBMITTED':
        
        

        if self.partial:
            return attrs
    
        return super().validate(attrs)

    # def _errors(self,serializer,state):
    #     if state == "DRAFT":
    #         raise serializers.ValidationError("SUBMITTED assignments can only be graded")
    #     elif state == "GRADED":
    #         raise serializers.ValidationError("GRADED assignments cannot be graded again")
    #     return Response(
    #             data= serializer.data,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )