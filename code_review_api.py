from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import astroid

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key (Replace with your actual key)
openai.api_key = "your-openai-api-key"

# Define request model
class CodeRequest(BaseModel):
    code: str

# Function to analyze code using AST (Static Analysis)
def static_analysis(code: str):
    try:
        tree = astroid.parse(code)
        return [f"Line {node.lineno}: {node.msg}" for node in tree.body]
    except Exception as e:
        return [str(e)]

# AI-Powered Code Review Endpoint
@app.post("/analyze/")
async def analyze_code(request: CodeRequest):
    """ AI Code Review (GPT-4 + Static Analysis) """
    try:
        # Perform static analysis
        static_issues = static_analysis(request.code)

        # AI Review using OpenAI GPT-4
        ai_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analyze this Python code for errors and suggest improvements."},
                {"role": "user", "content": request.code}
            ]
        )

        return {
            "static_analysis": static_issues,
            "ai_review": ai_response["choices"][0]["message"]["content"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
