import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.samplePaper import SamplePaper
from app.models.updateSamplePaper import UpdateSamplePaper
from app.connection import get_collection
from typing import List
from fastapi import HTTPException
from bson import ObjectId
import logging

router = APIRouter()
collection = get_collection()

@router.post("/papers", response_description="Adds new sample paper")
async def add_paper(samplePaper: SamplePaper):
    """
    Insert a new SamplePaper record.
    A unique `id` will be created and provided in the response.
    """

    try:
        
        new_sample_paper = collection.insert_one(
            samplePaper.model_dump()
        )
        
        response = {"id": str(new_sample_paper.inserted_id)}
        return JSONResponse(status_code=201, content= response)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))
    

@router.get("/papers/{paper_id}", response_description="Returns sample paper")
async def get_paper(paper_id: str):
    """
    Fetch a sample paper record by id.
    """

    try:
        paperId = ObjectId(paper_id)
        result = collection.find_one({"_id": paperId})

        if result is None:
            return JSONResponse(status_code=404, content={"message": "Sample paper not found"})
        
        result["_id"] = paper_id
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))
    
    
@router.put("/papers/{paper_id}", response_description="Partially updates sample paper")
async def update_paper(paper_id: str, samplePaper: UpdateSamplePaper):
    """
    Partially update a sample paper record.
    """

    try:
        paperId = ObjectId(paper_id)
        
        result = collection.update_one(
            {"_id": paperId},
            {"$set": samplePaper.model_dump(exclude_unset=True)},
        )

        if result.matched_count == 0:
            return JSONResponse(status_code=404, detail={"message": "Sample paper not found"})

        return JSONResponse(status_code=200, content={"id": paper_id, "message": "Updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))
    
    
@router.delete("/papers/{paper_id}", response_description="Deletes sample paper")
async def delete_paper(paper_id: str):
    """
    Delete a sample paper record.
    """

    try:
        paperId = ObjectId(paper_id)

        result = collection.delete_one({"_id": paperId})

        if result.deleted_count == 0:
            return JSONResponse(status_code=404, content={"message": "Sample paper not found"})

        return JSONResponse(status_code=200, content={"id": paper_id, "message": "Deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))