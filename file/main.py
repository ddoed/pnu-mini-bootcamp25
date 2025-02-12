from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

html = """
<html>
    <head><title></title>
    <body>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="text" name="name" />
            <br />
            
            <input type="file" name="files" />
            <input type="file" name="files" />
            <input type="file" name="files" />
            
            <br /><br />
            <input type="submit" />
        </form>
    </body>
</html>
"""
@app.get('/')
def home():
    return HTMLResponse(html)

def save_file(files: dict[str, bytes]):
    for filename in files:
        fileData = files[filename]
        strPath = os.path.join('files', filename)
        try:
            with open(strPath, 'wb') as f:
                f.write(fileData)

        except Exception as e:
            print(e)
            continue

@app.post('/upload')
def upload(back_tasks: BackgroundTasks,
           files: list[UploadFile] | None = None):
    
    filesToSave: dict[str, bytes] = {}
    for file in files:
        if len(file.filename) < 1:
            continue
        filesToSave[file.filename] = file.file.read()

    back_tasks.add_task(save_file, filesToSave)

    return {
        'files': len(filesToSave)
    }