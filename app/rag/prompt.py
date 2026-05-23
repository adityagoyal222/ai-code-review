from langchain_core.prompts import ChatPromptTemplate


def build_prompt() -> ChatPromptTemplate:
    system = (
        "You are a senior code reviewer. Use ONLY the provided context to justify findings. "
        "If the context does not support a claim, say it is not supported. "
        "Cite sources using the provided [source:...#chunkN] tags."
    )

    human = (
        "CODE:\n{code}\n\n"
        "CONTEXT:\n{context}\n\n"
        "Return a Markdown review with these sections:\n"
        "1. Summary\n"
        "2. Findings (bullets with citations)\n"
        "3. Risks (bullets with citations)\n"
        "4. Suggested Fixes (bullets, cite when grounded)\n"
        "5. Grounding Notes (state any uncertainty or missing context)\n"
    )

    return ChatPromptTemplate.from_messages([("system", system), ("human", human)])
