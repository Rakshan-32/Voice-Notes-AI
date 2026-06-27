# AI Voice Notes Transcriber and Assistant

An AI-powered voice note assistant that converts audio recordings into text, generates summaries, allows users to ask questions about the transcript, and automatically stores results using Make.com and Google Sheets.

## Project Objective

This project helps users convert long voice notes into structured, searchable, and interactive text content. It is useful for meetings, lectures, reminders, and personal notes.

## Features

* Upload or record voice notes
* Convert speech to text using Whisper
* Generate AI summary using Groq API
* Chat with the generated transcript
* Download transcript as TXT file
* Send transcript and summary to Make.com webhook
* Store results automatically in Google Sheets

## Tech Stack

* Python
* Gradio
* Whisper
* Groq API
* Make.com
* Google Sheets
* dotenv
* requests

## How It Works

1. User uploads or records an audio file.
2. Whisper converts the audio into text.
3. Groq API generates a summary from the transcript.
4. User can ask questions based on the transcript.
5. Transcript and summary are sent to Make.com.
6. Make.com stores the data in Google Sheets.

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
MAKE_WEBHOOK_URL=your_make_webhook_url
```

## Run the Project

```bash
python app.py
```

Open the local URL shown in the terminal:

```text
http://127.0.0.1:7860
```

## Automation Workflow

Make.com workflow:

```text
Webhook → Google Sheets → Add Row
```

The app sends transcript and summary to Make.com, and Make.com stores them in Google Sheets.

## Future Scope

* Multi-language transcription
* Speaker identification
* Better noise reduction
* Action item extraction
* Email and Telegram notifications
* Cloud deployment

## Project Status

Completed and ready for capstone submission.
