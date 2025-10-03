import os

def save_prd_file(file_name: str, content: str)-> dict:
    """
        This tool is responsible for saving a file inside the project. 
        And it returns the file location and status success upon success.
        Upon error, returns status failed and the error
    """
    try:
        # Get the directory of the current script (tools/)
        current_dir = os.path.dirname(__file__)

        # Go up one level and into prds/
        prds_dir = os.path.join(current_dir, "..", "prds")

        # Make sure prds folder exists
        os.makedirs(prds_dir, exist_ok=True)

        # Build full path: ../prds/example.md
        file_path = os.path.join(prds_dir, f"{file_name}.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("Saved to:", os.path.abspath(file_path))
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