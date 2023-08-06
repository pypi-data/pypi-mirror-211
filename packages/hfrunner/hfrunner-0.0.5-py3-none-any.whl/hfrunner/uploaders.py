from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def push_to_hub(model_path, path_on_hub):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    model.push_to_hub(path_on_hub)
    tokenizer.push_to_hub(path_on_hub)
