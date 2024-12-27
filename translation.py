import pandas as pd
from transformers import MarianMTModel, MarianTokenizer

class ExcelTranslator:
    def __init__(self, model_path):
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)
        self.model = MarianMTModel.from_pretrained(model_path)

    def translate_text(self, text):
        if pd.isna(text):  # Skip NaN values
            return text
        try:
            inputs = self.tokenizer.encode(text, return_tensors="pt", truncation=True)
            outputs = self.model.generate(inputs, max_length=512)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Error translating '{text}': {e}")
            return text

    def translate_dataframe(self, df):
        return df.map(self.translate_text)

    def translate_excel(self, input_file, output_file):
        try:
            # Load all sheets
            sheets = pd.read_excel(input_file, sheet_name=None)

            # Translate each sheet
            translated_sheets = {}
            for sheet_name, df in sheets.items():
                print(f"Translating sheet: {sheet_name}")
                translated_sheets[sheet_name] = self.translate_dataframe(df)

            # Save the translated sheets back to an Excel file
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                for sheet_name, df in translated_sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Translated file saved as {output_file}")
        except Exception as e:
            print(f"Error processing Excel file: {e}")

# Example usage
if __name__ == "__main__":
    model_path = "local_model"  # Path to the pre-downloaded model folder
    input_file = "data.xlsx"  # Path to the input Excel file
    output_file = "translated_file.xlsx"  # Path to save the translated Excel file

    translator = ExcelTranslator(model_path)
    translator.translate_excel(input_file, output_file)
