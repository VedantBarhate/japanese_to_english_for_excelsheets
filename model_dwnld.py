from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-ja-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

tokenizer.save_pretrained("local_model")
model.save_pretrained("local_model")
