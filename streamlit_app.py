from config import st, json, openai, tool, ConversationSummaryBufferMemory, chardet, ChatOpenAI, llm
from function_calling import tools

# setting page config
st.set_page_config(
    page_title="HAILAB 진로 상담 챗봇💬",
    page_icon="🙌🏻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("진로 상담 챗봇💬")
st.caption('명성교회 디아스포라 청소년부와 함께할 AI 진로 상담사🥰')

# Chatbot.py
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.secrets["system_prompt"]},
        {"role": "assistant", "content": "안녕하세요! 저는 오늘 당신과 함께 진로 고민에 대해 이야기 나눠볼 AI 진로 상담사입니다.😊 제가 어떻게 불러주면 좋을까요?"}
    ]

# Initialize memory
if "memory" not in st.session_state:
     st.session_state.memory = ConversationSummaryBufferMemory(
          llm=llm,
          max_token_limit=1000,  # 요약의 기준이 되는 토큰 길이를 설정합니다.
          return_messages=True,
          )

# Display chat messages from history on app rerun
for message in st.session_state.messages:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 

if user_input := st.chat_input(): 
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner('Please wait...'):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            functions=tools,
            function_call="auto"
        )
        response_message = response.choices[0].message
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)
            if function_name == "SearchCareerInfo":
                # 함수 실행
                function_response = SearchCareerInfo(function_name)
                parsed_data = json.loads(function_response)
                for info in parsed_data['career_info']:
                    detected = chardet.detect(info['content'].encode())
                    decoded_content = info['content'].encode(detected['encoding']).decode('utf-8', errors='ignore') #한국어로 디코딩
                # 함수 응답을 메시지 이력에 추가
                st.session_state.messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": decoded_content
                })
                assistant_reply= openai.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                    )
                assistant_replys = assistant_reply.choices[0].message.content
            elif function_name == "SearchSeniorInfo":
                # 함수 실행
                #function_response = SearchSeniorInfo(function_name)
                function_response = SearchSeniorInfo(function_args["query"])
                # 함수 응답을 메시지 이력에 추가
                st.session_state.messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response["careersenior_info"]
                })
                assistant_reply= openai.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                assistant_replys = assistant_reply.choices[0].message.content
        else:        
            assistant_replys = response.choices[0].message.content
        # Add assistant response to chat history
        st.chat_message("assistant").write(assistant_replys)  
    st.session_state.messages.append({"role": "assistant", "content": assistant_replys})    
    st.session_state.memory.save_context(inputs={"user": user_input}, outputs={"assistant": assistant_replys})