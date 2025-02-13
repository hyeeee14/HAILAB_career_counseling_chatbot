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

@tool
def SearchSeniorInfo(query):
    """Get the current Senior_info in RAG"""
    senior_info = None
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # load from disk (save 이후)

    try:
        vector = Chroma(persist_directory=persist_dir, embedding_function=embedding, collection_name="career_saramin")
        print("ChromaDB 문서 개수:", vector._collection.count())
    except Exception as e:
        print("Error Loading ChromaDB:", e)
    # ✅ RAG 기반 검색 수행
    search_results = vector.similarity_search(query, k=3)  # 🔥 상위 1개 문서 검색
    # page_content만 리스트로 추출
    page_contents = [doc.page_content for doc in search_results]

    senior_info = {
        "name": "senior_info",
        "query": query,
        "careersenior_info": page_contents,
    }
    return senior_info