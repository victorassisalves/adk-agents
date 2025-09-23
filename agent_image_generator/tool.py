import base64
import mimetypes
import os
from io import BytesIO
from typing import Dict, List, Optional

from google import genai
from google.genai import types
from google.adk.tools import tool_context  # only needed for type hinting

client = genai.Client()

async def generate_image(
    prompt: str,
    *,
    tool_context: tool_context.ToolContext,
    filename_prefix: str = "generated_image",
) -> Dict[str, Optional[str]]:
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
    )

    saved_artifacts: List[str] = []
    text_response: Optional[str] = None

    for idx, part in enumerate(response.candidates[0].content.parts):
        if part.text:
            text_response = part.text
            continue
        if not part.inline_data:
            continue

        blob = part.inline_data
        extension = mimetypes.guess_extension(blob.mime_type) or ".png"
        filename = f"{filename_prefix}_{idx}{extension}"

        version = await tool_context.save_artifact(
            filename,
            types.Part(inline_data=types.Blob(mime_type=blob.mime_type, data=blob.data)),
        )
        saved_artifacts.append(f"{filename}@v{version}")

    return {
        "generated_images": saved_artifacts,
        "text_response": text_response,
    }

# def generate_image(prompt: str) -> Dict[str, Optional[str]]:
#     """
#     Generate an image using the Gemini 2.5 Flash Image (Nano Banana) model.

#     Args:
#         prompt (str): A descriptive text prompt for the image.

#     Returns:
#         dict: A dictionary with keys:
#           - generated_image (str or None): Path to the saved PNG file.
#           - text_response (str or None): Any text commentary returned by the model.
#     """
#     response = client.models.generate_content(
#         model="gemini-2.5-flash-image-preview",
#         contents=[prompt],
#     )

#     saved_image_path = None
#     text_response = None
#     for part in response.candidates[0].content.parts:
#         if part.text is not None:
#             text_response = part.text
#         elif part.inline_data is not None:
#             image = Image.open(BytesIO(part.inline_data.data))
#             saved_image_path = "generated_image.png"
#             image.save(saved_image_path)

#     return {"generated_image": saved_image_path, "text_response": text_response}

def generate_image_text_and_image(prompt, image_path):
    image = Image.open(image_path)
    saved_image_path = None
    text_response = None
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt, image],
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
            text_response = part.text
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save("generated_image.png")
            saved_image_path = "generated_image.png"
    return {"generated_image": saved_image_path, "text_response": text_response}