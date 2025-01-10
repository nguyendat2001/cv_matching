import json
# import logging

from langchain_core.messages import HumanMessage

from .user_job_class import *
from ranking_service.src.team_agents.skill_matching_agent.agents import *
from ranking_service.src.team_agents.skill_matching_agent.prompts import *
from ranking_service.src.team_agents.skill_matching_agent.json_guide import *

server = 'ollama'
model = 'llama3.1'
model_endpoint = "http://localhost:11434/api/generate"

def skill_analysis(candidate_skill:List, job_description_requirement:List, scoring_board, skill_workflow):
    dict_inputs={
        "user_component_skills":candidate_skill,
        "job_description_component_skills":job_description_requirement,
        "scoring_board":scoring_board,
    }
    print("dict_inputs: ",dict_inputs)
    final_state = skill_workflow.invoke(dict_inputs)
    return final_state.get('final_reports', None)
    # skill_workflow_infer()

def qa_analysis(user_answer:str, correct_answer:str, qa_workflow):
    dict_inputs = {"user_answer": user_answer,
               "correct_answer": correct_answer}
    print("dict_inputs: ",dict_inputs)
    final_state = qa_workflow.invoke(dict_inputs)
    return json.loads(final_state.get('final_reports', None)[0].content)

def get_content_json_value(input_data):
    """
    Extracts JSON content from the input data, specifically handling
    nested structures within HumanMessage objects.

    Args:
        input_data: The input data.

    Returns:
        The extracted JSON content or the original input data if extraction fails.
    """
    try:
        # Check if input_data is a HumanMessage
        if isinstance(input_data, HumanMessage):
            content = json.loads(input_data.content)
            return content

        # Check if input_data is a list and the first element is a HumanMessage
        if isinstance(input_data, list) and len(input_data) > 0 and isinstance(input_data[0], HumanMessage):
            print("HumanMessage")
            print(input_data[0].content)
            return json.loads(input_data[0].content)

        # If input_data is a string, try to load it as JSON directly
        if isinstance(input_data, str):
            return json.loads(input_data)

        # If input_data has a 'content' attribute, try to load its content as JSON
        if hasattr(input_data, 'content'):
            return json.loads(input_data.content)

        # If none of the above conditions apply, return the input_data as is
        return input_data

    except (json.JSONDecodeError, TypeError, IndexError, KeyError):
        print(f"Warning: Failed to extract JSON content from input: {input_data}")
        return input_data

def get_score(data):

    try:
        # Check if data is already a dictionary
        if data["scoring_with_board"] is not None:
            return json.loads(data["scoring_with_board"])["assign_score_final"]
        else:  # If it's a JSON string, load it
            return data["matcher_value_response"]["assign_score_final"]
    except (KeyError, TypeError) as e:
        print(f"Warning: Could not find the required keys in the input data or encountered a TypeError: {e}")
        # Handle the error (e.g., return a default value, raise an exception)
        return None  # Or raise an exception if appropriate

def get_comment(data):
    try:
        # Check if data is already a dictionary
        if data["scoring_with_board"] is not None:
            return json.loads(data["scoring_with_board"])["comment"]
        else:  # If it's a JSON string, load it
            return data["matcher_value_response"]["comment"]
    except (KeyError, TypeError) as e:
        print(f"Warning: Could not find the required keys in the input data or encountered a TypeError: {e}")
        # Handle the error (e.g., return a default value, raise an exception)
        return None  # Or raise an exception if appropriate


