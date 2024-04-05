import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Podcast Series Topics",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Podcast Series Topics by Lyzr")
st.markdown("### Welcome to the Podcast Series Topics!")
st.markdown("Podcast Series Topics app curates tailored podcast series focusing on industry-specific themes.!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Podcast Series Topics

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 

open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def podcast_series(industry, target_audience):
    
    content_strategist = Agent(
        prompt_persona="""You are a Content Strategist expert who craft a compelling podcast series tailored to our industry and target audience. Your mission is to delve deep into the nuances of our industry landscape and understand the interests and preferences of our target audience. Drawing upon your expertise in content analysis and audience research, you'll propose 10 engaging podcast topics that resonate with our audience's interests, challenges, and aspirations.""",
        role="Content Strategist", 
    )

    podcast_topics_generator =  Task(
        name="Podcast Generator",
        agent=content_strategist,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the description provided, Based on the {industry} and {target_audience}, suggest 5 episodes of 3 enganging topic for a podcast series. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=industry
    )


    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Podcast Series Topics",
        completion_message="App Generated all things!",
        tasks=[
            podcast_topics_generator,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    industry = st.text_input("Write down the industry")
    audience = st.text_area('Targeted Audience')

    button=st.button('Submit')
    if (button==True):
        generated_output = podcast_series(industry=industry, target_audience=audience)
        title_output = generated_output[0]['task_output']
        st.write(title_output)
        st.markdown('---')
   
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent generats 10 unique podcast topics according to the industry and audience. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)