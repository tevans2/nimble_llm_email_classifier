import os
from dotenv import load_dotenv
import requests

load_dotenv()
FLOWISE_API_KEY = os.environ["FLOWISE_API_KEY"]

# ENSURE that these variables are applicable to the Flowise instance you are using
BASE_URL = "http://ec2-54-157-250-153.compute-1.amazonaws.com:3000/api/v1/prediction/"  # EC2 instance hosting flowise
CATEGORIZE_FLOW_ID = (
    "2425dc03-0ba7-4a11-a067-df32250806e4"  # Flowise Categorize Flow ID
)
REPLY_FLOW_ID = "2aef9ca7-174c-4994-b26f-d9c3e7ede6dc"  # Flowise Reply Flow ID


# Categorize email body based on categories in categories.txt
def llm_categorize(phrase: str, file_path):
    headers = {"Authorization": f"Bearer {FLOWISE_API_KEY}"}
    payload = {"question": phrase}

    CATEGORIZE_API_URL = BASE_URL + CATEGORIZE_FLOW_ID

    # Categorizes and converts to digit
    response = requests.post(CATEGORIZE_API_URL, headers=headers, json=payload)
    index = response.json()
    index = index["text"].replace(" ", "")

    categories_dict = load_categories(file_path)
    if index.isdigit() and 1 <= int(index) <= len(categories_dict):
        index = int(index)

        # Converts category number to category name
        if 0 < index <= len(categories_dict):
            category_name = categories_dict[index]
            return category_name
        else:
            return "invalid"

    else:
        return "invalid"


def llm_reply(phrase, category):
    payload = {
        "question": category,
        "overrideConfig": {
            "promptValues": {
                "email_body": phrase,
            }
        },
    }

    headers = {"Authorization": f"Bearer {FLOWISE_API_KEY}"}

    REPLY_API_URL = BASE_URL + REPLY_FLOW_ID

    response = requests.post(REPLY_API_URL, headers=headers, json=payload)
    answer = response.json()
    answer = answer["text"]
    return answer


# Loads indexed categories from text file
def load_categories(file_path):
    categories_dict = {}

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                number, category_name = line.split(".", 1)
                categories_dict[int(number)] = category_name.strip()

    return categories_dict
