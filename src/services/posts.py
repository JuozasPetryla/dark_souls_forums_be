from sqlalchemy.orm import Session
from fastapi import HTTPException
from groq import Groq
from src.core.config import settings
from src.db.models import Post

client = Groq(api_key=settings.GROQ_API_KEY)

SUMMARY_PROMPT = """
You are a summary generator for a Dark Souls themed discussion board.

Your task is to generate a SHORT and CONCISE summary (max 2-3 sentences) of the given post text.

Rules:
1. The summary must capture the main idea of the post
2. It should be in Lithuanian language
3. Keep it brief and informative
4. If the post is about Dark Souls gameplay, lore, or builds, focus on the key points
5. Remove any irrelevant details, spam, or off-topic content

Return only the summary text, nothing else.
"""

async def generate_and_save_post_summary(db: Session, post_id: int, content: str, title: str) -> str:
    """Generate AI summary for a post if it doesn't already have one"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # If summary already exists, return it
    if post.summary:
        return post.summary

    # Prepare the text for summarization
    text_to_summarize = f"Įrašo pavadinimas: {title}\n\nTurinys:\n{content}"

    for attempt in range(3):
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SUMMARY_PROMPT},
                    {"role": "user", "content": f"Sužmok šį tekstą:\n\n{text_to_summarize}"},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_completion_tokens=150,
                stream=True
            )

            # Collect the streamed response
            summary_text = ""
            for chunk in stream:
                content_chunk = getattr(chunk.choices[0].delta, "content", None)
                if content_chunk:
                    summary_text += content_chunk

            print(f"[Groq attempt {attempt+1}] generated summary: {summary_text}")

            if summary_text.strip():
                # Save the summary to the database
                post.summary = summary_text.strip()
                db.commit()
                db.refresh(post)
                return summary_text.strip()

        except Exception as e:
            print(f"[Groq attempt {attempt+1}] Exception: {e}")
            continue

    raise HTTPException(
        status_code=500,
        detail="Failed to generate summary for the post."
    )
