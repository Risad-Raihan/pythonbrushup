from text_renderer import TextRenderer
import json 

with open("sample.json", "r") as f:
    data = json.load(f)

renderer = TextRenderer()
output = renderer.render(data)

print(output)