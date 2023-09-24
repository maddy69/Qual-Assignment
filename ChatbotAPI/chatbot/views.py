from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from django.shortcuts import render

MODEL_NAME = "distilgpt2"
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)

def homepage(request):
    return render(request, 'index.html')

@api_view(['POST'])
def chat_endpoint(request):
    user_message = request.data.get("message")
    input_ids = tokenizer.encode(user_message, return_tensors='pt')
    output = model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id,do_sample=True, temperature = 0.7, top_k = 50)
    bot_response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    chat = ChatHistory(user_message=user_message, bot_response=bot_response)
    chat.save()

    return Response({"message": bot_response})

@api_view(['GET'])
def chat_history_endpoint(request):
    history = ChatHistory.objects.all()
    serializer = ChatHistorySerializer(history, many=True)
    return Response(serializer.data)

