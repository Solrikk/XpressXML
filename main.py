from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/uploaded_files",
          StaticFiles(directory="uploaded_files"),
          name="uploaded_files")

os.makedirs("uploaded_files", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <head>
            <title>Upload File</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    width: 50%;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                }
                form {
                    text-align: center;
                }
                input[type="file"] {
                    display: block;
                    margin: 10px auto;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Upload File</h1>
                <form action="/upload/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".xml">
                <input type="submit" value="Upload">
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploaded_files/{file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())

    server_url = "https://YOURURL.com.app"
    file_url = f"{server_url}/uploaded_files/{file.filename}"
    return {"url": file_url}
