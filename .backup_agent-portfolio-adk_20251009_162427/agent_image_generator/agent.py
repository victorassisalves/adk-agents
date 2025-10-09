import datetime
from google.adk.agents import Agent

from agent_image_generator.tool import generate_image

audio_model_native_audio = "gemini-live-2.5-flash-preview-native-audio"
audio_model = "gemini-live-2.5-flash-preview"
text_model_lite = "gemini-2.5-flash-lite"
text_model = "gemini-2.5-flash"
image_model = "gemini-2.5-flash-image-preview"
now = datetime.datetime.now()

image_generator = Agent(
    name="Master_Image_Generator_Agent",
    model=text_model,
    description=(
        "You are an expert in generating images using generative AI.\n"
        "You use the Image_Prompt_Generator_Agent to help you create detailed prompts "
        "for generating images."
    ),
    instruction=(
        "You are a helpful assistant that generates images using generative AI. Pass the user's prompt to the tool generate_image as a parameter."
        "If a user provides an image prompt and the path to an existing image, pass the image path as the second argument to the tool.\n"
        "If the user only provides an image prompt, use the tool generate_image to generate an image based on the prompt alone.\n"
        "Display the image and any text commentary returned by the model inside the chat."
    ),
    tools=[generate_image],
)

root_agent = Agent(
    name="Master_Image_Prompt_Generator_Agent",
    model=text_model,
    description=(
        "You are an expert in creating detailed prompts for generating images using generative AI."
    ),
    instruction=(
        "You are a helpful assistant that creates detailed prompts for generating images using generative AI. Pass the user's prompt to the tool generate_image as a parameter. If a user provides an image prompt and the path to an existing image, send to the agent as well.\n"
    ),
    sub_agents=[image_generator],
    output_key="image_details",
)