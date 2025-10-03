from rest_framework import serializers


class SendSMSSerializer(serializers.Serializer):
    """Serializer for sending SMS messages via Twilio"""
    to = serializers.CharField(
        max_length=20,
        help_text="Receiver's phone number with country code (e.g., +8801777804236)"
    )
    body = serializers.CharField(
        max_length=1600,
        help_text="SMS message body"
    )
    
    def validate_to(self, value):
        """Validate phone number format"""
        if not value.startswith('+'):
            raise serializers.ValidationError(
                "Phone number must include country code (e.g., +1 for US)"
            )
        # Remove any spaces or special characters
        cleaned_number = ''.join(filter(lambda x: x.isdigit() or x == '+', value))
        if len(cleaned_number) < 10:
            raise serializers.ValidationError(
                "Phone number is too short"
            )
        return cleaned_number
    
    def validate_body(self, value):
        """Validate message body"""
        if not value.strip():
            raise serializers.ValidationError(
                "Message body cannot be empty"
            )
        return value.strip()

