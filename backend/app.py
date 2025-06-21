from fastapi import FastAPI, File, UploadFile
import requests, os, base64, uuid

app = FastAPI()
SEG_ENDPOINT = "https://api.segmind.ai/v1/tryon"
HEADERS = {"x-api-key": os.getenv("SEGMIND_API_KEY")}

@app.post("/tryon")
async def try_on(photo: UploadFile = File(...), cloth: UploadFile = File(...)):
    data = {
        "photo": base64.b64encode(await photo.read()).decode(),
        "cloth": base64.b64encode(await cloth.read()).decode()
    }
    r = requests.post(SEG_ENDPOINT, json=data, headers=HEADERS, timeout=60)
    out_path = f"static/{uuid.uuid4()}.png"
    os.makedirs("static", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    return {"url": f"/{out_path}"}
