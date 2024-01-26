from unicodedata import category
from dotenv import load_dotenv
from urllib import response
import requests
import json
from bs4 import BeautifulSoup
from time import sleep
import sys
import os
from llm_actions import llm_categorize, llm_reply

# For Nimble Fresh Account:
# BASE_URL = "https://nimblegroupservicedesk.freshservice.com/api/v2"

# For Tate Fresh Account
BASE_URL = "https://tateinc.freshdesk.com/api/v2"

FRESH_API_KEY = os.environ["TATEINC_API_KEY"]
PASSWORD = "123"  # not needed
URL = BASE_URL + "/tickets"
NON_REPLY_CATEGORIES = ["Spam", "Human Review"]


# fetches most recent tickets without filtering
def fetch_all_tickets():
    # query_params = {"include": "department"}

    response = requests.get(URL, auth=(FRESH_API_KEY, PASSWORD))

    if response.status_code == 200:
        tickets = json.loads(response.content)
        for ticket in tickets["tickets"]:
            subject = ticket["subject"]
            body = ticket["description_text"]

            print(ticket["id"])
            print(subject)
            print(body)
            print("")
    else:
        print(f"Failed to fetch tickets. Status code: {response.status_code}")


# fetches all tickets NOT labled as auto_classified
def fetch_unprocessed_tickets():
    url_query = 'query="cf_auto_classified:false"'
    FILTER_URL = BASE_URL + "/search/tickets?" + url_query

    response = requests.get(FILTER_URL, auth=(FRESH_API_KEY, PASSWORD))

    if response.status_code == 200:
        response_data = json.loads(response.content)
        tickets = response_data["results"]

        return tickets
    else:
        return None


# label ticket as auto_classified and adds category tag
def update_ticket(ticket_id, category):
    update_fields = {
        "custom_fields": {
            "cf_auto_classified": True,
            "cf_category": category,
        }
    }

    headers = {
        "Content-Type": "application/json",
    }
    UPDATE_URL = BASE_URL + f"/tickets/{ticket_id}"

    response = requests.put(
        UPDATE_URL, auth=(FRESH_API_KEY, PASSWORD), json=update_fields, headers=headers
    )

    if response.status_code == 200:
        print(f"ticket {ticket_id} successfully updated")
    else:
        print(f"Update failed. Status Code: {response.status_code}")


# replys to email
def reply_to_ticket(id, body):
    reply_url = URL + f"/{str(id)}/reply"
    data = {"body": body}
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        reply_url, auth=(FRESH_API_KEY, PASSWORD), headers=headers, json=data
    )
    if response.status_code == 201:
        print("Email response sent to ticket ", id)


def process_tickets(tickets):
    for ticket in tickets:
        custom_fields = ticket["custom_fields"]
        auto_classified = custom_fields["cf_auto_classified"]
        if auto_classified == False:
            print("\nEmail received! Processing...")
            # categorize ticket using llm
            category = llm_categorize(ticket["description_text"], "categories.txt")
            print("Category: ", category)

            if category == "invalid":
                print("Category unclear - sending to human review")
                category = "Human Review"

            if len(category) > 0:
                # update ticket category and label as classified
                update_ticket(ticket["id"], category)

                if category in NON_REPLY_CATEGORIES:
                    print(category, "= non-reply category")
                else:
                    # Generate reply using llm
                    reply = (
                        "Hello,</br></br>"
                        + llm_reply(ticket["description_text"], category)
                        + "</br></br>Kind regards,</br>"
                        + "Nimble"
                    )
                    # send reply email
                    reply_to_ticket(ticket["id"], reply)


def loading_animation():
    animation = "|/-\\"
    i = 0
    while True:
        tickets = None
        tickets, tickets_found = emails_received()
        if not tickets_found:
            sys.stdout.write(
                "\rWaiting for incoming emails " + animation[i % len(animation)]
            )
            sys.stdout.flush()
            sleep(0.1)
            i += 1
        else:
            process_tickets(tickets)


def emails_received():
    # fetches all unclassified tickets
    tickets = fetch_unprocessed_tickets()

    if tickets is not None and len(tickets) > 0:
        return tickets, True
    else:
        tickets = None
        return tickets, False


if __name__ == "__main__":
    # Keep looping while waiting to recieve tickets. Ctrl C to stop.
    loading_animation()
