#!/usr/bin/env python

from crewai.flow import Flow, start, listen, router
from transcript_insights_flow.crews.story_teller_crew.story_teller_crew import StoryTellerCrew
from transcript_insights_flow.crews.transcript_analyst_crew.transcript_analyst_crew import TranscriptAnalystCrew
from transcript_insights_flow.models import TranscriptInsightsState

class TranscriptInsightsFlow(Flow[TranscriptInsightsState]):

    @start()
    def run(self):
        print("Generating sentence count")

    @listen(run)
    def validate_inputs(self):
        if not self.state.question:
            self.state.errors.append("Question cannot be empty.")

    @router(validate_inputs)
    def error_handler(self):
        if self.state.errors and len(self.state.errors) > 0:
            return "raise_error"
        return "proceed"

    @listen("raise_error")
    def raise_error_handler(self):
        raise ValueError("Invalid inputs: ")

    @listen("proceed")
    def proceed_handler(self):
        crew =  TranscriptAnalystCrew().crew()
        result = crew.kickoff(
            inputs={
                "question": self.state.question,
            }
        )

        if result.pydantic:
            return result.pydantic

    @listen(proceed_handler)
    def storify(self, prev):
        star_crew =  StoryTellerCrew().crew()
        result = star_crew.kickoff(
            inputs={
                "analysis": prev.answer
            }
        )

        print("Final Story:")
        print(result.raw)








def kickoff():
    transcript_flow = TranscriptInsightsFlow()
    transcript_flow.kickoff(
        inputs={
            "question": "Sobre o que se trata a transcription"
        }
    )
    


def plot():
    transcript_flow = TranscriptInsightsFlow()
    transcript_flow.plot()


if __name__ == "__main__":
    kickoff()
