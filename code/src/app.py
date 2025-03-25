from typing import Annotated
import json
import io
import csv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
app = FastAPI()


@app.post("/txt_to_json")
async def unstructured_transaction_to_json(file: UploadFile = File(...)):
    # Ensure the uploaded file is a .txt file
    if not file.filename.endswith(".txt"):
        return {"error": "Only .txt files are allowed"}
    # Read and decode the uploaded file
    contents = await file.read()
    text = contents.decode("utf-8")

    # Split the text into chunks based on the "---" delimiter
    sections = [section.strip() for section in text.split("---") if section.strip()]

    # Log the processed sections (You can replace this with actual storage or processing)
    print("Processed sections:", sections)
    print("Number of sections:" , len(sections))
    return FileResponse(
        path="./requirements.txt",
        filename="requirements.txt",
        media_type="application/octet-stream",
    )

@app.post("/txt_to_csv")
async def unstructured_transaction_to_csv(file: UploadFile = File(...)):
    # Ensure the uploaded file is a .txt file
    if not file.filename.endswith(".txt"):
        return {"error": "Only .txt files are allowed"}
    
    # Read and decode the uploaded file
    contents = await file.read()
    text = contents.decode("utf-8")

    # Split the text into chunks based on the "---" delimiter
    sections = [section.strip() for section in text.split("---") if section.strip()]

    return FileResponse(
        path="./requirements.txt",
        filename="requirements.txt",
        media_type="application/octet-stream",
    )

@app.post("/csv_to_json")
async def structured_transaction_to_json(file: UploadFile = File(...)):
    # Ensure the uploaded file is a .txt file
    if not file.filename.endswith(".csv"):
        return {"error": "Only .csv files are allowed"}
    
    # Read the uploaded CSV file
    contents = await file.read()
    text_io = io.StringIO(contents.decode("utf-8"))

    # Process CSV into JSON
    reader = csv.DictReader(text_io)
    rows = [row for row in reader]

    # Log the processed rows (You can replace this with actual storage or processing)
    print("Processed JSON rows:", json.dumps(rows, indent=4))

    return FileResponse(
        path="./requirements.txt",
        filename="requirements.txt",
        media_type="application/octet-stream",
    )

@app.post("/csv_to_csv")
async def unstructured_transaction_to_csv(file: UploadFile = File(...)):
    # Ensure the uploaded file is a .txt file
    if not file.filename.endswith(".csv"):
        return {"error": "Only .csv files are allowed"}
    
    # Read the uploaded CSV file
    contents = await file.read()
    text_io = io.StringIO(contents.decode("utf-8"))

    # Process CSV into JSON
    reader = csv.DictReader(text_io)
    rows = [row for row in reader]

    # Log the processed rows (You can replace this with actual storage or processing)
    print("Processed JSON rows:", json.dumps(rows, indent=4))
    
    return FileResponse(
        path="./requirements.txt",
        filename="requirements.txt",
        media_type="application/octet-stream",
    )