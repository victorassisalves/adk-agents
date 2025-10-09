# Auto Content Pipeline

Creates polished technical blog posts end-to-end using a team of ADK agents. Start with a theme, collaborate on outline decisions, research authoritative sources, generate copy, edit it into your voice, save Markdown, and finish with an on-brand image.

## Pipeline at a Glance
```
User Brief → Planning → Research (Loop) → Writing → Editing (with approval) → Markdown Save → Image Generation
```
`post_theme_extractor` is the entry point: it negotiates post settings with the user and then triggers the sequential production pipeline.

## Agent Roster
| Stage | Agent | What it does | Notable Context |
| --- | --- | --- | --- |
| Preflight | `Post_Theme_Extractor` | Captures theme, tone, language, audience; gathers user approvals. | Kicks off `Content_Creation_Pipeline` |
| 1 | `planning_agent` | Researches best structure patterns and drafts the outline. | Stores `outline` |
| 2 | `robust_blog_researcher` (`LoopAgent`) | Retries `research_agent` up to 3x using `google_search` to gather citations. | Produces `research_notes` |
| 3 | `writing_agent` | Writes the long-form draft using the outline and research. | Emits `draft` |
| 4 | `editing_agent` | Rewrites draft in Victor Drakentide’s voice, validating with the user until approved. | Outputs `final_post` |
| 5 | `finishing_agent` | Saves the Markdown to `blog_post.md` via `save_blog_post_to_file`. | Marks completion |
| 6 | `image_generator` | Crafts a prompt from `{outline}` and `{final_post}` and calls `generate_image`. | Returns artifacts + caption |

## Tools
- `google_search` (ADK provided) for up-to-date research.
- `save_blog_post_to_file(blog_post, filename)` to persist Markdown.
- `generate_image(prompt, tool_context)` to render supporting visuals and attach them to the session.

## Running the Pipeline
```bash
adk web
```
or
```bash
adk run auto_content
```
The pipeline pauses for user feedback during planning and editing, keeping the human in the loop where it matters most.

## Tips
- Change the author persona in `editing_agent.instruction` if you want a different writing style.
- Adjust `max_iterations` on `robust_post_researcher` when you need heavier fact gathering.
- Point `save_blog_post_to_file` at your content directory or CMS importer for hands-free publishing.
