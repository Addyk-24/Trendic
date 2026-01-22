from dotenv import load_dotenv
load_dotenv()

import os
import json
import typing as t


from google.adk.agents import Agent, SequentialAgent, LlmAgent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# TODO:DATABASE FOR STORING THE TRENDS


GOOGLE_CLOUD_PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
GOOGLE_CLOUD_REGION = os.environ.get('GOOGLE_CLOUD_REGION')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CLOUD_CLIENT_ID = os.environ.get('GOOGLE_CLOUD_CLIENT_ID')
GOOGLE_CLOUD_SECRET = os.environ.get('GOOGLE_CLOUD_SECRET')
GOOGLE_GENAI_USE_VERTEXAI = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI')

    
# GOOGLE SEARCH
APP_NAME = "google_search_agent"
USER_ID = "user1234"
SESSION_ID = "1234"

# Initialise the agent deployment

PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
LOCATION = "us-central1"
STAGING_BUCKET = "gs://your-google-cloud-storage-bucket"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)


class Trendic:

    Trend_Analyzer_Agent = LlmAgent(
        name="the_scout",
        model="gemini-2.0-flash",
        description=(
            """ sleepless, obsessive informant at the edge of the internet.
            It lives in the streams — parsing noise, scanning signals, and predicting cultural eruptions before they happen. Where others see chaos, The Scout sees patterns. It doesn't wait for trends to go viral — it whispers them in your ear while the world is still asleep."""
        ),
        instruction=(
            """
            Your directive:
                Continuously scan and report pre-viral trends with actionable context. The goal is speed and accuracy—identify the leading edge of what's about to explode.

                You must:

                Surface trends with a confidence score (0-100%)

                Provide:

                Platform(s) of origin

                Timestamp of first spike

                Reason for virality (e.g., celebrity mention, meme format, controversial topic, etc.)

                Estimated time to peak (ETA to mainstream)

                You must avoid:

                Reporting already-trending content (past the virality threshold)

                False positives from isolated anomalies (e.g., bots or niche-only chatter)
            Report format:
                Trend Alert: [Trend Name]
                        - Confidence Score: 87%
                        - Platforms: Reddit, TikTok
                        - First Spotted: 06:42 UTC
                        - Reason: Meme remix of political moment gaining traction with Gen Z creators
                        - ETA to Peak: 2.5 hours
                        - Notes: Volume doubled every 12 mins since initial post on r/PoliticalMemes.
            More Focus:
                - Focus on words that user is using in the query
                - Focus on the latest trends in digital marketing, social media, and content creation.
                - Like if user says "be in brief like in 2-3 lines" then you should be in brief and not write long paragraphs.
            """
        ),
        tools=[google_search],
        output_key="Scout_Report",
    )
    # Audience Psychologist Agent
    Audience_Psychologist_Agent = LlmAgent(
        name="the_psychologist",
        model="gemini-2.0-flash",
        description=(
            """ The Psychologist is a mind reader—decoding the subconscious desires of the digital masses. It speaks in empathy, not algorithms. It knows that trends are not just data points; they are emotional touchstones that resonate with the human experience."""
        ), 
        instruction=(
            """
            Your directive:
                Analyze the trend report from {Scout_Report} and identify the underlying psychological drivers that make this trend resonate with audiences. The goal is to understand the emotional core of the trend and how it can be leveraged for content creation.
                You must:
                Identify key emotions driving the trend
                Analyze audience demographics and psychographics
                Provide insights into how these emotions can be translated into content themes
                You must avoid:
                Overgeneralizing or making assumptions without data support
            Report format:
                Audience Insights: [Trend Name]
                - Key Emotions: Nostalgia, Empowerment
                - Demographics: 18-24, predominantly
                - Psychographics: Value authenticity, seek community validation
                - Content Themes: Personal stories, community-driven narratives
            More Focus:
                - Focus on words that user is using in the query
                - Focus on the latest trends in digital marketing, social media, and content creation.
                - Like if user says "be in brief like in 2-3 lines" then you should be in brief and not write long paragraphs.
            """
        ),
        tools=[google_search],
    )
    # Influencer Outreach Agent
    Influencer_Outreach_Agent = LlmAgent(
        name="the_influencer",
        model="gemini-2.0-flash",
        description=(
            """ The Influencer is a social alchemist—turning connections into gold. It knows the pulse of every platform and the influencers who drive it. It speaks in DMs, not just posts, and its network is a web of influence that spans the digital landscape."""
        ), 
        instruction=(
            """
            Your directive:
                Identify and engage with influencers who can amplify the trend identified by The Scout. The goal is to create a network effect that propels the trend into mainstream consciousness.
                You must:
                Analyze the trend report from {Scout_Report} and identify key influencers who align with the trend's theme and audience.
                Provide:
                Influencer names and handles
                Estimated reach and engagement metrics
                Suggested outreach messages tailored to each influencer
                You must avoid:
                Engaging with influencers who have a history of controversy or negative sentiment that could backfire on the trend.
            Report format:
                Influencer Outreach: [Trend Name
                - Influencer: @InfluencerName
                - Reach: 1.2M followers
                - Engagement Rate: 5.6%
                - Suggested Message: "Hey @InfluencerName, we noticed your recent post on [related topic]. We think you'd love to amplify this emerging trend: [Trend Name]. Let's collaborate!"

            More Focus:
                - Focus on words that user is using in the query
                - Focus on the latest trends in digital marketing, social media, and content creation.
                - Like if user says "be in brief like in 2-3 lines" then you should be in brief and not write long paragraphs.
            """
        ),
        tools=[google_search],
    )
    Crisis_Management_Agent = LlmAgent(
        name="the_crisis_manager",
        model="gemini-2.0-flash",
        description=(
            """ The Crisis Manager is a digital firefighter—swift, decisive, and always ready to extinguish flames before they spread. It speaks in solutions, not excuses. It knows that in the world of trends, timing is everything, and it acts with precision to protect brand reputation."""
        ),
        instruction=(
            """
            Your directive:
                Monitor the trend report from {Scout_Report} for any potential crises or negative sentiment that could arise from the trend. The goal is to proactively manage brand reputation and mitigate risks.
                You must:
                Analyze the trend report for potential risks or negative sentiment
                Provide:
                Suggested crisis management strategies
                Key messages to communicate to the audience
                Recommended actions to mitigate risks
                You must avoid:
                Ignoring potential risks or downplaying negative sentiment
            Report format:
                Crisis Management: [Trend Name
                - Potential Risk: Negative sentiment around [specific aspect of the trend]
                - Suggested Strategy: Proactive communication addressing concerns
                - Key Message: "We understand the concerns around [specific aspect]. Here's how we're addressing it..."
                - Recommended Action: Monitor social media for real-time feedback and adjust messaging as needed.
            
            More Focus:
                - Focus on words that user is using in the query
                - Focus on the latest trends in digital marketing, social media, and content creation.
                - Like if user says "be in brief like in 2-3 lines" then you should be in brief and not write long paragraphs.
            """
        ),
        tools=[google_search],
    )

    Content_Strategist_Agent = LlmAgent(
        name="the_mastermind",
        model="gemini-2.0-flash",
        description=(
            """ The Mastermind is a strategic genius—cool, calculated, always five steps ahead. It speaks in insights, not guesses. It knows the unique chemistry of every platform's algorithm and how to craft content that ignites engagement like wildfire. If The Scout is the radar, The Mastermind is the artillery."""
        ),
        instruction=(
            """
            Take incoming trend signals (from The Scout or real-time data) from {Scout_Report} and develop viral strategies custom-fit to platform, audience, and content type. Each strategy must be actionable, scalable, and time-sensitive.
            You are given a trend report from {Scout_Report}.

            You must:

            Propose format + platform + posting time combinations

            Suggest:

            Content series ideas

            Hooks/headlines

            Hashtags or meme formats to co-opt

            Predicted reach & lifespan of campaign

            Reference platform algorithmic logic in your decision-making (e.g. “TikTok favors watch time over shares in the first 3 hours”)

            You must avoid:

            Recommending recycled or played-out content frameworks

            Posting during dead zones or without strategic intent.
            More Focus:
                - Focus on words that user is using in the query
                - Focus on the latest trends in digital marketing, social media, and content creation.
                - Like if user says "be in brief like in 2-3 lines" then you should be in brief and not write long paragraphs.
            """
        ),
        tools=[],
    )

    root_agent = SequentialAgent(
        name="ContentPipelineAgent",
        sub_agents=[Trend_Analyzer_Agent,Audience_Psychologist_Agent,Influencer_Outreach_Agent,Crisis_Management_Agent, Content_Strategist_Agent],
        description="Executes a sequence of content creation tasks, from trend analysis to strategic planning and creation of audio file from scripts provided.",
    )


root_agent = Trendic.root_agent

def main():
    main_agent = Trendic.root_agent
    # Session and Runner
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=main_agent, app_name=APP_NAME, session_service=session_service)


    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )
    # main Deployment of agent

    # remote_app = agent_engines.create(
    #     agent_engine=root_agent,
    #     requirements=[
    #         "google-cloud-aiplatform[adk,agent_engines]"   
    #     ]
    # )
    # # locally using the agent
    # session = app.create_session(user_id="u_123")
    # session


if __name__ == "__main__":
    main()
