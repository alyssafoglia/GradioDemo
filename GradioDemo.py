import gradio as gr
from transformers import pipeline

#using hugging faces instead of openAI
summarizer = pipeline("summarization")
qa_pipeline = pipeline("question-answering")

def summarize_transcript(transcript):
    summary = summarizer(transcript, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question(transcript, question):
    answer = qa_pipeline(question=question, context=transcript)
    return answer['answer']

'''
#openAI would be called here  
def summarize_transcript(transcript):
    # Placeholder summary function
    return "This is a placeholder summary of the transcript. OpenAI API would be used here"

#openAI would be called here
def answer_question(transcript, question):
    # Placeholder answer function
    return "This is a placeholder answer to the question."
'''
def display_transcript(file):
    with open(file.name, "r", encoding="utf-8") as f:
        transcript = f.read()
    summary = summarize_transcript(transcript)
    return transcript, summary

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Transcript Summarizer")
    
    with gr.Row():
        with gr.Column():
            transcript_file = gr.File(label="Upload Transcript (.txt)")
            transcript_display = gr.Textbox(label="Transcript Content", lines=10)
            summary_display = gr.Textbox(label="Summary", lines=5)
        
        with gr.Column():
            question_input = gr.Textbox(label="Ask a Question")
            answer_display = gr.Textbox(label="Answer", lines=5)
    
    transcript_file.change(display_transcript, inputs=transcript_file, outputs=[transcript_display, summary_display])
    question_input.submit(answer_question, inputs=[transcript_display, question_input], outputs=answer_display)

# Launch the Gradio app
demo.launch()
