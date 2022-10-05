from gradio import Blocks, Textbox, Button, Label

with Blocks(title="test app") as app:
    tb = Textbox("Hello")
    button = Button("world")
    label = Label("Value")
    button.click(fn=lambda x: label.update(tb.value), inputs=[tb], outputs=[label])

app.launch()
