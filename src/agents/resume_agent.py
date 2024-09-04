from lyzragentapi import LyzrAgentConfig

def resume_optimization_agent(APIKey, LyzrKey, resumeData, desiredJob, careerGoal, skillsExperience):
    Agent = LyzrAgentConfig(
            x_api_key=LyzrKey,
            llm_api_key=APIKey)

    Agent_Environment = Agent.create_environment(name="Resume Optimization",
                                                 features=[{
                                                            "type": "TOOL_CALLING",
                                                            "config": {"max_tries": 2},
                                                            "priority": 0
                                                        }],
                                                        tools=["perplexity_search"])

    agent_prompt = f"Optimize the resume to align with their desired job role, Career Goal and Sills/Experience. Analyze the current skills and experiences listed in the resume, identify any gaps compared to the skills required for the desired job, and suggest improvements. Tailor the resume content to highlight relevant strengths, and recommend additional skills or experiences the user should acquire to enhance their candidacy for the desired role."

    resume_agent = Agent.create_agent(
        env_id=Agent_Environment['env_id'],
        system_prompt=agent_prompt,
        name='Resume Optimization Agent'
    )

    response = Agent.send_message(
        agent_id=resume_agent['agent_id'],
        user_id="default_user",
        session_id="resume optimization session",
        message=f"Optimize this resume:{resumeData} based on these data Job Role:{desiredJob}, Career Goal:{careerGoal}, and skills/experice:{skillsExperience}. [!Important] Only provide recommendations, areas of improvement and exclude the conclusion, make sure data will be presented in bullets points refrence to the existing data")

    return response['response']