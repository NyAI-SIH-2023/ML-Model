import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sys
import os
sys.path.append(os.getcwd())
from simplifier.test_model import sentence_formatting as sf

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model.load_state_dict(torch.load("C:\\Users\\Alonkr\\Downloads\\acts_trained_model_CPU.pt"))
model.to(device)

# Pydantic model for input validation
class InputText(BaseModel):
    text: str

def generate_summary(inp):
    #input_ids = tokenizer(act, return_tensors="pt").input_ids.to(device)
    #output_ids = model.generate(input_ids,max_length = 128,num_beams=4)
    #summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    #return summary
    
    inputs = tokenizer(inp, return_tensors="pt", truncation=True, padding=True)

    # Ensure attention mask is present
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Generate the summary
    output_ids = model.generate(input_ids, attention_mask=attention_mask, max_length=128, num_beams=4)

    # Decode and return the summary
    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary

@app.post("/summarize")
def generate_summary_api(input_text: InputText):
    #path = os.path.join(os.getcwd(),'data/raw data/1.txt')
    document = input_text.text
    
    sentences = sf.get_sentences(document)
    
    if len(sentences) < 20:
        n = len(sentences)
    else:
        n=sf.calculate_n(len(sentences))
    
    result = sf.rank_sentences(document,sentences)
    top_n_sentences = result[:n]
    paragraphs = sf.group_sentences_into_paragraphs(top_n_sentences)
    f = ''
    for i in paragraphs:
        f += generate_summary(i)
    return f
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)