from django.shortcuts import render
from .models import Complaint, ComplaintAssignment, ComplaintCategory
from .serializers import ComplaintSerializer, ComplaintAssignmentSerializer
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics, status
from Categories.models import Category
import time
import cloudinary
import cloudinary.utils

# Mapping from full department display name → department category code
DEPT_NAME_TO_CODE = {
    'Roads & Infrastructure':       'ROADS',
    'Traffic & Road Safety':        'TRAFFIC',
    'Water Supply':                 'WATER',
    'Sewerage & Drainage':          'SEWERAGE',
    'Sanitation & Garbage':         'SANITATION',
    'Street Lighting':              'LIGHTING',
    'Public Health Hazard':         'HEALTH',
    'Parks & Public Spaces':        'PARKS',
    'Stray Animals':                'ANIMALS',
    'Illegal Construction':         'ILLEGAL_CONSTRUCTION',
    'Encroachment':                 'ENCROACHMENT',
    'Public Property Damage':       'PROPERTY_DAMAGE',
    'Noise Pollution':              'NOISE',
    'Electricity & Power Issues':   'ELECTRICITY',
    'Street Vendor / Hawker Issues':'VENDORS',
    'Other':                        'OTHER',
}


import logging
logger = logging.getLogger(__name__)

class CreateComplaintView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("=== CREATE COMPLAINT REQUEST ===")
        print("FILES payload:", request.FILES)
        print("DATA payload:", request.data)
        logger.info(f"Received request.FILES: {request.FILES}")
        try:
            data = request.data.copy()
            cat_val = data.get('Category')

            if cat_val is not None and not str(cat_val).isdigit():
                dept_name = str(cat_val).strip()
                dept_code = DEPT_NAME_TO_CODE.get(dept_name, 'OTHER')

                cc, _ = Category.objects.get_or_create(
                    name=dept_name,
                    defaults={'code': dept_code, 'department': dept_code},
                )
                if cc.code != dept_code or cc.department != dept_code:
                    cc.code = dept_code
                    cc.department = dept_code
                    cc.save(update_fields=['code', 'department'])

                data['Category'] = cc.id

            if 'image_video' in request.FILES:
                data['image_video'] = request.FILES['image_video']

            serializer = ComplaintSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                print("--- VALIDATION SUCCESS, SAVING NOW ---")
                try:
                    complaint = serializer.save()
                    if complaint.image_video:
                        print("--- CLOUDINARY UPLOAD SUCCESS --- URL:", getattr(complaint.image_video, 'url', None))
                    else:
                        print("--- COMPLAINT SAVED WITHOUT IMAGE ---")
                except Exception as save_err:
                    print("--- ERROR DURING DRF SAVE/CLOUDINARY UPLOAD ---", save_err)
                    logger.error(f"Save error: {str(save_err)}", exc_info=True)
                    raise save_err

                return Response({
                    'success': True,
                    'message': 'Complaint Successfully Submitted',
                    'complaint_id': complaint.id,
                    'data': ComplaintSerializer(complaint, context={'request': request}).data
                }, status=status.HTTP_201_CREATED)

            print("--- DRF VALIDATION ERROR ---", serializer.errors)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print("--- CRITICAL API ERROR ---", str(e))
            logger.error(f"Critical error in CreateComplaintView: {str(e)}", exc_info=True)
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CloudinarySignatureView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            timestamp = int(time.time())
            
            params_to_sign = {
                'timestamp': timestamp,
            }
            
            # Using defaults automatically ingested via settings.py cloudinary.config()
            api_secret = cloudinary.config().api_secret
            api_key = cloudinary.config().api_key
            cloud_name = cloudinary.config().cloud_name
            
            signature = cloudinary.utils.api_sign_request(params_to_sign, api_secret)
            
            print("=== CLOUDINARY SIGNATURE GENERATED ===")
            print(f"Timestamp: {timestamp}")
            print(f"Signature: {signature}")

            return Response({
                'signature': signature,
                'timestamp': timestamp,
                'api_key': api_key,
                'cloud_name': cloud_name
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print("--- SIGNATURE GEN ERROR ---", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


