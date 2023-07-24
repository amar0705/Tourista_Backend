# your_app/views.py
import datetime
import jwt
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .authentication import GetMethodTokenAuthentication
from .models import BlogPost, Host, Property, RevokedToken, State, City, PropertyType, Guest
from .serializers import YourModelSerializer, HostSerializer, PropertySerializer, GuestSerializer
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from django.core.paginator import Paginator




class YourModelAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = BlogPost.objects.all()
        serializer = YourModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YourModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class HostAPIView(APIView):
    authentication_classes = [GetMethodTokenAuthentication]  # Use custom authentication for GET requests only
    permission_classes = []  # Add other permissions as needed

    def get(self, request):
        queryset = Host.objects.all()
        serializer = HostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully Added"}, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):

    def create_token_response(self, data):
        payload = {
            'id': data.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response({'token': token}, status=200)
        response['Authorization'] = token
        response.data = {
            'token': token,
            'user_id': data.id
        }
        return response
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user_type = request.data['user_type']
        data = {}
        user = False
        if user_type == 'HOST':
            data = Host.objects.filter(email=email).first()
            user = Host.objects.filter(email=email, password=password).exists()

            if not user:
                raise AuthenticationFailed('Incorrect Email or Password')
            else:
                return self.create_token_response(data)
        else:
            data = Guest.objects.filter(email=email)
            if data:
                value = data.first()
                user = Guest.objects.filter(email=email, password=password).exists()

                if not user:
                    raise AuthenticationFailed('Incorrect Email or Password')
                else:
                    return self.create_token_response(value)
            else:
                raise AuthenticationFailed('Does not exist')


# class HostLoginAPIView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         check_user = Host.objects.filter(email=email, password=password)
#         user = authenticate(username=email, password=password)
#         print(user, check_user.values()[0].get("id"))
#         if check_user.exists():
#             refresh = RefreshToken.for_user(check_user.values()[0])
#             access_token = str(refresh.access_token)
#
#             return Response({'access_token': access_token})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class HostPropertyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, task_id):
        return Property.objects.get(pk=task_id)
    def get(self, request):
        auth_header = get_authorization_header(request).split()

        # if not auth_header or auth_header[0].lower() != b'Bearer':
        #     return Response({'error': 'Invalid Authorization header'}, status=401)

        token = auth_header[0].decode('utf-8')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        property = Property.objects.all().filter(host=payload['id'])
        arrayData = []
        for i in property:
            _dict = {
                'id': i.id,
                'property': i.property,
                'host': i.host.id,
                'location': dict(id=i.city.id, city=i.city.city, state_id=i.state.id, state=i.state.state),
                'property_type': dict(id=i.property_type.id, name=i.property_type.name),
                'total_bedrooms': i.total_bedrooms,
                'summary': i.summary,
                'address': i.address,
                'price': i.price,
                'hosted_since': i.hosted_since,
                'created_at': i.created_at,
                'updated_at': i.updated_at
                # Add other fields as needed
            }
            arrayData.append(_dict)
        return Response({"data": arrayData}, status=201)

    def post(self, request):
        auth_header = get_authorization_header(request).split()
        token = auth_header[0].decode('utf-8')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully Added"}, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, task_id):
        auth_header = get_authorization_header(request).split()
        token = auth_header[0].decode('utf-8')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        task = get_object_or_404(Property, pk=task_id)
        serializer = PropertySerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully'})
        return Response(serializer.errors, status=400)

    def delete(self, request, task_id):
        task = self.get_object(task_id)
        task.delete()
        return Response({'message': 'Deleted successfully'}, status=204)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth

        if token:
            # Blacklist the token by adding it to the RevokedToken model
            RevokedToken.objects.create(token=token)

        return Response({'message': 'Logged out successfully'})

class StateAPIView(APIView):

    def get(self, request):

        location = State.objects.all()
        arrayData = []
        for i in location:
            _dict = {
                'id': i.id,
                'state': i.state
                # Add other fields as needed
            }
            arrayData.append(_dict)
        return Response({"data": arrayData}, status=201)

class CityAPIView(APIView):

    def get(self, request):
        state = self.request.query_params.get("state", None)
        location={}
        if state is not None:
            location = City.objects.all().filter(state=state)
        else:
            location = City.objects.all()

        arrayData = []
        for i in location:
            _dict = {
                'id': i.id,
                'city': i.city,
                'state_id': i.state.id,
                'state': i.state.state
                # Add other fields as needed
            }
            arrayData.append(_dict)
        return Response({"data": arrayData}, status=201)


class PropertyTypeAPIView(APIView):

    def get(self, request):
        property = PropertyType.objects.all()
        arrayData = []
        for i in property:
            _dict = {
                'id': i.id,
                'name': i.name
                # Add other fields as needed
            }
            arrayData.append(_dict)
        return Response({"data": arrayData}, status=201)


class GuestAPIView(APIView):
    authentication_classes = [GetMethodTokenAuthentication]  # Use custom authentication for GET requests only
    permission_classes = []  # Add other permissions as needed

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully Registered"}, status=201)
        return Response(serializer.errors, status=400)


class AllPropertiesAPIView(APIView):
    def get(self, request):
        # Get the query parameters from the URL
        property_type = request.query_params.get('property_type')
        city = request.query_params.get('city')
        price = request.query_params.get('price')
        search = request.query_params.get('search')
        sort = request.query_params.get('sort')
        # Start with all objects
        queryset = Property.objects.all()

        # Apply filters if they are present in the URL parameters
        if search:
            queryset = queryset.filter(property__icontains=search)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if city:
            queryset = queryset.filter(city=city)
        if price:
            prices = price.split(',')
            if '0' in prices:
                queryset = queryset.filter(Q(price__lte=500))
            if '1' in prices:
                queryset = queryset.filter(Q(price__gte=501) & Q(price__lte=1200))
            if '2' in prices:
                queryset = queryset.filter(Q(price__gte=1201) & Q(price__lte=2000))
            if '3' in prices:
                queryset = queryset.filter(Q(price__gte=2001))
        if sort == 'PRICE':
            queryset = queryset.order_by('price')
        if sort == 'NAME':
            queryset = queryset.order_by('property')
        if sort == 'CREATED':
            queryset = queryset.order_by('created_at')

        paginator = Paginator(queryset, per_page=3)  # Set the number of items per page
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)

        arrayData = []
        for i in page_obj:
            _dict = {
                'id': i.id,
                'property': i.property,
                'host': i.host.id,
                'location': dict(id=i.city.id, city=i.city.city, state_id=i.state.id, state=i.state.state),
                'property_type': dict(id=i.property_type.id, name=i.property_type.name),
                'total_bedrooms': i.total_bedrooms,
                'summary': i.summary,
                'address': i.address,
                'price': i.price,
                'hosted_since': i.hosted_since,
                'created_at': i.created_at,
                'updated_at': i.updated_at
                # Add other fields as needed
            }
            arrayData.append(_dict)
            # Construct the final paginated response
        response_data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'data': arrayData,
        }
        return Response(response_data)


