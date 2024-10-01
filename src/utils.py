import json
import re
import pdfkit
import tiktoken
import os
import base64
import requests
import aioboto3
import asyncio
from aiosmtplib import SMTP
from pinecone import Pinecone
from openai import AsyncOpenAI
from pdf2image import convert_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from config import *
# from src.mongodb import *
from src.html_contents import *

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
# textract = aioboto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

pc = Pinecone(PINECONE_API_KEY)
pindex = pc.Index(PINECONE_INDEX)


def decrypt(data: str) -> str:
    secret_key = SECRET_HASH_KEY
    iv = SECRET_IV
    ciphertext = b64decode(data)
    derived_key = b64decode(secret_key)
    cipher = AES.new(derived_key, AES.MODE_CBC, iv.encode('utf-8'))
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad(decrypted_data, 16).decode("utf-8")


async def get_embedding(text):
    embedding = await client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return embedding.data[0].embedding
   
    
def get_history_text(history):
    text = ""
    for h in history:
        if h['role'] != 'system':
            text += f"{h['role'].upper()}: {h['content']}\n\n"
    return text


def history_to_html_content(history):
    url_pattern = r"image_url: ([^\s]+)"
    html_content = ""
    for h in history:
        content = h['content'].replace('\n', '<br/>')
        if h['role'] == 'user':
            match = re.search(url_pattern, h['content'])
            if match:
                url = match.group(1)
                html_content += f"""
                    <div class="user-message message">
                        <p>{content.split('question: ')[1]}</p>
                        <img src={url} alt="User uploaded image" />
                    </div>
                    """
            else:
                html_content += f"""
                    <div class="user-message message">
                        {content}
                    </div>\n
                """
        elif h['role'] == 'assistant':
            html_content += f"""
                <div class="assistant-message message">
                    {content}
                </div>\n
            """
    return html_content


def get_history_html(history):
    history_html = history_to_html_content(history)
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat History</title>
    </head>
    <body>
    <div class="chat-container">
    <!-- Assistant's message -->
        {history_html}
    <div class="clear"></div>
    </div>
    </body>
    </html>
    """

    html_content = html_content.format(history_html=history_html)
    return html_content


async def sumarize_history(bot, thread_id):
    html_content = get_summarization_html()
    summarization_text = await bot.generate_summarize_text(thread_id)
    css_file = './public/css/summarize.css'
    html_content_with_image = html_content.format(logo=LOGOFILE, text=summarization_text)

    pdf = pdfkit.from_string(html_content_with_image, False, css=css_file)
    return pdf


async def save_history(filename, history):
    html_content = get_history_html(history)
    css_file = './public/css/feedback.css'
    pdfkit.from_string(html_content, f'feedbacks/{filename}.pdf', css=css_file)
    return f"feedbacks/{filename}.pdf"


async def send_mail(feedback_text, rate,  usermail, username, history):
    file_path = await save_history(usermail, history)

    smtpserver = SMTP(hostname="smtp.gmail.com", port=587)
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = 'TalkHealth.AI Feedback'

    html_content = get_feedback_html(feedback_text, rate, usermail, username)
    msg.attach(MIMEText(html_content, 'html'))
    
    attachment = MIMEBase('application', 'octet-stream')

    try:
        with open(file_path, 'rb') as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="ChatHistory.pdf"')
        msg.attach(attachment)
    except IOError:
        print(f"Could not open or read the file {file_path}. Please check the file path and permissions.")

    try:
        await smtpserver.connect()
        await smtpserver.starttls()
        await smtpserver.login(SENDER_EMAIL, APP_PASSWORD)
        await smtpserver.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        await smtpserver.quit()
        
        
async def send_contact(feedback_text, usermail, username):
    smtpserver = SMTP(hostname="smtp.gmail.com", port=587)

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = 'TalkHealth.AI Contact'

    # Assuming get_contact_html is defined elsewhere and synchronous.
    # If it performs I/O, consider making it asynchronous as well.
    html_content = get_contact_html(feedback_text, usermail, username)  
    msg.attach(MIMEText(html_content, 'html'))

    try:
        await smtpserver.connect()
        await smtpserver.starttls()
        await smtpserver.login(SENDER_EMAIL, APP_PASSWORD)
        await smtpserver.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        await smtpserver.quit()
        

async def send_ResetEmail(feedback_text, usermail):
    smtpserver = SMTP(hostname="smtp.gmail.com", port=587)

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = usermail  # Assuming you want to send this to the user's email
    msg['Subject'] = 'TalkHealth.AI Password Reset'

    html_content = get_Reset_html(feedback_text, usermail)  # Assuming this function is defined elsewhere
    msg.attach(MIMEText(html_content, 'html'))

    try:
        await smtpserver.connect()
        await smtpserver.starttls()
        await smtpserver.login(SENDER_EMAIL, APP_PASSWORD)
        await smtpserver.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        await smtpserver.quit()
        
        
def count_tokens_from_messages(messages, model):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 3
    tokens_per_name = 1
    num_tokens = 0
    
    if isinstance(messages, str):
        num_tokens += len(encoding.encode(messages))
    else:
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3
    print(num_tokens)
    return num_tokens


def calculate_cost(num_tokens, is_input):
    if is_input:
        return num_tokens * 0.00001
    else:
        return num_tokens * 0.00003
    
    
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')    
    
    
def convert_pdf_to_images(pdf_url, user_id):
    if not os.path.exists(f'images/{user_id}'):
        os.makedirs(f'images/{user_id}')
    pdf = requests.get(pdf_url, stream=True)
    images = convert_from_bytes(pdf.raw.read())
    image_files = []
    for idx in range(len(images)):
        images[idx].save(f'images/{user_id}/'+ str(idx+1) +'.png', 'PNG')
        image_files.append(encode_image(f'images/{user_id}/'+ str(idx+1) +'.png'))
    return image_files


async def textract_fromS3(url):
    session = aioboto3.Session()
    async with session.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION) as textract:
        response = await textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': 'pdfimageupload',
                    'Name': url.split('/').pop(),
                }
            }
        )
        request_text = ""
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                request_text = request_text + item['Text'] + "\n"
        return request_text


async def pdf_textract_froms3(url):
    # Start the document text detection job
    session = aioboto3.Session()
    async with session.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION) as textract:
        start_response = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': 'pdfimageupload',
                    'Name': url.split('/').pop(),
                }
            }
        )
        
        job_id = start_response['JobId']
        print(f"Started job with ID: {job_id}")

        # Polling for the text detection job to complete
        while True:
            response = await textract.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            
            if status == 'SUCCEEDED':
                break
            elif status == 'FAILED':
                print("Text detection job failed")
                return []
            else:
                await asyncio.sleep(2)  # Avoids spamming AWS with requests
        # Once the job succeeds, process and return the detected text
        request_text = ""
        next_token = None
        while True:
            kwargs = {'JobId': job_id}
            if next_token:
                kwargs['NextToken'] = next_token
            response = await textract.get_document_text_detection(**kwargs)
            
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    request_text += block['Text'] + "\n"
            next_token = response.get('NextToken', None)
            if not next_token:
                break
        return request_text