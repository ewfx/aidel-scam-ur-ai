from typing import Annotated
import json
import io
import csv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from generateoutput import process_transaction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define request model for multi-line text input
class TransactionData(BaseModel):
    text: str

@app.post("/transaction_analysis")
async def upload_text(data: TransactionData):
    # Log the received text
    print("Received Multi-Line Text:\n", data.text)
    transaction_analysis=process_transaction(data.text)
    if(isinstance(transaction_analysis,dict)):
        return transaction_analysis
    else:
        return {"error":transaction_analysis}
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
    responses=[]
    for section in sections:
        transaction_analysis=process_transaction(section)
        if(isinstance(transaction_analysis,dict)):
            responses.append(transaction_analysis)
        else:
            responses.append({"error":transaction_analysis})
    # Convert and save as JSON file
    with open("transactions.json", "w", encoding="utf-8") as json_file:
        json.dump(responses, json_file, indent=4)
    return FileResponse(
        path="./transactions.json",
        filename="transactions.json",
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
    responses=[]
    for section in sections:
        transaction_analysis=process_transaction(section)
        if(isinstance(transaction_analysis,dict)):
            responses.append(transaction_analysis)
        else:
            responses.append({"error":transaction_analysis})
    
    # Find all unique keys across all dictionaries
    fieldnames = set()
    for item in responses:
        fieldnames.update(item.keys())
    fieldnames = list(fieldnames)  # Convert set to list for CSV headers

    # Write to CSV file
    with open("output.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write rows
        for row in responses:
            writer.writerow(row)  # Missing fields will be left blank in CSV

    print("CSV file 'output.csv' created successfully!")
    return FileResponse(
        path="./output.csv",
        filename="output.csv",
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

    # Convert each JSON row into multi-line text
    formatted_rows = [
        "\n".join(f"{key}: {value}" for key, value in row.items()) for row in rows
    ]

    # Log the multi-line formatted rows
    print("Processed Multi-Line Text:")
    responses=[]
    for row_text in formatted_rows:
        transaction_analysis=process_transaction(row_text)
        if(isinstance(transaction_analysis,dict)):
            responses.append(transaction_analysis)
        else:
            responses.append({"error":transaction_analysis})
    # Convert and save as JSON file
    with open("transactions.json", "w", encoding="utf-8") as json_file:
        json.dump(responses, json_file, indent=4)
    return FileResponse(
        path="./transactions.json",
        filename="transactions.json",
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
    # Convert each JSON row into multi-line text
    # Log the processed rows (You can replace this with actual storage or processing)
    print("Processed JSON rows:", json.dumps(rows, indent=4))
    formatted_rows = [
        "\n".join(f"{key}: {value}" for key, value in row.items()) for row in rows
    ]

    # Log the multi-line formatted rows
    print("Processed Multi-Line Text:")
    responses=[]
    for row_text in formatted_rows:
        transaction_analysis=process_transaction(row_text)
        if(isinstance(transaction_analysis,dict)):
            responses.append(transaction_analysis)
        else:
            responses.append({"error":transaction_analysis})
    
    # Find all unique keys across all dictionaries
    fieldnames = set()
    for item in responses:
        fieldnames.update(item.keys())
    fieldnames = list(fieldnames)  # Convert set to list for CSV headers

    # Write to CSV file
    with open("output.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write rows
        for row in responses:
            writer.writerow(row)  # Missing fields will be left blank in CSV

    print("CSV file 'output.csv' created successfully!")
    return FileResponse(
        path="./output.csv",
        filename="output.csv",
        media_type="application/octet-stream",
    )