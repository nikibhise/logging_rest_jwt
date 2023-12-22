import logging
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')


class EmployeeAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            success_logger.info("Employee feched successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error("There is an error fetching the employees")
            return Response(data={'detail':"There is an error fetching the posts"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info(f"Employee with id {serializer.data.get('id')} created successfully")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_logger.error(f"Failed to create employee: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            serializer = EmployeeSerializer(employee) 
            success_logger.info(f"Employee details fetched: {serializer.data}")  
            return Response(data=serializer.data, status=status.HTTP_200_OK) 
        except Exception as e:
            error_logger.error(f"There is an error fetching the employees")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                instance=serializer.save()
                success_logger.info(f"Employee updated: {instance}")
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:    
            error_logger.error(f"Failed to update employee {pk}: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                success_logger.info(f"Employee partially updated: {instance}")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e: 
            error_logger.error(f"Failed  to partially update employee {pk}: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk=None):
        try:
            employee = get_object_or_404(Employee, pk=pk)
            employee.delete()
            success_logger.info(f"Employee deleted successfully: {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_logger.error(f"Failed to delete employee")
            return Response(data={'detail': 'Error deleting employee'}, status=status.HTTP_400_BAD_REQUEST)


        

