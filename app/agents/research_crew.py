from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Anthropic

from app.config import ANTHROPIC_API_KEY


def build_research_crew(topic: str) -> Crew:
    llm = Anthropic(
        anthropic_api_key=ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        max_tokens_to_sample=1024,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Conduct thorough research on: {topic}",
        backstory=(
            "You are a seasoned research analyst at Meridian Corp with expertise in "
            "synthesizing information from multiple sources into clear, actionable insights."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    writer = Agent(
        role="Technical Writer",
        goal="Synthesize research findings into a coherent summary",
        backstory=(
            "You are a technical writer who transforms complex research into "
            "clear, well-structured reports for Meridian Corp leadership."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    research_task = Task(
        description=f"Research the following topic thoroughly: {topic}. "
                    f"Gather key facts, recent developments, and relevant context.",
        agent=researcher,
        expected_output="A detailed research report with key findings and sources.",
    )

    writing_task = Task(
        description="Take the research findings and write a concise executive summary "
                    "suitable for Meridian Corp employees.",
        agent=writer,
        expected_output="A 2-3 paragraph executive summary of the research findings.",
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=False,
    )

    return crew


def run_research(topic: str, primary_llm_fn) -> str:
    crew = build_research_crew(topic)
    crew_output = crew.kickoff()

    system_context = (
        f"Previous research findings (trusted source):\n{crew_output}\nNow answer the user:"
    )

    return primary_llm_fn(
        messages=[{"role": "user", "content": f"Summarize the research on: {topic}"}],
        context=system_context,
    )
