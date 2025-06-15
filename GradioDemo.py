import gradio as gr
from transformers import pipeline
import openai
import os

#using hugging faces instead of openAI
summarizer = pipeline("summarization")
qa_pipeline = pipeline("question-answering")

def summarize_transcript(transcript):
    summary = summarizer(transcript, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question(transcript, question):
    answer = qa_pipeline(question=question, context=transcript)
    return answer['answer']

# OpenAI integration
def openai_summary(transcript):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following transcript:\n\n{transcript}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

def openai_answer(transcript, question):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer the following question based on the transcript:\n\nTranscript:\n{transcript}\n\nQuestion:\n{question}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

def display_transcript(file):
    with open(file.name, "r", encoding="utf-8") as f:
        transcript = f.read()
    summary = summarize_transcript(transcript)
    return transcript, summary

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center; color: #4CAF50;'>Transcript Summarizer</h1>")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("<h3 style='color: #2196F3;'>Upload and View Transcript</h3>")
            transcript_file = gr.File(label="Upload Transcript (.txt)")
            transcript_display = gr.Textbox(label="Transcript Content", lines=10, interactive=False)
            summary_display = gr.Textbox(label="Summary", lines=5, interactive=False)
        
        with gr.Column(scale=1):
            gr.Markdown("<h3 style='color: #2196F3;'>Ask Questions</h3>")
            question_input = gr.Textbox(label="Ask a Question")
            answer_display = gr.Textbox(label="Answer", lines=5, interactive=False)
    
    transcript_file.change(display_transcript, inputs=transcript_file, outputs=[transcript_display, summary_display])
    question_input.submit(answer_question, inputs=[transcript_display, question_input], outputs=answer_display)

    # OpenAI section
    gr.Markdown("<h2 style='text-align: center; color: #FF5722;'>OpenAI Integration</h2>")
    with gr.Row():
        openai_summary_display = gr.Textbox(label="OpenAI Summary", lines=5, interactive=False)
        openai_answer_display = gr.Textbox(label="OpenAI Answer", lines=5, interactive=False)
    
    with gr.Row():
        openai_summary_button = gr.Button("Summarize with OpenAI", elem_id="openai-summary-btn")
        openai_answer_button = gr.Button("Answer with OpenAI", elem_id="openai-answer-btn")
    
    openai_summary_button.click(
        openai_summary, 
        inputs=transcript_display, 
        outputs=openai_summary_display
    )
    openai_answer_button.click(
        openai_answer, 
        inputs=[transcript_display, question_input], 
        outputs=openai_answer_display
    )

# Launch the Gradio app
demo.launch()
