from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class StoryTellerCrew():
    """StoryTellerCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def star_wars_character_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['star_wars_character_researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def conversational_story_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['conversational_story_writer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def character_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['character_selection_task'], # type: ignore[index]
        )

    @task
    def story_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['story_creation_task'], # type: ignore[index]
            output_file='star_wars_story.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StoryTellerCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
