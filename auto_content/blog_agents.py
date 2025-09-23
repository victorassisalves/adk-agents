"""
Blog publishing agents for the tech‑startups workflow.

This module defines a set of ADK agents and tools that work together to
research a trending topic, write an article, generate an image prompt
using Gemini, generate an image via Nano Banana (Gemini 2.5 Flash),
create alt text, and save the result locally as a Markdown file and a
JPEG image.  It uses the Agent Development Kit (ADK) to orchestrate
LLM agents and function tools in a sequential workflow.

Environment variables
---------------------
The following environment variables are expected to be set in a `.env`
file or in your shell:

```
PERPLEXITY_API_KEY=...   # API key for Perplexity
PERPLEXITY_HEADER_AUTH=...  # Additional header value if required
GEMINI_API_KEY=...       # API key for Google Gemini/Nano Banana
BLOG_SAVE_ROOT=posts     # Root folder for saving posts (default: posts)
```

These values are loaded at runtime when the tools execute.  For
security, never commit real API keys to version control.

"""

import base64
import datetime
import json
import os
from typing import Any, Dict, Optional

import requests
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool


# ---------------------------------------------------------------------------
# Configuration helpers
def _get_env(var: str, default: Optional[str] = None) -> str:
    """Fetch an environment variable or return a default value.

    Args:
        var: Name of the environment variable.
        default: Value to return if the variable is not set.

    Returns:
        The environment variable value or the default.
    """
    value = os.getenv(var, default)
    if value is None:
        raise RuntimeError(f"Required environment variable {var} is not set")
    return value


# ---------------------------------------------------------------------------
# Tools

def call_perplexity() -> Dict[str, Any]:
    """Query Perplexity for the latest Spanish tech‑startup trend.

    This tool uses the Perplexity API to generate a Spanish article about
    the most relevant trend in the Spanish‑speaking tech startup
    ecosystem.  It returns the raw JSON response from the API.  In a
    production system you would pass in parameters and handle errors.
    Here we construct a fixed request similar to the n8n workflow.

    Returns:
        A dict with keys ``status`` and ``response``.  ``response`` is
        the raw JSON returned by Perplexity.
    """
    api_key = _get_env("PERPLEXITY_API_KEY")
    header_auth = os.getenv("PERPLEXITY_HEADER_AUTH", "")
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en generar artículos SEO en "
                    "español neutro sobre startups tecnológicas. El tono debe "
                    "ser educativo, práctico, reflexivo e inspirador."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Redacta un artículo basado en la tendencia más relevante "
                    "del ecosistema de startups tecnológicas hispanohablantes "
                    "del día.\n\n"
                    "Devuelve la respuesta estrictamente en formato JSON con esta "
                    "estructura:\n{\n  \"title\": \"[título atractivo en una sola línea]\",\n"
                    "  \"content\": \"[cuerpo del artículo en HTML limpio, sin caracteres "
                    "escapados, sin markdown, sin saltos \n, y sin comentarios "
                    "externos. Usar solo etiquetas estándar de HTML como <p>, <h2>, <ul>, <li>, "
                    "<strong> y <em>. No uses etiquetas personalizadas ni scripts.]\"\n}\n\n"
                    "El artículo debe:\n"
                    "- Tener entre 1000 y 1500 palabras.\n"
                    "- Incluir subtítulos usando <h2>.\n"
                    "- Iniciar con un gancho atractivo de máximo 3 frases dentro de <p>.\n"
                    "- Incluir al menos 2 datos estadísticos actuales con fuente (en texto).\n"
                    "- Ofrecer mínimo 3 consejos útiles, en formato de lista con <ul> y <li>.\n"
                    "- Terminar con una reflexión motivadora e invitación a sumarse a la comunidad (sin enlaces).\n"
                    "- Usar naturalmente palabras clave como: startups tecnológicas, innovación, emprendimiento, inversión, comunidad.\n\n"
                    "No agregues ningún texto ni explicación fuera del objeto JSON."
                ),
            },
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if header_auth:
        headers["x-api-key"] = header_auth
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    try:
        response.raise_for_status()
        data = response.json()
        return {"status": "success", "response": data}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "response": None}


def generate_image_with_gemini(prompt: str) -> Dict[str, Any]:
    """Generate an image using the Gemini (Nano Banana) model.

    This tool calls Google's generative image API.  It expects an API
    key in the ``GEMINI_API_KEY`` environment variable.  The returned
    object contains a base64‑encoded JPEG string.

    Args:
        prompt: Text prompt for the image.

    Returns:
        A dict with ``status`` and ``image_bytes`` or ``error``.
    """
    api_key = _get_env("GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateImage"
    params = {"key": api_key}
    body = {"prompt": prompt, "n": 1, "size": "768x768"}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, params=params, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Assume the API returns base64 data in data['images'][0]['base64_data']
        image_b64 = data["images"][0]["base64_data"]
        image_bytes = base64.b64decode(image_b64)
        return {"status": "success", "image_bytes": image_bytes}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "image_bytes": b""}


def save_to_local(title: str, content: str, image_bytes: bytes) -> Dict[str, Any]:
    """Save the article and image locally in a date‑based folder.

    Args:
        title: Article title.
        content: Article body as HTML (will be saved with .md extension).
        image_bytes: Raw JPEG data.

    Returns:
        A dict containing the file paths of the saved markdown and image.
    """
    root = os.getenv("BLOG_SAVE_ROOT", "posts")
    date_str = datetime.date.today().isoformat()
    folder = os.path.join(root, date_str)
    os.makedirs(folder, exist_ok=True)
    # Slugify the title for safe filenames
    safe_title = (
        "-".join(
            "".join(c.lower() if c.isalnum() else "-" for c in title).split()
        )
        or "article"
    )
    md_path = os.path.join(folder, f"{safe_title}.md")
    img_path = os.path.join(folder, f"{safe_title}.jpg")
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)
    with open(img_path, "wb") as img_file:
        img_file.write(image_bytes)
    return {
        "status": "success",
        "markdown_file": md_path,
        "image_file": img_path,
    }


