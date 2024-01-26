![Alt text](images/header.png)

# Automated Email Responder

## Overview

The Automated Email Responder is a Python-based program designed to streamline the handling of customer emails. The program utilizes two language models to automatically categorize and generate responses to incoming emails.

## Table of Contents

1. [Input and Output](#input-and-output)
2. [Dependencies](#dependencies)
3. [Configuration](#configuration)
4. [Installation](#installation)
5. [Model Integration](#model-integration)
6. [Category Definitions](#category-definitions)
7. [Further Development](#further-development)

## Input and Output

Currently [Fresh Desk](https://www.freshworks.com/freshdesk/lp/home-bex/?tactic_id=6330166&utm_source=google-adwords&utm_medium=FD-Search-Brand-Core-MEA-Bex&utm_campaign=FD-Search-Brand-Core-MEA-Bex&utm_term=freshdesk&device=c&matchtype=e&network=g&gclid=CjwKCAiAzc2tBhA6EiwArv-i6ZvTBL222E-Xjo2dP2NAuZBNPRMqAFijj8MaedUxWyn8KXsi2w_-sRoCL3cQAvD_BwE&audience=aud-95784370677%3Akwd-30002131023&ad_id=688610343062&gad_source=1) is used as the input and output interface.

- **Input**: When an email is recieved it is automatically converted into a ticket in Fresh Desk. As the ticket has not yet been processed, it is labeled as unclassified. This way all unlcassified emails can be processed and updated to be labeled as classified.

- **Output**: Once an email has been processed, a reply to the ticket containing the generated response is created through Fresh Desk and a reply email is automatically sent.

## Dependencies

- **Programming Language**: Python 3.12.1
- **Dependencies**:
  - Refer to the Pipfile for a list of required libraries and their versions.
  - Required APIs:
    - [Fresh API](https://developers.freshdesk.com/api/)
    - [OpenAI API](https://platform.openai.com/docs/api-reference)
    - [AWS Bedrock API](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)
    - [Flowise API](https://docs.flowiseai.com/using-flowise/api)

## Configuration

- **Configuration Files**: No additional configuration files are needed; dependencies can be installed using the Pipfile.
- **Credentials and Access Tokens**:

  - Create a .env containing access tokens:
    - [Fresh API](https://developers.freshdesk.com/api/) - include in .env
    - [Flowise API](https://docs.flowiseai.com/using-flowise/api) - include in .env
  - Configure the following inside of flowise:
    - [OpenAI API](https://platform.openai.com/docs/api-reference) - configure in Reply Flow (Flowise)
    - [AWS Bedrock API](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html) - configure in Categorization Flow (Flowise)

- Ensure that the correct flow ids and server address are set so that the correct flows are identified when calling Flowise.

  - Configure these in the following variables in llm_actions.py:
    - BASE_URL: address of the Flowise instance you are using
    - CATEGORIZE_FLOW_ID: ID of the Categorization flow (FLowise)
    - REPLY_FLOW_ID: ID of the Reply flow (Flowise)

- Ensure that the correct Fresh Domain is set to identify the correct Fresh account.

  - Configure the following variable in main.py:
    - FRESH_BASE_URL: Set this to your Fresh domain (eg. yourdomain.freshdesk.com/api/v2)

- Ensure that adequate custom ticket fields are present in Fresh:
  - A tickbox field named: "auto_classified"
  - A listbox field named: "Category" which has a valid list of categories. This must match with the categories in categories.txt as well as those specified in the flowise prompt.

Fresh field names can be custmised inside of fresh but the code must be updated to reflect the new ticket field names if they are customised.

## Installation

1. Clone the repository.
2. Install dependencies using the Pipfile.
3. Ensure a valid instance of Flowise is running in an accessable location.
4. Configure API tokens (in .env and Flowise instance) and set specified variables.

## Category Definitions

- **Structure of "categories.txt"**: The file lists categories with corresponding IDs, following the example:

  ```
  1.Human Review
  2.Password Request
  3.Telephone Number Removal
  ...
  12.Call Back Request
  13.Settlement Letter Request
  14.Spam

  ```

- **Modification**: To customise/update categories:
  - Update the prompt structure in the categorization flow in Flowise
  - Mirror the changes in "categories.txt" so that both category lists are aligned

## Further Development

- **Flowise Replacement**: Flowise is used for prototyping, aiding experimental development in the interaction and integration with external language and classification models. After a robust and capable system has been designed, the functions currently being performed by Flowise should be allocated to a lower-level tool such as [Langchain](https://python.langchain.com/docs/get_started/introduction) for more extensive development.
- **Interchanging Language Models**: Different models could be used in the future for both classification and replies. Further research into the most applicable and cost-effective models is required.
- **Data Secuirity**: To ensure that data is safe at all times, the details of the way in which data is processed, stored and managed by all services used is vital. This also effects the future choice of tools/models.
- **Further fine-tuning + prompt engineering**: The performance and accuracy of the classification and responses can be improved by fine-tuning the models used aswell as more extensive prompt engineering.
- **Omni-chanel integration**: The poetential of this tool to be used through other chanels besides email is clear.
