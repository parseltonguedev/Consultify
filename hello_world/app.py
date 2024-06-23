import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Predefined responses
predefined_responses = {
    "What services do you offer?": "We offer a wide range of legal services including contract law, family law, criminal defense, and corporate law. For more details, visit our services page.",
    "What is your price list?": "Our pricing varies depending on the service. For a detailed price list, please visit our pricing page or contact our support team.",
    "How can I contact you?": "You can contact us via phone at (123) 456-7890 or email at contact@legalservices.com. We are also available on WhatsApp and Telegram.",
    "What are your operating hours?": "Our operating hours are Monday to Friday, 9 AM to 6 PM. We are closed on weekends and public holidays."
}

def lambda_handler(event, context):
    try:
        # Get user query from the event
        body = json.loads(event['body'])
        user_query = body['query']
        conversation_history = body.get('history', [])

        # Check for predefined response
        if user_query in predefined_responses:
            return {
                'statusCode': 200,
                'body': json.dumps({'response': predefined_responses[user_query]})
            }

        # OpenAI API key from environment variable

        # Generate prompt for the new API
        messages = [
            {"role": "system", "content": "You are a highly experienced legal consultant specializing in contract law."},
            {"role": "user", "content": user_query}
        ]

        for message in conversation_history:
            messages.append({"role": "user", "content": message})

        # Call OpenAI API with the new ChatCompletion.create method
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=0.7)

        # Extract and return the response
        result = response.choices[0].message.content.strip()
        return {
            'statusCode': 200,
            'body': json.dumps({'response': result})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
