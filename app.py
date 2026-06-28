import streamlit as st
import json
from main import call_llm, run_tool
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

st.title("🌍 Country Information Agent")
st.write("Ask me anything about any country!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Function to render messages
def render_messages():
    for message in st.session_state.messages:
        # Don't render system prompt
        if message["role"] == "system":
            continue
            
        # Handle tool messages
        if message["role"] == "tool":
            with st.status(f"Tool Result ({message.get('name', 'Unknown')})", state="complete"):
                st.write(message["content"])
            continue
            
        # Handle assistant messages with tool calls
        if message["role"] == "assistant" and message.get("tool_calls"):
            for tool_call in message["tool_calls"]:
                with st.status(f"Calling tool: {tool_call['function']['name']}", state="complete"):
                    st.write(f"Arguments: {tool_call['function']['arguments']}")
            
            # If the message also has content, display it
            if message.get("content"):
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
            continue

        # Render normal user/assistant messages
        if message.get("content"):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

render_messages()

# React to user input
if prompt := st.chat_input("Ask me about a country..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call the LLM
    with st.spinner("Thinking..."):
        max_steps = 5
        
        for step in range(max_steps):
            try:
                result = call_llm(st.session_state.messages)
                message = result["choices"][0]["message"]
                
                # Append the raw message for history
                st.session_state.messages.append(message)
                
                # If there's content, display it
                if message.get("content"):
                    with st.chat_message("assistant"):
                        st.markdown(message["content"])

                # Handle tool calls
                if "tool_calls" in message and message["tool_calls"]:
                    for tool_call in message["tool_calls"]:
                        tool_name = tool_call["function"]["name"]
                        with st.status(f"Running tool: {tool_name}", expanded=True) as status:
                            st.write(f"Arguments: {tool_call['function']['arguments']}")
                            tool_result = run_tool(tool_call)
                            st.write(f"Result: {tool_result}")
                            status.update(label=f"Tool Result ({tool_name})", state="complete", expanded=False)
                        
                        tool_msg = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": tool_name,
                            "content": tool_result
                        }
                        st.session_state.messages.append(tool_msg)
                else:
                    break
            except Exception as e:
                st.error(f"An error occurred: {e}")
                break
