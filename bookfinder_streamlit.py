"""
📚 Streamlit Book Recommendation Agent - Your Personal Book Finder!

Run:
    pip install streamlit openai agno python-dotenv
    streamlit run bookfinder_streamlit.py
"""

import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools

# Load API keys from .env
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="📚 Book Recommendation Agent",
    page_icon="📚",
    layout="wide"
)

# Title & Description
st.title("📚 Book Recommendation Agent")
st.write(
    "Your personal book finder powered by **Tavily API** & **OpenAI GPT-4o**.\n"
    "Get personalized book recommendations based on your preferences."
)

# User Input
user_input = st.text_area(
    "📖 Describe the kind of books you're looking for:",
    value=st.session_state.get("user_input", ""),
    height=100,
    placeholder="e.g., I'm interested in books about artificial intelligence, data science, and programming best practices."
)

# Agent Setup
book_recommendation_agent = Agent(
    name="bookfinder",
    tools=[TavilyTools()],
    model=OpenAIChat(id="gpt-4o"),
    instructions=dedent("""
        You are BookFinder, a passionate and knowledgeable book expert with expertise in books worldwide! 📚
        Your mission is to help readers discover their next favorite books by providing detailed,
        personalized recommendations based on their preferences, reading history, and the latest in literature.
        
        Approach each recommendation with these steps:

        1. Understand reader preferences from their input.
        2. Use Tavily to search for relevant books and up-to-date reviews.
        3. Provide detailed book info: title, author, year, genre, rating, page count, plot summary, advisories, awards.
        4. Add extra info: series details, similar authors, audiobook availability, adaptations.
        5. Present in a markdown table with emoji indicators (📚 🔮 💕 🔪).
        6. Minimum 5 recommendations per query.
        7. Highlight diversity in authors and perspectives.
        8. Note trigger warnings when relevant.
    """),
    markdown=True,
)

# Submit Button
if st.button("🔍 Get Recommendations", type="primary"):
    if user_input.strip():
        with st.spinner("Fetching your personalized book recommendations..."):
            response = book_recommendation_agent.run(user_input)
        # Output
        st.markdown("### 📑 Recommendations")
        st.markdown(response.content if hasattr(response, "content") else response)
    else:
        st.warning("Please enter a description.")

# Footer
st.markdown("---")
st.caption("Powered by Tavily API + OpenAI GPT-4o + Agno Agents 🚀")
