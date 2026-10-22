import os
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# --------------------------------------------------
# MODEL
# --------------------------------------------------

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    temperature=0
)

# --------------------------------------------------
# CLASSIFICATION OUTPUT SCHEMA
# --------------------------------------------------

class Classification(BaseModel):
    category: Literal[
        "delayed",
        "damaged",
        "lost",
        "unknown"
    ] = Field(
        description="The shipment exception category."
    )


# --------------------------------------------------
# CHAIN 1: CLASSIFY EXCEPTION
# --------------------------------------------------

classify_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You classify shipment exception reports.

        Choose exactly one category:

        - delayed: The shipment is late or delivery is overdue.
        - damaged: The shipment or its contents are damaged.
        - lost: The shipment is missing or cannot be located.
        - unknown: The report is garbled, unintelligible, or
          does not provide enough information to classify reliably.

        Do not invent facts.
        If the report cannot be reliably classified, choose unknown.
        """
    ),
    (
        "human",
        "Shipment exception report:\n{report}"
    )
])

classify_chain = (
    classify_prompt
    | llm.with_structured_output(Classification)
)


# --------------------------------------------------
# CHAIN 2: DRAFT ESCALATION NOTE
# --------------------------------------------------

escalate_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an operations analyst preparing an internal
        shipment exception escalation note for a manager.

        Include:
        1. The original problem.
        2. The classification.
        3. Shipment value.
        4. Calculated compensation.
        5. Why human review is required.
        6. Recommended next steps.

        Be concise, factual, and professional.
        Do not invent information.
        """
    ),
    (
        "human",
        """
        Original report:
        {report}

        Category: {category}
        Shipment value: {shipment_value}
        Compensation: {compensation}
        Customer tier: {customer_tier}
        Escalation reason: {escalation_reason}
        """
    )
])

escalate_chain = escalate_prompt | llm


# --------------------------------------------------
# CHAIN 3: DRAFT CUSTOMER EMAIL
# --------------------------------------------------

email_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You write professional customer-service emails for
        Northwind Logistics.

        Explain the shipment issue and the compensation outcome.

        Be polite, clear, and empathetic.

        Do not promise refunds, reimbursements, or actions
        beyond the supplied compensation decision.

        Do not invent delivery dates or other facts.
        """
    ),
    (
        "human",
        """
        Original report:
        {report}

        Category: {category}
        Shipment value: {shipment_value}
        Compensation: {compensation}
        Customer tier: {customer_tier}
        """
    )
])

draft_email_chain = email_prompt | llm