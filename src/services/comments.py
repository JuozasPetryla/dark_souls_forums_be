from sqlalchemy.orm import Session
from fastapi import HTTPException
from groq import Groq
from src.core.config import settings
from src.db.models import Comment

client = Groq(api_key=settings.GROQ_API_KEY)

FIXED_PROMPT = "Based on the following text, pick a number between 1 and 200. Return only numeric digits."

async def calculate_and_save_comment_iq(db: Session, comment_id: int, text: str) -> int:
    """
    Calculate a numeric value from text and save it as comment_iq for a specific comment.
    """
    # Fetch the comment first
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Build the prompt message
    user_message = f"{FIXED_PROMPT}\n\nText: {text}"

    # Attempt to get a valid number
    for attempt in range(3):
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.0,  # deterministic output
                max_completion_tokens=10,
                stream=True
            )

            # Collect streamed content
            result_str = ""
            for chunk in stream:
                result_str += chunk.choices[0].delta.content

            # Extract digits only
            digits_only = "".join(filter(str.isdigit, result_str))
            if not digits_only:
                continue

            number = int(digits_only)
            if 1 <= number <= 200:
                # Save to the comment
                comment.comment_iq = number
                db.commit()
                db.refresh(comment)
                return number

        except Exception:
            continue

    raise HTTPException(status_code=500, detail="Failed to generate a valid number between 1-200.")