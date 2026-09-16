import os
import io
import time
import gc  
from flask import Flask, render_template, request, send_file
from google import genai
from google.genai import types
from pdf2image import convert_from_path, pdfinfo_from_path  
from docx import Document
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Error: GEMINI_API_KEY could not be found in the .env file!")

client = genai.Client(api_key=API_KEY)

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

session_data = {"extracted_text": ""}

@app.route('/')
def home():
    session_data["extracted_text"] = ""
    return render_template('index.html', result=None)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400
        
    file = request.files['pdf_file']
    if file.filename == '':
        return "No file selected", 400

    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)
        
        try:
            poppler_path = r"C:\poppler\Library\bin" 
            
            
            if not os.path.exists(poppler_path):
                poppler_path = None 
            
            
            print("Fetching PDF info...")
            info = pdfinfo_from_path(pdf_path, poppler_path=poppler_path)
            total_pages = info["Pages"]
            print(f"Total Pages to process: {total_pages}")
            
            full_extracted_text = ""
            
            
            for page_num in range(1, total_pages + 1):
                print(f"Processing page {page_num}/{total_pages} (RAM Optimized)...")
                
                
                single_page_list = convert_from_path(
                    pdf_path, 
                    dpi=300, 
                    first_page=page_num, 
                    last_page=page_num, 
                    poppler_path=poppler_path
                )
                
                if not single_page_list:
                    continue
                    
                page = single_page_list[0]
                
                
                img_path = os.path.join(UPLOAD_FOLDER, f"temp_page_{page_num}.png")
                page.save(img_path, 'PNG')
                
                response_text = ""
                try:
                    with open(img_path, 'rb') as f:
                        image_bytes = f.read()
                    
                    input_image_part = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/png"
                    )

                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[
                            input_image_part,
                            "Act as a professional typist and expert linguist. Transcribe all text from this image exactly as it is, regardless of the language (e.g., English, Bengali, Arabic, Spanish, etc.). "
                            "Accurately auto-detect the language and maintain exact paragraphs, lists, alignment, and original spelling. "
                            "Do not translate the text. Do not add any comment, intro, or markdown formatting like '**' or '###'."
                        ]
                    )
                    response_text = response.text if response.text else ""
                    
                except Exception as e:
                    print(f"-> Error on page {page_num}: {e}")
                    response_text = f"[Error processing page {page_num}]"
                
                full_extracted_text += f"--- PAGE {page_num} ---\n" + response_text + "\n\n"
                
                
                if os.path.exists(img_path):
                    os.remove(img_path)
                
                del single_page_list  
                gc.collect()          
            
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            
            session_data["extracted_text"] = full_extracted_text
            return render_template('index.html', result=full_extracted_text)
            
        except Exception as e:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return f"An error occurred: {str(e)}", 500

    return "Invalid file format. Please upload a PDF.", 400

@app.route('/download')
def download_docx():
    text_content = session_data.get("extracted_text", "")
    if not text_content:
        return "No content available to download", 400
    
    doc = Document()
    pages_data = text_content.split("--- PAGE ")
    
    # খালি বা স্পেস ওয়ালা এলিমেন্টগুলো ফিল্টার করে শুধু আসল পেজগুলো নেওয়া
    valid_pages = [p.strip() for p in pages_data if p.strip()]
    total_valid_pages = len(valid_pages)
    
    for index, page_data in enumerate(valid_pages):
        lines = page_data.split('\n', 1)
        if len(lines) > 1:
            actual_text = lines[1] # পেজ নম্বরের নিচের আসল টেক্সটটুকু নেওয়া
            
            paragraphs = actual_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    doc.add_paragraph(para.strip())
            
            # শর্ত: যদি এটি একদম শেষ পেজ না হয়, শুধুমাত্র তখনই পেজ ব্রেক দেওয়া হবে
            if index < total_valid_pages - 1:
                doc.add_page_break()

    docx_buffer = io.BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)
    
    return send_file(
        docx_buffer,
        as_attachment=True,
        download_name="Gemini_Converted_Document.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
