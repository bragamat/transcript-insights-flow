from crewai_tools import PDFSearchTool

# Initialize the tool allowing for any PDF content search if the path is provided during execution
pdf_search_tool = PDFSearchTool(pdf='knowledge/setup-crewai.pdf')

if __name__ == "__main__":
    tool = PDFSearchTool()
    result = tool._run(query="What is the most important step in setting up CrewAI?")
    print("Result:", result)
