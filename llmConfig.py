class LLMConfig:
    Prompt = """
            You are an expert at analyzing content based on "work-life balance" providing an opinion on it.
            You will be given a piece of content, and you need to classify it.

            Content: {content}

            Output fields:
            - for_or_against: MUST be one of ["for", "against", "non-indicative"]. No other values are allowed.
            - employee_or_employer: MUST be one of ["employee", "employer", "non-indicative"].
            - promotional_or_opinion: MUST be one of ["promotional", "opinion", "non-indicative"].

            Examples:

            Example 1:
            Content: "Work-life balance is crucial for productivity and happiness."
            Output:
            {{
                "for_or_against": "for",
                "employee_or_employer": "non-indicative",
                "promotional_or_opinion": "opinion"
            }}

            Example 2:
            Content: "Companies should focus less on work-life balance and more on performance."
            Output:
            {{
                "for_or_against": "against",
                "employee_or_employer": "employer",
                "promotional_or_opinion": "opinion"
            }}

            Example 3:
            Content: "Looking for a job with great work-life balance? Apply now!"
            Output:
            {{
                "for_or_against": "for",
                "employee_or_employer": "non-indicative",
                "promotional_or_opinion": "promotional"
            }}

            Your response should ONLY be in JSON format, following this structure:
            {{
                "for_or_against": "[for/against/non-indicative]",
                "employee_or_employer": "[employee/employer/non-indicative]",
                "promotional_or_opinion": "[promotional/opinion/non-indicative]"
            }}

            {format_instructions}
            """

    LLM_MODEL = "llama3"