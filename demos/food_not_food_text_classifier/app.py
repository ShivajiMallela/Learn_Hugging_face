# 1. Import the required packages
import torch
import gradio as gr

from typing import Dict
from transformers import pipeline

# 2. Define function to use our model on given text 
def food_not_food_classifier(text: str) -> Dict[str, float]:
    """
    Takes an input string of text and classifies it into food/not_food in the form of a dictionary.
    """
    # 2. Setup the pipeline to use the local model (or Hugging Face model path)
    food_not_food_classifier = pipeline(task='text-classification',
                                        model = "shivajimallela/learn_hf_food_not_food_classifier-ditsilbert-base-uncased",
                                        device= "cuda" if torch.cuda.is_available() else "cpu",
                                        top_k = None)
    
    # 3. Get outputs from pipeline (as a list of dicts)
    outputs = food_not_food_classifier(text)[0]
    # print(food_not_food_classifier(text))

    # 4. Format output for Gradio (e.g. {"label_1": probability_1, "label_2": probability_2})
    output_dict = {}
    for item in outputs:
        output_dict[item['label']] = item['score']

    return output_dict

# 3. Create a Gradio interface with details about our app
description = """
A text classifier to determine if a sentence is about food or not food. 

Fine-tuned from [DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased) on a [small dataset of food and not food text](https://huggingface.co/datasets/mrdbourke/learn_hf_food_not_food_image_captions).

See [source code](https://github.com/mrdbourke/learn-huggingface/blob/main/notebooks/hugging_face_text_classification_tutorial.ipynb).
"""

demo = gr.Interface(fn=food_not_food_classifier,
                    inputs='text',
                    outputs=gr.Label(num_top_classes=2),
                    title="😋🙅🥑 Food or Not Food Text Classifier",
                    description=description,
                    examples=[['I whipped up a fresh batch of code, but it seems to have a syntax error.'],
                    ["A delicious photo of a plate of scrambled eggs, bacon and toast."]])

# 4. Launch the interface
if __name__ == "__main__":
    demo.launch()
