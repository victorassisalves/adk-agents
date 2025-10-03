import os

def create_guidelines(content: str)-> dict:
    """
        This tool is responsible for saving a file inside the project.
        Parameters (file_name: str, conten: str)
        And it returns the file location and status success upon success.
        Upon error, returns status failed and the error
    """
    try:
        # Get the directory of the current script (tools/)
        current_dir = os.path.dirname(__file__)

        # Go up one level and into prds/
        guideline_dir = os.path.join(current_dir, "..", "content/guidelines")

        # Make sure prds folder exists
        os.makedirs(guideline_dir, exist_ok=True)

        # Build full path: ../prds/example.md
        file_path = os.path.join(guideline_dir, "guidelines.md")
        mode = "a" if os.path.exists(file_path) else "w"
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(("\n" if mode == "a" else "") + content)

        return {
            "file_location": file_path,
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