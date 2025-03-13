from google import genai
import wikipediaapi
import wikipedia
import re
import os
from dotenv import load_dotenv


load_dotenv()
genai_key = os.getenv("GENAI_API_KEY")
AI_con = genai.Client(api_key=genai_key)

if not genai_key:
    raise ValueError("No API keys found.")


def llm_query(user_claim):
    try:
        prompt = f'{user_claim} Answer with True or False first, then a very short explanation (1 sentence).'
        AI_res = AI_con.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        llm_response = AI_res.text
        print(f"\nGemini response: {llm_response}")

        match = re.match(r"(True|False|Uncertain)\b", llm_response, re.IGNORECASE)

        if match:
            llm_truth = match.group(1).lower()
            llm_explanation = llm_response[len(match.group(1)):].strip()

        else:
            llm_truth = "uncertain"
            llm_explanation = llm_response

        fact_check(user_claim, llm_truth, llm_explanation)

    except Exception as e:
        print(f"Error querying Gemini: {e}")
        print("Final Decision: API Error)")


def wiki_search(claim):
    match = re.search(r"(.*?)\s(?:is|was|are|were|has|have)\s", claim)

    if match:
        keywords = match.group(1).strip()

    else:
        parts = claim.split(" is ", 1)
        keywords = parts[0].strip()

    wiki_wiki = wikipediaapi.Wikipedia(user_agent="fact_checker/1.0", language="en")
    page = wiki_wiki.page(keywords)

    if not page.exists():
        try:
            search_results = wikipedia.search(keywords)

            if search_results:
                page = wiki_wiki.page(search_results[0])

        except Exception as e:
            print(f"WIkipedia search error: {e}")
            return "No relevant Wikipedia data found."

    if not page.exists():
        return "No Wikipedia data found."

    summary = page.summary.split(". ")

    if len(summary) < 3:
        sections = list(page.sections)
        for section in sections[:2]:
            if section.text:
                additional_text = section.text.split(". ")[:5]
                summary.extend(additional_text)

                if len(summary) >= 5:
                    break

    return summary[:7]


def check_with_gemini(claim, wiki_content):
    if not wiki_content or wiki_content[0] == "No relevant Wikipedia data found.":
        return "uncertain (No Wikipedia data)"

    wiki_text = ". ".join(wiki_content)

    prompt = f"""
    Claim: "{claim}"
    Wikipedia Text: "{wiki_text}"

    Based ONLY on the Wikipedia text provided, is the claim true, false, or uncertain?
    Answer with "True" if confirmed, "False" if contradicted, or "Uncertain" if the Wikipedia text doesn't 
    provide enough information to verify the claim. Then give a short explanation.
    """

    try:
        AI_res = AI_con.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        check_response = AI_res.text

        match = re.match(r"(True|False|Uncertain)\b", check_response, re.IGNORECASE)

        if match:
            wiki_truth = match.group(1).lower()
            wiki_explanation = check_response[len(match.group(1)):].strip()

        else:
            wiki_truth = "uncertain"
            wiki_explanation = check_response

        return wiki_truth, wiki_explanation

    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return "uncertain"


def fact_check(user_claim, llm_truth, llm_explanation):
    wiki_content = wiki_search(user_claim)
    print(f"Wikipedia info:, {wiki_content} \n")

    if not wiki_content or wiki_content[0] == "No Wikipedia data found.":
        print("Final Decision: UNCERTAIN (No Wikipedia data found)")
        return

    wiki_truth, wiki_explanation = check_with_gemini(user_claim, wiki_content)

    if wiki_truth == "uncertain" or llm_truth == "uncertain":
        final_decision = "UNCERTAIN (Missing or unclear information)"

    elif llm_truth == wiki_truth:
        final_decision = "TRUE (LLM and Wikipedia agree)"

    else:
        final_decision = "FALSE (LLM and Wikipedia contradict)"

    print(f"Final Decision: {final_decision}")


user_claim = input("Write the claim: ")
llm_query(user_claim)