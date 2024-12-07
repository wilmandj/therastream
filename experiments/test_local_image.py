import openai
import base64

def test_local_image(image_path):
    # Convert the local image to base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Create the request to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            \{
                "role": "user",
                "content": [
                    \{"type": "text", "text": "What is in this image?"\},
                    \{"type": "image_url", "image_url": \{"url": f"data:image/jpeg;base64,\{base64_image\}"\}\}
                ]
            \}
        ]
    )

    # Print the response from the API
    print(response['choices'][0]['message']['content'])