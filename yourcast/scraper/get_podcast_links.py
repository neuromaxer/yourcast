import re

from markdownify import markdownify as md

from yourcast.tools.helpers import store_json

# Path to your HTML file
html_path = "yourcast/assets/podcasts_from_2025.html"

# Read the HTML file
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Convert HTML to Markdown
markdown_content = md(html_content)


def extract_episode_info(markdown: str) -> list:
    # Regex to match the multiline markdown structure
    pattern = re.compile(r"\[([^\n\[]+)\n-+\n\n([^\n]+)\n\n([A-Za-z]{3} \d{2}, \d{4})\]\((/[^)]+)\)", re.MULTILINE)
    matches = pattern.findall(markdown)
    # Each match: (episode_name, podcast_name, date, url)
    result = []
    for episode_name, podcast_name, date, url in matches:
        result.append(
            {
                "episode_name": episode_name.strip(),
                "podcast_name": podcast_name.strip(),
                "publication_date": date.strip(),
                "url": "https://www.readablepod.com" + url.strip(),
            }
        )
    return result


episode_info = extract_episode_info(markdown_content)

store_json({"raw_episodes": episode_info}, "yourcast/assets/episode_urls.json")

# Optionally, save to a .md file
# with open("output.md", "w", encoding="utf-8") as f:
#     f.write(markdown_content)
