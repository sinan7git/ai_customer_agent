import openai
import key
import tempfile
import os

conversation = []

# Set OpenAI API key
openai.api_key = key.openai_key

def get_ai_response(question):
    messages = [
    {
        "role": "system",
        "content": """
        You are a recruitment consultant representing TalentPool Recruitement Solutions, a specialized agency that connects businesses with top talent across various industries.
        Your goal is to have a concise, interactive conversation to understand the client's hiring needs, gather their contact information, 
        and assure them that they will be contacted soon for further details. 
        Share specific service information or fees only if the client asks. Focus on asking relevant questions rather than giving too much detail upfront.

        Services offered (provide only if asked):
        - Full-time Recruitment
        - Contract Staffing
        - Executive Search
        - Onboarding and Background Checks
        - Recruitment Process Outsourcing (RPO)

        Conversation guidelines:
        1. Begin with a friendly introduction, such as: "Hello, I'm Benzi, a recruitment consultant at TalentPool Recruitement Solutions. How can I assist you today?"
        2. Ask questions to understand the client's hiring goals and challenges:
        - "Could you tell me a bit about your company and the roles you are looking to fill?"
        - "What are the main challenges you face in finding the right candidates?"
        - "Are you currently using any in-house or external recruitment resources?"
        3. Gather the client’s contact details:
        - "Could I get your phone number or email to follow up with you?"
        4. If the client asks about services or fees, provide the requested information briefly, and ask follow-up questions like:
        - "Does that address your immediate hiring needs?"
        - "Would you like to discuss a custom recruitment plan?"
        5. Offer to schedule a follow-up meeting for customized solutions (at least 2 days ahead, excluding Sunday):
        - "I can schedule a call with one of our senior consultants. Would [insert date] work for you?"
        6. Conclude by thanking the client and assuring them they will hear back soon.

        Always keep responses short, polite, and question-focused, waiting for the client's reply before proceeding.
        """
    },
    {
        "role": "assistant",
        "content": "Hello, my name is Benzi, and I am a recruitment consultant at TalentPool Recruitement Solutions. How can I assist you today?"
    }
    ]


    for message in conversation:
        if "assistant" in message:
            messages.append({"role": "assistant", "content": message["assistant"]})
        if "user" in message:
            messages.append({"role": "user", "content": message["user"]})

    messages.append({"role": "user", "content": question})
    conversation.append({"user": question})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages,
        stream=True
    )

    def generate():
        ai_response = ""
        for chunk in response:
            if "choices" in chunk and "delta" in chunk.choices[0]:
                content = chunk.choices[0].delta.get("content", "")
                ai_response += content
                yield content
        conversation.append({"assistant": ai_response})

    return generate

def transcribe(request):
    if "audio" not in request.files:
        raise ValueError("No audio file provided in the request")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file_name = temp_file.name

    try:
        audio_content = request.files["audio"]
        with open(temp_file_name, "wb") as f:
            f.write(audio_content.read())

        # Transcribe the audio file using the updated API
        with open(temp_file_name, "rb") as audio_file:
            transcription = openai.Audio.transcribe("whisper-1", audio_file)
        return transcription["text"]

    except Exception as e:
        print("Error during transcription:", e)
        raise ValueError("Failed to process the audio file. Please try again.")

    finally:
        # Always remove the temporary file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
