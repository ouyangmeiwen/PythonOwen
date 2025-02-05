#pip install python-multipart
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
from pathlib import Path

router_file = APIRouter()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 上传文件
@router_file.post("/files/upload/", tags=["files"])
async def upload_file(file: UploadFile = File(...)):

    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if file.size > 5 * 1024 * 1024:  # 限制大小为 5 MB
        raise HTTPException(status_code=400, detail="File too large")
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "file_size": file.size}

# 下载文件
@router_file.get("/files/download/{filename}", tags=["files"])
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@router_file.get("/files/list", tags=["files"])
async def list_files():
    files = [file.name for file in UPLOAD_DIR.iterdir() if file.is_file()]
    return {"files": files}
