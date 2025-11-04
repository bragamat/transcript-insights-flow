# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **CrewAI Flow** project for analyzing transcripts and generating insights. The project uses CrewAI's Flow pattern to orchestrate multi-agent AI systems that collaborate on complex tasks.

## Key Commands

### Running the Flow
```bash
crewai run
```
Main entry point that executes the TranscriptInsightsFlow.

### Visualizing Flow Structure
```bash
crewai plot
# or
uv run plot
```
Generates a visualization of the flow execution graph (saves to `crewai_flow.html`).

### Development
```bash
crewai install  # Lock and install dependencies using uv
pip install uv  # Install uv package manager if not present
```

### Direct Python Execution
```bash
python src/transcript_insights_flow/main.py  # Runs kickoff()
uv run kickoff  # Alternative via pyproject.toml script
```

## Architecture

### Flow-Based Architecture

This project uses CrewAI's **Flow pattern** (`[tool.crewai] type = "flow"` in pyproject.toml), not the older standalone Crew pattern. Key characteristics:

- **Main Flow**: `TranscriptInsightsFlow` (in `main.py`) extends `Flow[TranscriptInsightsState]`
- **State Management**: Uses Pydantic model `TranscriptInsightsState` to maintain state across flow steps
- **Flow Decorators**:
  - `@start()` - Entry point of the flow
  - `@listen(method)` - Triggered after specified method completes
  - `@router(method)` - Conditional branching based on state

### Flow Execution Pattern

The flow implements input validation with error routing:

1. `run()` - Start point
2. `validate_inputs()` - Checks for empty transcript/question
3. `error_handler()` - Routes to "raise_error" or "proceed" based on validation
4. Either `raise_error_handler()` or `proceed_handler()` executes

### Crews as Flow Components

Multiple crews can be integrated into the flow (though not yet fully integrated in current state):

- **PoemCrew** (`src/transcript_insights_flow/crews/poem_crew/`)
  - Single agent: `poem_writer`
  - Task: Generate poems with specific sentence counts
  - Uses parameter: `{sentence_count}`

- **TranscriptAnalystCrew** (`src/transcript_insights_flow/crews/transcript_analyst_crew/`)
  - Two agents: `researcher`, `reporting_analyst`
  - Sequential process with two tasks
  - Outputs to `report.md`
  - Uses parameters: `{topic}`, `{current_year}`

### Configuration Structure

Each crew follows the pattern:
```
crews/<crew_name>/
├── <crew_name>.py        # Crew class with @CrewBase decorator
├── config/
│   ├── agents.yaml       # Agent definitions (role, goal, backstory)
│   └── tasks.yaml        # Task definitions (description, expected_output, agent)
```

### State Management

`TranscriptInsightsState` (in `models/transcript_insights_flow_state.py`):
- `question: str` - Question to analyze transcript for
- `transcript: str` - Transcript text to analyze
- `errors: List[str]` - Accumulated error messages during processing

State is shared across all flow methods and can be modified in place.

### Crew Class Pattern

Crews use the `@CrewBase` decorator and define:
- `agents_config` / `tasks_config` - Paths to YAML files
- `@agent` decorated methods - Return Agent instances from YAML config
- `@task` decorated methods - Return Task instances from YAML config
- `@crew` decorated method - Assembles agents and tasks into a Crew
- `agents: List[BaseAgent]` and `tasks: List[Task]` - Auto-populated by decorators

## Environment Setup

- Python version: >=3.10 <3.14
- Package manager: **UV** (not pip/poetry)
- Environment variable required: `OPENAI_API_KEY` in `.env` file

## Integration Points

To integrate a crew into the flow:
1. Instantiate the crew in a flow method
2. Call `crew.kickoff()` with appropriate inputs
3. Pass state variables as inputs (e.g., `transcript`, `question`)
4. Update flow state with crew results

Example pattern (not yet implemented):
```python
@listen("proceed")
def analyze_transcript(self):
    crew = TranscriptAnalystCrew()
    result = crew.crew().kickoff(inputs={
        'topic': self.state.question,
        'transcript': self.state.transcript
    })
    # Process result and update state
```

## Testing

Test directory exists at `tests/` but no test infrastructure is currently configured.
