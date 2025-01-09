import os
import shutil

import numpy as np

from datetime import datetime
from datetime import timezone
import time

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import FastAPI, Form, UploadFile
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from ranking_service.src.rules import *
import json
from ranking_service.src.utils.util import check_for_content, get_current_utc_datetime
from ranking_service.src.utils import *
from ranking_service.src.utils import *
from ranking_service.src.utils.excel_handling import *
from ranking_service.src.team_agents.question_answer import *
from ranking_service.src.team_agents.skill_matching_agent import *
from ranking_service.src.team_agents.skill_matching_agent import *

router = APIRouter(
    prefix="/api",
    tags=[""]
)

server = 'ollama'
model = 'llama3.1'
model_endpoint = "http://localhost:11434/api/generate"

iterations = 40

print ("Creating graph and compiling workflow...")

graph = create_graph(server=server, model=model)
workflow = graph.compile()

graph = create_graph_matching_QA(server=server, model=model, model_endpoint=model_endpoint, state=qa_state)
qa_workflow = graph.compile()

print ("Graph and workflow created.")

@router.post("/matching_excell", status_code=status.HTTP_200_OK)
async def matching_excell(file: UploadFile = File(...)):
    try:
        # Kiểm tra xem file có phải là Excel không
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Please upload an Excel file."
            )
        
        # Đường dẫn lưu file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
        file_path = os.path.join(upload_dir, file.filename)

        # Lưu file vào thư mục
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        df, num_dynamic_col = read_candidate_file_with_questions(file_path)
        user_infors = map_to_userinfo(df=df, num_answers=num_dynamic_col)

        results = matching_array_resume(candidate_skills=user_infors, job_requirement_skill=job_description_requirement, skill_requirement_score=job_requirement_score, skill_workflow=workflow, weights=weights, qa_workflow=qa_workflow)
        
        return {
            "message": "File uploaded and saved successfully.",
            "results": results
        }

    except Exception as e:
        # Nếu có lỗi, trả về phản hồi lỗi
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
