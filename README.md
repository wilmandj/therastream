# Therastream Application

Welcome to Therastream, a Streamlit-based application designed to assist with therapy needs. This application leverages OpenAI's language models to offer a range of therapeutic functionalities.

## Features

- **Connect to OpenAI**: Securely connect to OpenAI using an API key to enable AI-driven functionalities.
- **Define Expertise**: Customize the AI therapist's expertise by adding focus areas, improving responses, and saving configurations.
- **Therapist Assistant**: Engage in therapeutic conversations with an AI therapist, with options to save, load, and reset interactions.
- **Therapy Author**: Create book content or related material through conversations with an AI therapy author.
- **Create Drawing**: A new feature allowing users to create and analyze drawings as part of therapeutic exploration. To analyze, first save, then re-load under 'Analyze Drawing'
- **Analyze Drawing**: Upload and analyze drawings, providing psychological insights based on the provided captions.


## Getting Started

### Prerequisites

- Python ( e.g. Anaconda or an alternative installation )
- OpenAI API Key

### Installation from a linux / os terminal:

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd therastream
```

Install the required Python packages with pip ( includes streamlit ):

```bash
pip install -r requirements.txt
```

### Setting Up OpenAI API

1. Visit the [OpenAI website](https://openai.com/) and sign up for an account if you haven't already.
2. After logging in, navigate to the API section to generate a new API key.
3. Store this API key securely as you'll need it to connect the Therastream application to OpenAI's services.

### Running the Application

Run the Streamlit application:

```bash
streamlit run therastream_v2.py
```

### Usage

1. **Connect to OpenAI**: Enter your API key to establish a connection.
2. **Define Expertise**: Customize AI expertise settings as needed.
3. **Therapist Assistant**: Start a conversation with the AI therapist.
4. **Therapy Author**: Engage with the AI to create therapeutic content.
5. **Create Drawing**: Use the new feature to create drawings and explore psychological aspects.
6. **Analyze Drawing**: Upload drawings and receive AI-generated insights.

## Repository Structure

- **therastream_v2.py**: Main entry point for the Streamlit application.
- **pages/**: Directory containing the individual pages for the Streamlit application.
- **content/**: Directory containing content files used within the application.
- **experiments/**: Directory for experimental scripts and testing various features.
- **requirements.txt**: List of Python dependencies required for the application.
- **README.md**: Documentation for setting up and using the Therastream application.

We hope Therastream assists you in your journey towards mental well-being and personal growth. Enjoy exploring the features and integrating them into your therapeutic practices!

### Experimental Online Deployment

Therastream is currently deployed experimentally on the Streamlit Cloud Service as a Private App. 
The URL is: 
[https://therastreamv0.streamlit.app/](https://therastreamv0.streamlit.app/)