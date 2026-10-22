"""CS Tutor backend: FastAPI + WebSocket + Groq + Edge TTS.

Run:  uvicorn main:app --reload
"""
import json
import os
import tempfile
from pathlib import Path

import edge_tts
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Edge TTS voices (free, no API key needed)
VOICES = {
    "marc": "en-US-AndrewMultilingualNeural",   # Male - Andrew
    "anna": "en-US-AvaMultilingualNeural",      # Female - Ava
}

ALLOWED_COMMANDS = {"clear", "text", "rect", "circle", "line", "arrow", "label"}
STAGES = {"hook", "mental_model", "why", "confusions", "formal", "mini_project", "question", "wait"}

SYSTEM_PROMPT = """
You are an expert Computer Science tutor for first and second-year CS students,
specialised in Data Structures & Algorithms and Operating Systems.

STYLE RULES (very important):
- Speak like a smart, slightly sarcastic senior CS student explaining to a confused junior friend.
- Use casual language: "okay so here's the tea", "this is the part that usually messes people up", "imagine this...", "honestly...", "the real reason we do this is..."
- Short sentences. Sound like you're talking, not writing a blog post.
- Show personality. It's okay to be a bit dramatic or funny.
- Never sound like a textbook or Wikipedia.

Your output is parsed by a frontend that draws on an HTML5 Canvas (800x600) and
reads the "speak" text aloud.

TEACHING ORDER (one stage per reply, in this order):
1. hook          - real-world problem or funny analogy
2. mental_model  - simple visual model; draw it
3. why           - trade-offs and reasons behind the design
4. confusions    - the 2-3 things that usually confuse students
5. formal        - formal terms, complexity, precise definitions
6. mini_project  - connect to a small practical example
Move to the next stage only when the student says to continue or has answered.
If the student interrupts with a question, answer it clearly, then steer back.

REPLY WITH VALID JSON ONLY, exactly this shape:
{
  "speak": "natural spoken text, no markdown, 2-5 short sentences",
  "draw_commands": [ ... ],
  "stage": "hook | mental_model | why | confusions | formal | mini_project | question | wait",
  "wait_for_student": true,
  "suggested_questions": ["up to 3 short questions the student might tap"]
}

ALLOWED draw_commands (nothing else):
{"type":"clear"}
{"type":"text","text":"...","x":0,"y":0,"size":18,"color":"#hex","align":"left|center|right"}
{"type":"rect","x":0,"y":0,"width":0,"height":0,"color":"#hex","fill":true}
{"type":"circle","x":0,"y":0,"radius":0,"color":"#hex","fill":false}
{"type":"line","x1":0,"y1":0,"x2":0,"y2":0,"color":"#hex","width":2}
{"type":"arrow","x1":0,"y1":0,"x2":0,"y2":0,"color":"#hex","width":2}
{"type":"label","text":"...","x":0,"y":0,"size":16,"color":"#hex"}

RULES
- The canvas background is white, so use dark or medium colours.
- Keep drawings clean and well spaced inside 800x600. Max 25 commands per reply.
- Almost every important idea gets matching draw_commands. Start a new
  mental model with a "clear" command; otherwise keep adding to the board.
- Keep ONE small running example for the whole concept.
- Prefer short speaking turns. Ask the student something when you want them to think.

Current topic: "__TOPIC__"

CRITICAL: Output raw JSON only. Do not use escaped quotes inside values.
""".strip()


def build_prompt(topic: str) -> str:
    return SYSTEM_PROMPT.replace("__TOPIC__", topic)


def clean_reply(data: dict) -> dict:
    commands = [
        c for c in data.get("draw_commands", [])
        if isinstance(c, dict) and c.get("type") in ALLOWED_COMMANDS
    ][:40]
    stage = data.get("stage") if data.get("stage") in STAGES else "wait"
    questions = [str(q) for q in data.get("suggested_questions", [])][:4]
    return {
        "speak": str(data.get("speak", "")).strip(),
        "draw_commands": commands,
        "stage": stage,
        "wait_for_student": bool(data.get("wait_for_student", True)),
        "suggested_questions": questions,
    }


async def ask_tutor(messages: list[dict]) -> tuple[str, dict]:
    resp = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3, # Lowered from 0.7 to prevent formatting errors
        max_tokens=1800,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content
    return raw, clean_reply(json.loads(raw))


app = FastAPI(title="CS Tutor")


@app.get("/tts")
async def tts(text: str = Query(..., max_length=800), voice: str = Query("marc")):
    """Generate speech using free Edge TTS (Microsoft neural voices)."""
    voice_name = VOICES.get(voice, VOICES["marc"])

    try:
        communicate = edge_tts.Communicate(text, voice_name)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name

        await communicate.save(tmp_path)

        return FileResponse(
            tmp_path,
            media_type="audio/mpeg",
            filename="speech.mp3",
        )
    except Exception as e:
        return Response(status_code=500, content=f"TTS error: {str(e)}")


@app.websocket("/ws")
async def tutor_socket(ws: WebSocket):
    await ws.accept()
    messages: list[dict] = []
    try:
        while True:
            data = await ws.receive_json()
            kind = data.get("type")

            if kind == "start":
                topic = str(data.get("topic", "Arrays vs Linked Lists"))[:100]
                messages = [
                    {"role": "system", "content": build_prompt(topic)},
                    {"role": "user", "content": "Start the lesson with the hook stage."},
                ]
            elif kind == "student":
                if not messages:
                    await ws.send_json({"error": "Start a lesson first."})
                    continue
                text = str(data.get("text", ""))[:500]
                messages.append({"role": "user", "content": f"Student says: {text}"})
            else:
                continue

            try:
                raw, reply = await ask_tutor(messages)
                messages.append({"role": "assistant", "content": raw})
                messages[:] = messages[:1] + messages[1:][-14:]
                await ws.send_json(reply)
            except Exception as exc:
                await ws.send_json({"error": f"Tutor hit a problem: {exc}"})
    except WebSocketDisconnect:
        pass


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "frontend", html=True),
    name="frontend",
)