# Wrap tools as FunctionTool for ADK
perplexity_tool = FunctionTool.create(call_perplexity)
image_tool = FunctionTool.create(generate_image_with_gemini)
save_tool = FunctionTool.create(save_to_local)


# ---------------------------------------------------------------------------
# Agent definitions

# Research and writing agent: obtains the article from Perplexity
article_agent = LlmAgent(
    name="ArticleWriter",
    model="gemini-2.0-pro",
    description="Genera un artículo SEO en español sobre startups tecnológicas usando Perplexity",
    instruction=(
        "Llama al tool 'call_perplexity' sin parámetros.  Este tool devuelve "
        "un JSON con el título y el cuerpo del artículo.  Guarda el JSON "
        "completo en state['raw_article'] para que otros agentes lo utilicen."
    ),
    tools=[perplexity_tool],
    output_key="raw_article",
)


# Parsing agent: extract title and content from the raw Perplexity response
def parse_article(raw_article: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the title and content from a raw Perplexity response.

    The Perplexity API wraps its responses under a ``choices`` key when
    using the chat/completion endpoint.  This helper normalises the
    structure and pulls out the ``title`` and ``content`` fields.

    Args:
        raw_article: The dictionary returned by the ``call_perplexity`` tool.

    Returns:
        A dict with keys ``status``, ``title`` and ``content``.  If the
        extraction fails, ``status`` will be ``error`` and an ``error``
        message will be included.
    """
    if not raw_article or "response" not in raw_article:
        return {"status": "error", "error": "Invalid article data"}
    try:
        response = raw_article["response"]
        # When using chat completions, the JSON string is nested under choices
        if "choices" in response:
            content_json = json.loads(
                response["choices"][0]["message"]["content"]
            )
        else:
            content_json = response
        title: str = content_json.get("title", "")
        content: str = content_json.get("content", "")
        return {"status": "success", "title": title, "content": content}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


parse_tool = FunctionTool.create(parse_article)

parse_agent = LlmAgent(
    name="ParseArticle",
    model="gemini-2.0-pro",
    description="Extrae el título y el contenido del artículo generado",
    instruction=(
        "Llama al tool 'parse_article' con '{raw_article}' como único "
        "argumento. Este tool devuelve un dict con 'title' y 'content'. "
        "Guarda el título en state['title'] y el contenido en state['content']."
    ),
    tools=[parse_tool],
    output_key="parsed_article",
)


# Prompt generation agent: crafts an English prompt for the image
prompt_agent = LlmAgent(
    name="ImagePromptGenerator",
    model="gemini-2.0-pro",
    description="Genera un prompt en inglés para una imagen editorial cinematográfica",
    instruction=(
        "Utiliza el título ('{title}') y el contenido ('{content}') del artículo "
        "para escribir una sola línea en inglés que describa una imagen editorial "
        "cinematográfica, sin comillas ni texto adicional. La imagen debe ser "
        "apta para un artículo de blog. Guarda el prompt en state['image_prompt']."
    ),
    tools=[],
    output_key="image_prompt",
)


# Image generation agent: calls the Gemini image API via the tool
image_agent = LlmAgent(
    name="ImageGenerator",
    model="gemini-2.0-pro",
    description="Genera una imagen usando el modelo de Gemini y el prompt dado",
    instruction=(
        "Llama al tool 'generate_image_with_gemini' con '{image_prompt}' como "
        "único parámetro. Este tool devuelve bytes JPEG en 'image_bytes'. "
        "Guarda los bytes en state['image_bytes']."
    ),
    tools=[image_tool],
    output_key="generated_image",
)


# Alt text agent: produce a short alt text in Spanish
alt_agent = LlmAgent(
    name="AltTextWriter",
    model="gemini-2.0-pro",
    description="Genera un texto alternativo para la imagen",
    instruction=(
        "A partir del título ('{title}') y del contenido del artículo, escribe "
        "un texto alternativo breve en español que describa la imagen de forma "
        "informativa y accesible. Guarda el texto en state['alt_text']."
    ),
    tools=[],
    output_key="alt_text",
)


# Save agent: writes the article and image to disk
save_agent = LlmAgent(
    name="SaveLocally",
    model="gemini-2.0-pro",
    description="Guarda el artículo y la imagen en una carpeta local",
    instruction=(
        "Llama al tool 'save_to_local' con los siguientes argumentos: '{title}', '{content}', "
        "y '{image_bytes}'.  Este tool crea un directorio con la fecha de hoy y guarda "
        "el archivo Markdown y la imagen.  Guarda las rutas devueltas en state['file_paths']."
    ),
    tools=[save_tool],
    output_key="file_paths",
)


# Root agent orchestrating the workflow
root_agent = SequentialAgent(
    name="BlogPublishingPipeline",
    sub_agents=[
        article_agent,
        parse_agent,
        prompt_agent,
        image_agent,
        alt_agent,
        save_agent,
    ],
    description="Orquesta la generación y almacenamiento de un artículo con su imagen usando ADK",
)


__all__ = [
    "root_agent",
    "article_agent",
    "parse_agent",
    "prompt_agent",
    "image_agent",
    "alt_agent",
    "save_agent",
    "call_perplexity",
    "generate_image_with_gemini",
    "save_to_local",
    "parse_article",
]