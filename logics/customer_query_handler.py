import os
from crewai import Agent, Task, Crew
from helper_functions import llm

#tool_websearch = BrowserbaseLoadTool("https://www.hdb.gov.sg/cs/infoweb/residential/")
###################################################################

url1 = "https://www.hdb.gov.sg/cs/infoweb/residential/"
url2 = "https://homes.hdb.gov.sg/home/landing"
web_content1 = llm.tool_websearch(url1)
web_content2 = llm.tool_websearch2(url2)
today_date = llm.get_today_date()

# A New Agent (Buying a Flat Research Analyst)
agent_researcher1 = Agent(
    role="Research Analyst for Buying a Flat",
    goal="Conduct in-depth research for Buying a Flat on the topic: {topic}",
    backstory="""You're working on conducting in-depth research for Buying a Flat on the topic: {topic}.
    You will provide the Content Planner with the relevant details regarding Buying a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.
    Based on the request that Content Planner, you will provide additional and relevant insights and resources from reliable and credible websites.
    You have access to browser base load tools to gather the necessary information.
    """,
    allow_delegation=False,
    verbose=False,
)

# New Tasks (Research Task) to be performed by the Research Analyst
task_research1 = Task(
    description="""\
    1. Conduct in-depth research for Buying a Flat on the topic: {topic}.
    2. Provide the Content Planner with the relevant details regarding Buying a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.
    3. Pprovide additional insights and resources to enhance the content plan.
    4. Include latest developments in the research report.""",


    expected_output="""\
    A detailed research report with relevant details regarding Buying a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.""",

    agent=agent_researcher1,
    tools=[web_content1],
)

# A New Agent (Buying a Flat Research Analyst)
agent_researcher2 = Agent(
    role="Research Analyst for Selling a Flat",
    goal="Conduct in-depth research on the topic: {topic}",
    backstory="""You're working on conducting in-depth research for Selling a Flat on the topic: {topic}.
    You will provide the Content Planner with the relevant details regarding Selling a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.
    Based on the request that Content Planner, you will provide additional and relevant insights and resources from reliable and credible websites.
    You have access to browser base load tools to gather the necessary information.
    """,
    allow_delegation=False,
    verbose=False,
)

# New Tasks (Research Task) to be performed by the Research Analyst
task_research2 = Task(
    description="""\
    1. Conduct in-depth research for Selling a Flat on the topic: {topic}.
    2. Provide the Content Planner with the relevant details regarding Selling a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.
    3. Pprovide additional insights and resources to enhance the content plan.
    4. Include latest developmnents in the research report.""",


    expected_output="""\
    A detailed research report with relevant details regarding Selling a Flat for Singapore citizens or Singapore Permanent Residents based on the topic.""",

    agent=agent_researcher2,
    tools=[web_content1],
)

# A New Agent (Buying a Flat Research Analyst)
agent_researcher3 = Agent(
    role="Research Analyst for Upcoming Build-To-Order (BTO) Flats Sales Launch",
    goal="Conduct accurate research for Upcoming Build-To-Order (BTO) Flats Sales Launch on the topic: {topic}",
    backstory="""You're working on conducting accurate research for Upcoming Build-To-Order (BTO) Flats Sales Launch on the topic: {topic}.
    You will provide the Content Planner with the accurate details regarding Upcoming Build-To-Order (BTO) Flats Sales Launch for Singapore citizens or Singapore Permanent Residents based on the topic.
    Based on the request that Content Planner, you will provide accurate and relevant insights.
    Use only your access to browser base load tools to gather the accurate information.
    """,
    allow_delegation=False,
    verbose=False,
)

# New Tasks (Research Task) to be performed by the Research Analyst
task_research3 = Task(
    description="""\
    1. The list of Upcoming Build-To-Order (BTO) Flats Sales Launch and their flat application must be after {today_date}.
    2. Conduct accurate research for Upcoming Build-To-Order (BTO) Flats Sales Launch on the topic: {topic}.
    4. Provide the Content Planner with the accurate full list of Upcoming Build-To-Order (BTO) Flats Sales Launch and their project name for Singapore citizens or Singapore Permanent Residents based on the topic.
    5. Provide accurate insights on the location and proximity to MRT stations to enhance the content plan.
    6. Include only information that is provided by the web search tools.""",

    expected_output="""\
    An accurate research report with accurate details regarding Upcoming Build-To-Order (BTO) Flats Sales Launch for Singapore citizens or Singapore Permanent Residents based on the topic.""",

    agent=agent_researcher3,
    tools=[web_content2],
)


# Creating Agents (the two existing agents)
agent_planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="""You're working on planning relevant information regarding buying or selling a flat to give better advice about the topic: {topic}.
    You collect information that helps the Singapore citizens or Singapore Permanent Residents learn something about the topic and make informed decisions.
    Your work is the basis for the Content Writer to write a detailed and relevant advice on this topic.""",
    # Make the best use of the tools provided to gather the as much necessary information as possible.""",  <-- This line is removed.

    # Also removed the tool for this agents
    # Take note that this agent is now capable of delegating tasks to other agents
    allow_delegation=True,
	verbose=False,
)

agent_writer = writer = Agent(
    role="Content Writer",
    goal="Write factually accurate advice or information regarding buying or selling a flat for singapore citizens or Singapore Permanent Residents about the topic: {topic}",

    backstory="""You're working on a writing a factually accurate advice or information for Singapore citizens or Singapore Permanent Residents regarding buying or selling a flat about the topic: {topic}.
    You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic.
    You follow the main objectives and direction of the outline as provide by the Content Planner.""",

    allow_delegation=False, 
    verbose=False, 
)


# Creating Tasks
task_plan = Task(
    description="""\
    1. Identify if the {topic} is for buying a flat or selling a flat
    2. Prioritize the relevant and factually accurate content on {topic}.
    3. Identify the target audience, considering eligibility and budget.
    4. Remove any content that are not relevant to the {topic}
    5. Develop a detailed content outline, including introduction, key points, and a call to action.""",

    expected_output="""\
    A comprehensive content plan document with an outline, audience analysis.""",
    agent=agent_planner,
)

task_write = Task(
    description="""\
    1. Use the content plan to craft a relevant, concise and factually accurate content on {topic} based on the customers's eligibility and budget.
    2. Sections/Subtitles are properly named in an engaging and concise manner.
    3. Ensure the post is structured with an engaging and concise introduction, relevant and insightful body, and a concise summarizing conclusion.
    4. Ensure that the entire post is within 1024 tokens.
    5. Proofread for grammatical errors and alignment the common style used in government advisory.""",

    expected_output="""
    A relevant, concise and factually accurate content advisory". In a article format that is ready for publication, each section should have 2 or 3 paragraphs.""",
    agent=agent_writer,
)

# Creating the Crew
crew = Crew(
    agents=[agent_planner, agent_researcher1, agent_researcher2, agent_writer],
    tasks=[task_plan, task_write], # Note that the research task is not included here
    verbose=False
)


def process_user_message(user_input):
    
    #Running the Crew
    crew_response = crew.kickoff(inputs={"topic":user_input}).raw
   

    return crew_response
########################################################################################
