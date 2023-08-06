import os
import typer
import uvicorn
from dotenv import load_dotenv
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def start_server(openai_api_key: Annotated[str, typer.Option(help="OpenAI API Key",
                                                             rich_help_panel="Customization and Utils")]):
    """
    Start the openplugin server
    """
    from openplugin.api import app
    load_dotenv()
    os.environ["OPENAPI_KEY"] = openai_api_key
    uvicorn.run(app, host=os.environ['HOST'], port=int(os.environ['PORT']))
