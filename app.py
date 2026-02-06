from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from groq import Groq
import PyPDF2
from PIL import Image
import pytesseract
import io
import base64
from werkzeug.utils import secure_filename
from fun import count_tokens

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Groq client - User needs to set GROQ_API_KEY environment variable
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    return Groq(api_key=api_key)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_image(file_path):
    """Extract text from image using OCR"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting from image: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or image files.'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext == 'pdf':
            extracted_text = extract_text_from_pdf(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        if not extracted_text or len(extracted_text) < 10:
            return jsonify({'error': 'Could not extract meaningful text from the file. Please ensure the file is clear and readable.'}), 400
        
        # Store extracted text for chat context
        return jsonify({
            'success': True,
            'extracted_text': extracted_text,
            'message': 'Report analyzed successfully. You can now ask questions about it.'
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        report_text = data.get('report_text', '')
        chat_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize Groq client
        client = get_groq_client()
        
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": """You are a helpful medical assistant that explains medical reports in simple language. 

IMPORTANT INSTRUCTIONS:

1. You are a helpful medical assistant that answers questions related to **medical reports, medical tests, and healthcare in general**.
2. Automatically detect the user's language from their question and respond in the SAME language (Hindi, English, Gujarati).
3. Explain medical terms in simple, easy-to-understand language.
4. Be empathetic and supportive.
5. If you see concerning values in the report, gently suggest consulting a doctor.
6. Never provide definitive diagnoses – only explain what the report shows.
7. Keep responses concise but informative.
8. For any questions NOT related to medical reports or general medical/healthcare advice (e.g.,  pricing, app development, unrelated topics), politely refuse with a short message:
   "I'm sorry, I can only help with medical reports or healthcare-related questions."

DEVELOPER INFORMATION:
- If asked who developed this chatbot, reply: "This medical report analyzer was developed by Prakash Bokarvadiya using AI technology."
- If asked for contact information: 
  Email: prakasbokarvadiya0@gmail.com
  LinkedIn: https://www.linkedin.com/in/prakash-bokarvadiya-609001369
- The AI model used is  Medical Report Analyzer Pro version 1.0 by prakash bokarvadiya, but the application itself was built by Prakash Bokarvadiya

When a medical report is provided, analyze it and answer questions about:
- Test results and their meanings
- Normal vs abnormal values
- Medicines mentioned
- Health recommendations related to the report
- Any medical terminology
- General healthcare questions (like basic health tips, precautions, wellness) if related to medical knowledge
"""
   }
        ]
        
        # Add report context if available
        if report_text:
            messages.append({
                "role": "system",
                "content": f"Medical Report Content:\n\n{report_text}"
            })
        
        # Add chat history
        for msg in chat_history[-5:]:  # Keep last 5 messages for context
            messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Calculate tokens and respect Groq's limits
        prompt_tokens = count_tokens(messages)
        context_window = 131072
        max_output_tokens = 32768  # Groq's hard limit for max_tokens
        safety_buffer = 1000
        
        # Calculate available tokens for output
        max_allowed_output = min(
            max_output_tokens,  # Groq's API limit
            context_window - prompt_tokens - safety_buffer  # Available context
        )
        
        if max_allowed_output < 100:
            return jsonify({
                'error': 'The report is too long and exceeds the model\'s context window. Please try a shorter report or ask a specific question about a part of the report.'
            }), 400
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",  # You can change to other Groq models
            temperature=0.3,
            max_tokens=max_allowed_output,
            top_p=0.9
        )
        
        assistant_response = chat_completion.choices[0].message.content
        
        return jsonify({
            'success': True,
            'response': assistant_response
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check if GROQ_API_KEY is set
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'GROQ_API_KEY not configured'
            }), 500
        
        return jsonify({
            'status': 'ok',
            'message': 'Server is running'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)