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