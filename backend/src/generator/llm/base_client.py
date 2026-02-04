from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA


def build_qa_chain(llm,prompt_template, vector_store, output_parser, k=3):
    """
    Builds a RetrievalQA chain with structured output parsing.
    """
    print("----Building QA Chain----")
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        }
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": k}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain
