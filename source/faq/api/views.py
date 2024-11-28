from rest_framework import viewsets,status
from rest_framework.response import Response
from faq.models import Faq
from .serializers import FaqSerializer
from faq.utils.gpt import get_chatgpt_response,sanitize_cache_key
from django.core.cache import cache



class FaqViewset(viewsets.ViewSet):

    def list(self, request):
        # Cache key for the FAQ list
        cached_faq_list = cache.get('faq_list')
        if cached_faq_list:
            return Response(cached_faq_list, status=status.HTTP_200_OK)

        # If not cached, fetch the FAQ list from the database
        queryset = Faq.objects.all()
        serializer = FaqSerializer(queryset, many=True)
        
        # Cache the FAQ list for 30 minutes
        cache.set('faq_list', serializer.data, timeout=60*30)  # Cache for 30 minutes
        
        return Response(serializer.data)
    

    def create(self, request):
        question_to_search = request.data.get('question', None)  # Get the question from the POST data
        if not question_to_search:
            return Response(
                {"detail": "Question is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sanitize the question to create a safe cache key
        sanitized_question = sanitize_cache_key(question_to_search)

        # Check if the FAQ for this specific question is already cached
        cached_faq = cache.get(f'faq_{sanitized_question}')
        if cached_faq:
            return Response(cached_faq, status=status.HTTP_200_OK)

        # Search for the question in the database
        faq = Faq.objects.filter(question__icontains=question_to_search).first()

        if faq:
            serializer = FaqSerializer(faq)
            faq_data = serializer.data

            # Cache the result for this specific question for 30 minutes
            cache.set(f'faq_{sanitized_question}', faq_data, timeout=60*30)  # Cache for 30 minutes

            return Response(faq_data, status=status.HTTP_200_OK)
        else:
            # If the question doesn't exist in the FAQ, redirect to ChatGPT API integration
            return Response(
                {"detail": "Question does not exist. Kindly search in chatbot."},
                status=status.HTTP_404_NOT_FOUND
            )

class GptViewset(viewsets.ViewSet):

    def create(self, request):
        user_question = request.data.get('question', None)

        if not user_question:
            return Response(
                {"detail": "Question is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the utility function to get response from ChatGPT
        gpt_response, error = get_chatgpt_response(user_question)

        if error:
            return Response(
                {"detail": f"Error communicating with ChatGPT API: {error}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Store the question and answer in the Faq model
        faq_entry = Faq.objects.create(
            question=user_question,
            answer=gpt_response
        )

        # Return the response along with status
        return Response({"response": gpt_response}, status=status.HTTP_200_OK)