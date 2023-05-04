import gradio as gr
from wordsmyth import Pipeline
from wordsmyth.core import Output


def predict(text):
    output: Output = list(model.eval(text, 10))[0]
    rating = round(output.rating() * 10)
    return "⭐" * rating


model = Pipeline()
demo = gr.Interface(fn=predict, inputs="text", outputs="text")

demo.launch()
