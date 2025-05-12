from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>GPT 질문하기</title>
    </head>
    <body style="font-family: sans-serif; padding: 20px; max-width: 600px; margin: auto;">
      <h2>GPT에게 질문하기</h2>
      <input id="prompt" type="text" placeholder="질문을 입력하세요" style="width: 100%; padding: 8px;" />
      <button onclick="askGPT()" style="margin-top: 10px;">질문 보내기</button>
      <div id="response" style="margin-top: 20px; white-space: pre-wrap;"></div>

      <script>
        async function askGPT() {
          const prompt = document.getElementById("prompt").value.trim();
          const responseBox = document.getElementById("response");
          if (!prompt) {
            responseBox.innerText = "질문을 입력해주세요.";
            return;
          }
          responseBox.innerText = "GPT가 응답 중입니다...";

          try {
            const res = await fetch("/generate", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ prompt })
            });
            const data = await res.json();
            responseBox.innerText = data.response || data.error || "응답 없음";
          } catch (e) {
            responseBox.innerText = "서버 연결 실패 또는 오류 발생.";
          }
        }
      </script>
    </body>
    </html>
    """)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "친절하고 유용한 GPT입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return jsonify({"response": response['choices'][0]['message']['content'].strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)







