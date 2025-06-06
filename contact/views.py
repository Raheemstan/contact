from django.shortcuts import render


from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer


class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Send email to admin
            send_mail(
                subject=f"New contact message for {contact.subject}",
                message=f"Name: {contact.name} <{contact.email}>\n\n{contact.message}",
                from_email=None,
                recipient_list=['admin@mail.com'],
                fail_silently=False,
            )

            # Send confirmation email to user
            send_mail(
                subject="We have received your message",
                message=f"Hello {contact.name},\n\nThank you for reaching out to us. We have received your message and will get back to you shortly.\n\nBest regards,\nYour Company",
                from_email=None,
                recipient_list=[contact.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
