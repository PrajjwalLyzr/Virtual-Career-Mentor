import requests
import json
import streamlit as st

class LyzrAgentConfig:
    def __init__(self, x_api_key, llm_api_key):
        self.url = "https://agent.api.lyzr.app/v2/"
        self.headers = {
            "accept": "application/json",
            "x-api-key": x_api_key
        }
        self.llm_api_key = llm_api_key

    def create_environment(self, name, features, tools=None):
        payload = json.dumps({
            "name": name,
            "features": features,
            "tools": tools,
            "llm_config": {
                            "provider": "openai",
                            "model": "gpt-4o-mini",
                            "config": {
                                "temperature": 0.5,
                                "top_p": 0.9
                            },
            "llm_api_key": self.llm_api_key
        }})

        url = self.url + "environment"

        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    def create_agent(self, env_id, system_prompt, name):
        payload = json.dumps({
            "env_id": env_id,
            "system_prompt": system_prompt,
            "name": name,
            "agent_persona": "",
            "agent_instructions": "",
            "agent_description": ""
        })

        url = self.url + "agent"

        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    def send_message(self, agent_id, user_id, session_id, message):
        payload = json.dumps({
            "user_id": user_id,
            "agent_id": agent_id,
            "session_id": session_id,
            "message": message
        })

        url = self.url + "chat/"

        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    def create_task(self, agent_id, session_id, input_message):
        payload = json.dumps({
            "agent_id": agent_id,
            "session_id": session_id,
            "input": input_message
        })

        url = self.url + "task"

        response = requests.post(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None