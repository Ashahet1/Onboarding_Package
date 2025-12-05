import os
import time
import ssl
import urllib3
from openai import OpenAI
from openai import RateLimitError, OpenAIError

# Disable SSL warnings for debugging (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Try with default settings first
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Standard client failed: {e}")
        # Try with custom HTTP client for SSL issues
        import httpx
        custom_client = httpx.Client(
            verify=False,  # Disable SSL verification as workaround
            timeout=30.0
        )
        return OpenAI(api_key=api_key, http_client=custom_client)


def summarize_markdown_files(client, markdown_files, image_files=None):
    """
    Summarizes markdown files and mentions related images
    """
    summaries = {}
    
    for path, content in markdown_files.items():
        try:
            # Get the directory of this markdown file
            file_dir = os.path.dirname(path)
            
            # Find images in the same directory
            related_images = []
            if image_files:
                related_images = [img for img in image_files if img.startswith(file_dir)]
            
            # Check if this file has related images
            has_images = len(related_images) > 0
            
            # TRUNCATE LARGE FILES - Keep first 3000 characters to stay under token limit
            if len(content) > 3000:
                truncated_content = content[:3000] + "\n\n[... Content truncated for brevity ...]"
                print(f"⚠️ Truncated {path} from {len(content)} to {len(truncated_content)} characters")
            else:
                truncated_content = content
            
            # Enhanced prompt that includes image information
            prompt = f"""
Summarize the following markdown file in 3-5 concise sentences.

File: {path}
Directory: {file_dir}
Related images in same directory: {related_images}

If there are related images, mention them in the summary.
End with: "For full details, refer to: [{os.path.basename(path)}]({path})"

Markdown content:
{truncated_content}
"""

            # Rate-limit-safe call with retry
            max_retries = 2
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert technical writer."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2,
                        max_tokens=200  # Reduced from 250 to save tokens
                    )
                    
                    summary_text = response.choices[0].message.content.strip()
                    
                    # Append custom note about images if they exist
                    if has_images:
                        summary_text += "\n\nNote: This section includes images/diagrams for improved understanding."
                    
                    summaries[path] = summary_text
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 30  # Increased wait time
                        print(f"Rate limit or other error: {e}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        # If all retries fail, create a simple fallback summary
                        summaries[path] = f"Documentation file: {os.path.basename(path)}. For full details, refer to: [{os.path.basename(path)}]({path})"
                        print(f"⚠️ Failed to summarize {path}, using fallback summary")
                        break
                        
        except Exception as e:
            summaries[path] = f"❌ Error summarizing {path}: {str(e)}"
    
    return summaries