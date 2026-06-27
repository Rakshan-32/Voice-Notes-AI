import os
import requests
import gradio as gr
import whisper
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

client = Groq(api_key=GROQ_API_KEY)

print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded!")


def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Keep answers clear and simple."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


def process_audio(audio_file):
    if audio_file is None:
        return "Please upload or record an audio file.", "", "", None

    result = model.transcribe(audio_file)
    transcript = result["text"]

    summary_prompt = f"""
Summarize this voice note clearly in simple bullet points:

{transcript}
"""
    summary = ask_groq(summary_prompt)

    if MAKE_WEBHOOK_URL:
        try:
            requests.post(MAKE_WEBHOOK_URL, json={
                "transcript": transcript,
                "summary": summary
            })
        except Exception as e:
            print("Make.com error:", e)

    return transcript, summary, transcript, create_transcript_file(transcript)


def chat_with_transcript(question, transcript):
    if not transcript:
        return "Please upload and transcribe audio first."

    if not question:
        return "Please type a question."

    prompt = f"""
Answer only using the transcript below.

TRANSCRIPT:
{transcript}

QUESTION:
{question}

Give a simple and direct answer.
"""
    return ask_groq(prompt)


def create_transcript_file(transcript):
    if not transcript:
        return None

    file_path = "transcript.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(transcript)

    return file_path


custom_css = """
#title {
    text-align: center;
    padding: 20px;
}
#subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
}
"""

with gr.Blocks(
    title="AI Voice Notes Transcriber and Assistant",
    css=custom_css,
    theme=gr.themes.Soft()
) as app:

    gr.Markdown(
        """
        # 🎙️ AI Voice Notes Transcriber and Assistant
        """,
        elem_id="title"
    )

    gr.Markdown(
        """
        Convert voice notes into text, generate AI summaries, chat with the transcript, and automatically save results using Make.com.
        """,
        elem_id="subtitle"
    )

    stored_transcript = gr.State("")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="🎧 Upload or Record Voice Note"
            )

            transcribe_button = gr.Button("🚀 Transcribe and Summarize", variant="primary")

        with gr.Column():
            gr.Markdown(
                """
                ### ✅ Features
                - Speech-to-Text transcription  
                - AI-generated summary  
                - Chat with transcript  
                - Make.com automation  
                - Google Sheets storage  
                - Download transcript as TXT  
                """
            )

    with gr.Row():
        transcript_output = gr.Textbox(
            label="📝 Transcript",
            lines=10
        )

    with gr.Row():
        summary_output = gr.Textbox(
            label="📌 Summary",
            lines=7
        )

    download_file = gr.File(label="📥 Download Transcript")

    transcribe_button.click(
        process_audio,
        inputs=audio_input,
        outputs=[transcript_output, summary_output, stored_transcript, download_file]
    )

    gr.Markdown("## 💬 Chat with Transcript")

    question_input = gr.Textbox(
        label="Ask a question about the transcript",
        placeholder="Example: What is the meeting time?"
    )

    ask_button = gr.Button("Ask AI", variant="primary")

    answer_output = gr.Textbox(
        label="🤖 AI Answer",
        lines=5
    )

    ask_button.click(
        chat_with_transcript,
        inputs=[question_input, stored_transcript],
        outputs=answer_output
    )

app.launch()