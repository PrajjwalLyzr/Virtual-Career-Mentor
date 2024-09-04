from lyzragentapi import LyzrAgentConfig

def job_search_agent(APIKey, LyzrKey, searchJobData, candiateSummary):
    Agent = LyzrAgentConfig(
            x_api_key=LyzrKey,
            llm_api_key=APIKey)

    Agent_Environment = Agent.create_environment(name="Job Search",
                                                 features=[{
                                                            "type": "TOOL_CALLING",
                                                            "config": {"max_tries": 2},
                                                            "priority": 0
                                                        }],
                                                        tools=["perplexity_search"])

    agent_prompt = f"Given the following job search results and a candidate's resume summary, identify which job descriptions or qualifications match the candidate's resume summary. Consider the matching based on relevance to skills, experience, and job roles. Return a new JSON containing only those job listings with their description, qualifications, and apply links where there is a match between the candidate's resume summary and the job description or qualifications."

    resume_agent = Agent.create_agent(
        env_id=Agent_Environment['env_id'],
        system_prompt=agent_prompt,
        name='Job Search Agent'
    )

    response = Agent.send_message(
        agent_id=resume_agent['agent_id'],
        user_id="default_user",
        session_id="resume optimization session",
        message=f"""
                    Job Search Results (JSON): {searchJobData}

                    Candidate Resume Summary: {candiateSummary}

                    Please extract and filter the job listings where the job description or qualifications align with the candidate's resume summary. The output should be a JSON that includes only the relevant job listings with their description, qualifications, and apply link. [!Important] Don't provide anything other than JSON Object, just pure JSON object remove any prefix if have.

                    Output JSON will be:    {{ 
                                                "matching_jobs": [
                                                    {{
                                                        "title": {{"Job Title"}},
                                                        "description":{{"Job Description"}},
                                                        "qualifications":{{"Required Qualifications"}}
                                                        "company_name": {{"Company Name"}},
                                                        "apply_link": {{"Apply link"}}
                                                    }},
                                                    {{
                                                        "title": {{"Job Title"}},
                                                        "description":{{"Job Description"}},
                                                        "qualifications":{{"Required Qualifications"}}
                                                        "company_name": {{"Company Name"}},
                                                        "apply_link": {{"Apply link"}}
                                                    }},
                                                    {{
                                                        "title": {{"Job Title"}},
                                                        "description":{{"Job Description"}},
                                                        "qualifications":{{"Required Qualifications"}}
                                                        "company_name": {{"Company Name"}},
                                                        "apply_link": {{"Apply link"}}
                                                    }},
                                                    {{
                                                        "title": {{"Job Title"}},
                                                        "description":{{"Job Description"}},
                                                        "qualifications":{{"Required Qualifications"}}
                                                        "company_name": {{"Company Name"}},
                                                        "apply_link": {{"Apply link"}}
                                                    }},
                                                    {{
                                                        "title": {{"Job Title"}},
                                                        "description":{{"Job Description"}},
                                                        "qualifications":{{"Required Qualifications"}}
                                                        "company_name": {{"Company Name"}},
                                                        "apply_link": {{"Apply link"}}
                                                    }},
                                                ]}}
                """
                    )
    return response['response']