from typing import Optional

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import Settings
from app.rag.agent import plan_tools, run_tools
from app.rag.prompt import build_prompt


def review_code(
    settings: Settings,
    code: str,
    language: Optional[str] = None,
    file_path: Optional[str] = None,
) -> str:
    _ = language
    _ = file_path

    tools = plan_tools(code)
    tool_outputs = {}
    if "retrieve_docs" in tools:
        tool_outputs = run_tools(settings, code)

    prompt = build_prompt()
    llm = Ollama(base_url=settings.ollama_base_url, model=settings.ollama_model)

    chain = (
        RunnablePassthrough.assign(context=lambda _: tool_outputs.get("context", ""))
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"code": code})
