import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sys
import os
sys.path.append(os.getcwd())
import spacy
nlp = spacy.load("C:\\Users\\Alonkr\\Downloads\\en_legal_ner_sm")
#from simplifier.test_model import sentence_formatting as sf

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model.load_state_dict(torch.load("C:\\Users\\Alonkr\\Downloads\\test_large_summ_batch_2_CPU.pth"))
model.to(device)

# Pydantic model for input validation
class InputText(BaseModel):
    text: str

@app.post("/summarize")
def generate_summary_api(input_text: str):
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        input_ids = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True)['input_ids'].to(device)
        attention_mask = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True)["attention_mask"].to(device)

        # Generate summary for the current chunk
        output_ids = model.generate(input_ids, attention_mask=attention_mask, max_length=1024, num_beams=3) # change num_beams from 3-5 for summary length
        #beam search of 3 is longer and more detailed than beam search of 5
        # Decode and append the summary
        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary

@app.post("/find_acts")
def find_acts_api(input_text: str):
    doc = nlp(input_text)
    f = ' '
    for ent in doc.ents:
        if ent.label_ == "STATUTE" or ent.label_ == "PROVISION" or ent.label_ == "ACT" or ent.label_ == "REGULATION" : 
            f += f"{ent.label_} : {ent} \n"
    return f
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)