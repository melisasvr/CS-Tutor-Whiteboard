# 🎓 CS Tutor Whiteboard

An interactive, AI-powered Computer Science tutor featuring a dynamic HTML5 whiteboard canvas and natural neural voice narration. It acts as a smart, slightly sarcastic senior CS student explaining complex Data Structures, Algorithms, and Operating Systems concepts step-by-step.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-005571?logo=fastapi)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

* **Structured AI Tutoring:** Powered by Groq LLMs, structured in pedagogical stages (`hook`, `mental_model`, `why`, `confusions`, `formal`, `mini_project`).
* **Live Whiteboard Visualization:** Real-time HTML5 Canvas animation synced step-by-step with the lesson using custom drawing commands[cite: 1, 3].
* **Free Neural Audio:** Integrated with Microsoft Edge TTS (`edge-tts`) for natural human-like speech without paywalls or API limits[cite: 4].
* **Interactive Prompts:** Tap suggested questions or type your own responses to steer the lesson flow[cite: 1, 3].
## ⚠️ Note on AI Speech Latency
- Because the application generates neural voice audio on-the-fly using Edge TTS, there may be a **brief delay (1–3 seconds)** before the audio starts playing, depending on sentence length and network response time. The whiteboard and text captions will update instantly while the audio loads.

---

## 📁 Project Structure
```
cs-tutor-whiteboard/
├── main.py              # FastAPI application & WebSocket server
├── index.html           # Frontend UI, Canvas drawing logic, and audio handler
├── requirements.txt     # Python dependency definitions
├── .env                 # Environment configuration (GROQ_API_KEY)
├── .gitignore           # Git ignore file (prevents secret leaks)
└── README.md            # Project documentation
```

---
## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, WebSockets, `edge-tts`, Groq Async SDK[cite: 2, 4].
* **Frontend:** Vanilla JavaScript, HTML5 Canvas, CSS3[cite: 1, 3].
* **LLM Engine:** Groq API (openai/gpt-oss-120b or equivalent)
---

## 💡 Example Topics to Try
- You can type any CS concept into the topic bar to start a structured lesson. Here are a few recommended topics:
- "Arrays vs Linked Lists"
- "Virtual Memory and Paging"
- "Hash Tables"
- "Processes vs Threads"
- "Recursion and the Call Stack"

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher installed on your machine.
* A free **Groq API Key** (`GROQ_API_KEY`).

### 1. Clone the Repository
- `git clone [https://github.com/your-username/cs-tutor-whiteboard.git](https://github.com/your-username/cs-tutor-whiteboard.git)`
- `cd cs-tutor-whiteboard`

### 2. Install Dependencies
- `pip install -r requirements.txt`

### 3. Environment Configuration
- Create a `.env` file in the root directory and add your Groq API key:
- `GROQ_API_KEY=your_groq_api_key_here`

### 4. Run the Application
- Start the Uvicorn development server:
- `uvicorn main:app --reload`
- Open your browser and navigate to: `http://127.0.0.1:8000`

---

## 🤝 Contributing
- Contributions are always welcome! If you'd like to improve the whiteboard capabilities, add new stages, or refine the prompt style:
1. Fork the Project.
2. Create your Feature Branch (git checkout -b feature/AmazingFeature).
3. Commit your Changes (git commit -m 'Add some AmazingFeature').
4. Push to the Branch (git origin push feature/AmazingFeature).
5. Open a Pull Request.

---

## 📄 License
- Distributed under the MIT License. See below for details:
- MIT License

```
Copyright (c) 2026 CS Tutor Whiteboard Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```