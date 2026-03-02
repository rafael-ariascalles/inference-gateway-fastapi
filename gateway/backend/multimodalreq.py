### TODO: Mockup for multimodal request
import base64
import requests

def image_to_data_uri(path, mime="image/png"):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# Assume you already converted page 1 of the PDF to page-1.png
data_uri = image_to_data_uri("page-1.png")

url = "http://127.0.0.1:8080/v1/chat/completions"
payload = {
    "model": "your-multimodal-model",  # started with --mmproj or -hf multimodal GGUF
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Read this page and summarize the main points.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": data_uri},
                },
            ],
        }
    ],
}

resp = requests.post(url, json=payload, timeout=120)
print(resp.json())