def resume_analysis(candidate_skill:UserInfo, job_requirement_skill:JobDescription, skill_requirement_score:SkillRequirementScore, weights, skill_workflow, qa_workflow):
    degree = skill_analysis(candidate_skill=candidate_skill["degree"],
                            job_description_requirement=job_requirement_skill["degree"],
                            scoring_board=skill_requirement_score["degree"],
                            skill_workflow=skill_workflow)

    university = skill_analysis(candidate_skill=candidate_skill["university"],
                                job_description_requirement=None,
                                scoring_board=skill_requirement_score["university"],
                                skill_workflow=skill_workflow)

    # year_experience = skill_analysis(candidate_skill=candidate_skill["year_experience"],
    #                                  job_description_requirement=job_requirement_skill["year_experience"],
    #                                  scoring_board=None,
    #                                  skill_workflow=skill_workflow)

    technical_skill = skill_analysis(candidate_skill=candidate_skill["technical_skill"],
                                     job_description_requirement=job_requirement_skill["technical_skill"],
                                     scoring_board=None,
                                     skill_workflow=skill_workflow)

    certificate = skill_analysis(candidate_skill=candidate_skill["certificate"],
                                 job_description_requirement=None,
                                 scoring_board=skill_requirement_score["certificate"],
                                 skill_workflow=skill_workflow)

    soft_skill = skill_analysis(candidate_skill=candidate_skill["soft_skill"],
                                job_description_requirement=job_requirement_skill["soft_skill"],
                                scoring_board=None,
                                skill_workflow=skill_workflow)

    english_level = skill_analysis(candidate_skill=candidate_skill["english_level"],
                                   job_description_requirement=None,
                                   scoring_board=skill_requirement_score["english_level"],
                                   skill_workflow=skill_workflow)

    year_experience = MatchingExperienceAgent(
              state=None,
              model=model,
              server=server,
              guided_json=matching_experience_guided_json,
              stop=None,
              model_endpoint=model_endpoint,
              temperature=None
          ).invoke(
              candidate_experience = candidate_skill["year_experience"],
              job_experience = job_requirement_skill["year_experience"],
              prompt_template=matching_experience_prompt_template
          )

    responsibility = MatchingResponsibilityAgent(
              state=None,
              model=model,
              server=server,
              guided_json=matching_responsibility_guided_json,
              stop=None,
              model_endpoint=model_endpoint,
              temperature=None
          ).invoke(
              candidate_responsibilities = candidate_skill["responsibility"],
              job_responsibilities = job_requirement_skill["responsibility"],
              prompt=matching_responsibility_prompt_template
          )

    num_correct_answers = len([field for field in job_requirement_skill if field.startswith("correct_answer_")])
    correct_answers = []
    for index in range(1, num_correct_answers + 1):
        correct_answer = qa_analysis(user_answer=candidate_skill[f"answer_{index}"],
                                      correct_answer=job_requirement_skill[f"correct_answer_{index}"],
                                      qa_workflow=qa_workflow)
        correct_answers.append(correct_answer)


    degree = get_content_json_value(degree)
    university = get_content_json_value(university)
    technical_skill = get_content_json_value(technical_skill)
    certificate = get_content_json_value(certificate)
    soft_skill = get_content_json_value(soft_skill)
    english_level = get_content_json_value(english_level)
    year_experience = get_content_json_value(year_experience)
    responsibility = get_content_json_value(responsibility)

    print("responsibility: ",responsibility)
    print("year_experience: ",year_experience)

    print("degree: ",get_score(degree))
    print("university: ",get_score(university))
    print("technical_skill: ",get_score(technical_skill))
    print("certificate: ",get_score(certificate))
    print("soft_skill: ",get_score(soft_skill))
    print("english_level: ",get_score(english_level))
    print("responsibility: ",responsibility["average_matching_percentage"])
    print("year_experience: ",year_experience["average_experience_percentage"])

    final_score = weights["degree"] * float(get_score(degree)) + \
                  weights["university"] * float(get_score(university)) + \
                  weights["technical_skill"] * float(get_score(technical_skill)) + \
                  weights["certificate"] * float(get_score(certificate)) + \
                  weights["soft_skill"] * float(get_score(soft_skill)) + \
                  weights["english_level"] * float(get_score(english_level)) + \
                  weights["responsibility"] * float(responsibility["average_matching_percentage"]) + \
                  weights["year_experience"] * float(year_experience["average_experience_percentage"])

    comment = "degree: "+ (get_comment(degree) or "") +"\n"
    comment += "university: " + (get_comment(university) or "") +"\n"
    comment += "technical_skill: " + (get_comment(technical_skill) or "") +"\n"
    comment += "certificate: " + (get_comment(certificate) or "") +"\n"
    comment += "soft_skill: " + (get_comment(soft_skill) or "") +"\n"
    comment += "english_level: " + (get_comment(english_level) or "") +"\n"
    comment += "responsibility: " + (responsibility["comment"] or "") +"\n"
    comment += "year_experience: " + (year_experience["comment"] or "") +"\n"

    # ranking_score = {
    #     "degree": degree,
    #     "university": university,
    #     "technical_skill": technical_skill,
    #     "certificate": certificate,
    #     "soft_skill": soft_skill,
    #     "english_level": english_level,
    #     "year_experience": year_experience,
    #     "final_score": final_score,
    #     "comment": comment,
    # }

    ranking_score = {
        "name": candidate_skill["name"],
        "date_of_birth": candidate_skill["date_of_birth"],
        "position": candidate_skill["position"],
        "email": candidate_skill["email"],
        "phone_number": candidate_skill["phone_number"],
        "degree": get_score(degree),
        "university": get_score(university),
        "technical_skill": get_score(technical_skill),
        "certificate": get_score(certificate),
        "soft_skill": get_score(soft_skill),
        "english_level": get_score(english_level),
        "responsibility": responsibility["average_matching_percentage"],
        "year_experience": year_experience["average_experience_percentage"],
        "final_score": final_score,
        "comment": comment,
        "answer_matching": correct_answers,
    }
    return ranking_score

def matching_array_resume(candidate_skills: List[UserInfo], job_requirement_skill: JobDescription, skill_requirement_score: SkillRequirementScore, weights, skill_workflow, qa_workflow):
    import time 
    
    candidate_matching_responses = []
    error_thresh = 3  # Set the number of retries

    for candidate_skill in candidate_skills:
        start = time.time()
        candidate_skill = candidate_skill.model_dump(exclude_unset=True)
        candidate_skill = json.dumps(candidate_skill)
        candidate_skill_dict = json.loads(candidate_skill)

        for attempt in range(error_thresh):
            try:
                candidate_matching_response = resume_analysis(candidate_skill=candidate_skill_dict, job_requirement_skill=job_requirement_skill, skill_requirement_score=skill_requirement_score, skill_workflow=skill_workflow, weights=weights, qa_workflow=qa_workflow)
                candidate_matching_responses.append(candidate_matching_response)
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error during resume_analysis (Attempt {attempt + 1}/{error_thresh}): {e}")
                if attempt < error_thresh - 1:
                    print("Retrying...")
                    # You might want to add a delay here using time.sleep()
                else:
                    print("Maximum retries reached. Skipping this candidate skill.")
        print("-"*50)
        print(f"Execution time: {time.time() - start} seconds")
        print("-"*50)
    return candidate_matching_responses