# 🏥 Medical Report Analyzer Chatbot

Ek intelligent chatbot jo medical reports ko analyze karta hai aur Hindi/English mein explain karta hai using Groq AI.

## ✨ Features

- 📄 **PDF & Image Upload**: PDF aur sabhi image formats (JPG, JPEG, PNG, etc.) support
- 🌐 **Automatic Language Detection**: Hindi ya English mein automatically respond karta hai
- 🤖 **Groq AI Powered**: Fast aur accurate medical explanations
- 💬 **Interactive Chat**: Report ke baare mein koi bhi question poocho
- 📱 **Responsive Design**: Mobile aur desktop dono pe works perfectly

## 🚀 Installation & Setup

### Step 1: System Requirements Install Karein

**For Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-hin python3-pip
```

**For macOS:**
```bash
brew install tesseract tesseract-lang
```

**For Windows:**
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install karein aur PATH mein add karein

### Step 2: Python Dependencies Install Karein

```bash
pip install -r requirements.txt
```

### Step 3: Groq API Key Setup

1. **Groq Account Banao**: https://console.groq.com pe jao
2. **Free API Key Lo**: Dashboard se API key generate karo
3. **Environment Variable Set Karo**:

**Linux/macOS:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your-api-key-here"
```

**Permanent Setup (Linux/macOS):**
```bash
echo 'export GROQ_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Application Run Karo

```bash
python app.py
```

Server start ho jayega: `http://localhost:5000`

## 📖 Usage Guide

1. **Browser Open Karo**: `http://localhost:5000` pe jao
2. **Report Upload Karo**: 
   - Click karke ya drag & drop se medical report upload karo
   - PDF ya image (JPG, PNG, etc.) koi bhi format
3. **Questions Poocho**:
   - Hindi mein: "Ye report kya kehti hai?"
   - English mein: "What does this report mean?"
   - Medicine ke baare mein: "Ye medicine kya kaam karti hai?"
   - Normal values: "Kya ye values normal hai?"

## 🛠️ Troubleshooting

### Problem: "GROQ_API_KEY not configured"
**Solution**: Environment variable properly set karein (Step 3 dekho)

### Problem: Tesseract OCR error
**Solution**: 
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

### Problem: Image text extract nahi ho raha
**Solution**: 
- Clear aur readable image upload karein
- Handwritten reports ke liye typed reports better work karte hain
- Image quality improve karein

### Problem: Port 5000 already in use
**Solution**: Port change karo `app.py` mein:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📂 File Structure

```
medical-chatbot/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Frontend UI
├── requirements.txt      # Python dependencies
├── README.md            # Ye file
└── uploads/             # Temporary upload folder (auto-created)
```

## 🔒 Important Notes

- ⚠️ **Medical Disclaimer**: Ye chatbot educational purpose ke liye hai. Always consult a qualified doctor.
- 🔐 **Privacy**: Reports locally process hote hain, data store nahi hota
- 💰 **Groq API**: Free tier available hai with rate limits
- 📱 **File Size**: Maximum 16MB files upload kar sakte ho

## 🎯 Example Questions

**Hindi:**
- "Meri cholesterol level kya hai?"
- "Ye medicine kitni baar leni hai?"
- "Kya meri sugar normal hai?"
- "Doctor ne kya likha hai?"

**English:**
- "What is my blood sugar level?"
- "Are these values normal?"
- "What does this medicine do?"
- "Should I be concerned about anything?"

## 🆘 Support

Problems ho to:
1. README phir se carefully padho
2. Error messages check karo
3. API key properly set hai ya nahi verify karo

## 📝 License

Free to use for personal and educational purposes.

---

**Made with ❤️ for better health awareness**
