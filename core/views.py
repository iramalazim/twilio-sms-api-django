from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .serializers import SendSMSSerializer


class SendSMSView(APIView):
    """
    API endpoint for sending SMS messages via Twilio
    
    POST /api/send-sms/
    Body: {
        "to": "+18777804236",
        "body": "Your message here"
    }
    """
    
    def post(self, request):
        # Validate input data
        serializer = SendSMSSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        to_number = serializer.validated_data['to']
        message_body = serializer.validated_data['body']
        
        try:
            # Initialize Twilio client
            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            
            # Send SMS
            message = client.messages.create(
                messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
                body=message_body,
                to=to_number
            )
            
            # Return success response
            return Response({
                'success': True,
                'message': 'SMS sent successfully',
                'data': {
                    'message_sid': message.sid,
                    'to': message.to,
                    'body': message.body,
                    'status': message.status,
                    'date_created': message.date_created
                }
            }, status=status.HTTP_200_OK)
            
        except TwilioRestException as e:
            # Handle Twilio-specific errors
            return Response({
                'success': False,
                'error': 'Twilio API Error',
                'message': str(e),
                'code': e.code
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Handle unexpected errors
            return Response({
                'success': False,
                'error': 'Server Error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
