from config import st, os, TavilySearchResults, TavilySearchAPIWrapper, tool, json
from config import OPENAI_API_KEY, persist_dir

#----------------------------------------------------------------------------------------------------
# function calling
# ----------------------------------------------------------------------------------------------------
# 현재 작업 디렉토리 가져오기
current_directory = os.getcwd()

# 안전한 경로 설정 (배포 환경에서도 유지됨)
persist_dir = os.path.join(current_directory, "career_saramin")

@tool
def SearchCareerInfo(query):
    """Get the current carrer_info in a given url"""
    career_info = None
    tavily_search = TavilySearchAPIWrapper(tavily_api_key=st.secrets['TAVILY_API'])
    # 쿼리 작성
    url = "https://www.work.go.kr/consltJobCarpa/srch/getExpTheme.do?jobClcd=D&pageIndex=1&pageUnit=10"

    # TavilySearchAPIWrapper를 이용하여 검색 결과 가져오기
    search_results = TavilySearchResults(max_results=5, tavily_api_key=st.secrets['TAVILY_API']).invoke(query)
    career_info = {
        "name": career_info,
        "query": query,
        "career_info": search_results,
    }
    return json.dumps(career_info)

tools = [
    {
        "name": "SearchCareerInfo",
        "description": "A tool that search the information needed to generate job information according to the prompt based on the given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look for specific Career information."
                },            
            },
            "required": ["query"]
        },
    }
]