from fastapi import APIRouter, Depends, Form, HTTPException
from ..auth.route import authenticate
from .query import diagnosis_report
from ..config.db import reports_collection, diagnosis_collection
import time


router=APIRouter(prefix="/diagnosis",tags=['diagnosis'])


@router.post("/from_report")
async def diagnos(user=Depends(authenticate),doc_id:str=Form(...),question:str=Form(default="Please provide a diagnosis based on my report")):
    report=reports_collection.find_one({"doc_id":doc_id})
    if not report:
        raise HTTPException(status_code=404,detail="Report not found")
    #patient can only access
    if user["role"] == "patient" and report['uploader'] !=user["username"]:
       raise HTTPException(status_code=406,details="You cannot access another users report")
    
    #if user is apatient and want diagnosis from his own report
    if user["role"]=="patient":
        res=await diagnosis_report(user["username"],doc_id,question)
        #persist the diagnosis report
        diagnosis_collection.insert_one({
            "doc_id":doc_id,
            "requester":user['username'],
            "question":question,
            "answer":res.get("diagnosis"),
            "doc_id":res.get("sources",[]),
            "doc_id":time.time(),
        })
        return res
    
    #if the user is a doctor or other,they cant ask for diagnosis
    if user['role'] in ("doctor","admin"):
        raise HTTPException(status_code=407,detail="Doctors cannot access for diagnosis with this endpoint")
    
    raise HTTPException(status_code=408,detail='Unauthorized action')
    
@router.get("/by_patient_name")
async def get_patient_diagnosis(patient_name: str, user=Depends(authenticate)):
    # Only doctors can view a patient's diagnosis
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can access this endpoint")

    # Fetch records
    diagnosis_records = diagnosis_collection.find({"requester": patient_name})

    # Convert cursor to list
    records_list = []
    for record in diagnosis_records:
        record["_id"] = str(record["_id"])  # Convert ObjectId to string
        records_list.append(record)

    # Check if empty
    if not records_list:
        raise HTTPException(status_code=404, detail="No diagnosis found for this patient")

    return records_list
