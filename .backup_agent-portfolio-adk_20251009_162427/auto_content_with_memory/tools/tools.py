import mimetypes
import os
from typing import Dict, List, Optional

from google import genai
from google.genai import types
from google.adk.tools import tool_context  # only needed for type hinting

client = genai.Client()

current_dir = os.path.dirname(__file__)
def create_file(content: str, file_path: str) -> dict:
    """
        Persist file content to the provided markdown file path.
        Parameters (content: str, file_path: str)
        Returns the file location and status "success" when writing succeeds.
        Upon error, returns status "failed" and the error message.
    """
    try:
        # Ensure we can create the parent folder before writing.
        resolved_path = os.path.abspath(file_path)
        parent_dir = os.path.dirname(resolved_path)

        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        mode = "a" if os.path.exists(resolved_path) else "w"
        with open(resolved_path, mode, encoding="utf-8") as f:
            f.write(("\n" if mode == "a" else "") + content)

        return {
            "file_location": resolved_path,
            "status": "success"
        }
    except FileNotFoundError:
        return {
            "status": "failed",
            "error": "Directory not found."
        }
    except PermissionError:
        return {
            "status": "failed",
            "error": "Permission denied when writing file."
        }
    except OSError as e:
        return {
            "status": "failed",
            "error": f"OS Error: {e}."
        }

def read_file(file_path: str) -> dict:
    """
        Use this tool to read the contents of a file in a determined path.
        Upon success:
        returns {file_content: str, status: str }
        Upon failure:
        returns {status: failed, error: str}
    """
    try:
        file_content = ""
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return {
            "file_content": file_content,
            "status": "success"
        }
    except FileNotFoundError:
        return {
            "status": "failed",
            "error": "File not found."
        }
    except PermissionError:
        return {
            "status": "failed",
            "error": "Permission denied when reading file."
        }
    except OSError as e:
        return {
            "status": "failed",
            "error": f"OS Error: {e}."
        }

def get_user_file_path(user: str)-> dict:
    """
        Use this tool to change the file path to save the content and guidelines.
        Upon success:
        returns {
            "user_content_path": content_dir,
            "user_guideline_path": guideline_dir,
            "user_guideline_file_path": guideline_file
        }
        Upon failure:
        returns {status: failed, error: str}
    """
    user_folder = user.strip().lower().replace(" ", "_")
    try:

        base_dir = os.path.abspath(os.path.join(current_dir, ".."))  # one level up

        content_dir = os.path.join(base_dir, "content", user_folder)
        guideline_dir = os.path.join(content_dir, "guidelines")
        guideline_file = os.path.join(guideline_dir, "guidelines.md")

        return {
            "user_content_path": content_dir,
            "user_guideline_path": guideline_dir,
            "user_guideline_file_path": guideline_file
        }
    except FileNotFoundError:
        return {
            "status": "failed",
            "error": "File not found."
        }
    except PermissionError:
        return {
            "status": "failed",
            "error": "Permission denied when reading file."
        }
    except OSError as e:
        return {
            "status": "failed",
            "error": f"OS Error: {e}."
        }

def get_user_list() -> dict:
    """
        This function returns the user list from a md file

    """
    user_list = os.path.join(current_dir, "..", f"content")

    file_path = os.path.join(user_list, "user_list.md")
    file_content = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return {
            "file_content": file_content,
            "status": "success"
        }
    except FileNotFoundError:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return {
            "file_content": file_content,
            "status": "success"
        }

def create_user_list(user_content: str) -> dict:

    """
        This function create and or update the user list and return the updated file content.
        Upon success:
        returns {file_content: str, status: str }
        Upon failure:
        returns {status: failed, error: str}
    """
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    user_list = os.path.join(base_dir, "content")

    try:
        file_path = os.path.join(user_list, "user_list.md")
        mode = "a" if os.path.exists(file_path) else "w"
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(("\n" if mode == "a" else "") + user_content)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return {
            "file_content": file_content,
            "status": "success"
        }
    except FileNotFoundError:
        return {
            "status": "failed",
            "error": "File not found."
        }
    except PermissionError:
        return {
            "status": "failed",
            "error": "Permission denied when reading file."
        }
    except OSError as e:
        return {
            "status": "failed",
            "error": f"OS Error: {e}."
        }


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