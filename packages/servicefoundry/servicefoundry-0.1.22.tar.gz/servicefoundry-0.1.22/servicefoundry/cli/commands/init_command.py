import logging
from types import SimpleNamespace

import questionary
import rich_click as click
from questionary import Choice

from servicefoundry.build import lib
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.lib import workspace as workspace_lib
from servicefoundry.build.lib.util import resolve_cluster_or_error, resolve_workspaces
from servicefoundry.build.parser.sf_template import SfTemplate
from servicefoundry.build.parser.template_parameters import (
    NUMBER,
    OPTIONS,
    STRING,
    WORKSPACE,
)
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.util import BadRequestException
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)

MSG_CREATE_NEW_SPACE = "Create a new workspace"


@click.command(help="Initialize new service for servicefoundry")
@handle_exception_wrapper
def init():
    # Get SFSClient
    tfs_client = ServiceFoundryServiceClient.get_client()

    # Get Session else do login
    try:
        get_session()
    except BadRequestException:
        do_login = questionary.select(
            "You need to login to create a service", ["Login", "Exit"]
        ).ask()
        if do_login == "Login":
            lib.login(non_interactive=False)
        else:
            return

    # Static call to get list of templates
    templates = tfs_client.get_templates_list()

    # Choose a template of service to be created.
    template_choices = [
        Choice(f'{t["id"]} - {t["description"]}', value=t["id"]) for t in templates
    ]
    template_id = questionary.select("Choose a template", template_choices).ask()
    sf_template = SfTemplate.get_template(f"truefoundry.com/v1/{template_id}")

    parameters = {}
    for param in sf_template.parameters:
        if param.kind == STRING:
            parameters[param.id] = questionary.text(
                param.prompt, default=param.default
            ).ask()
        elif param.kind == NUMBER:
            while True:
                value = questionary.text(param.prompt, default=str(param.default)).ask()
                if value.isdigit():
                    parameters[param.id] = int(value)
                    break
                else:
                    print("Not an integer Value. Try again")
        elif param.kind == OPTIONS:
            parameters[param.id] = questionary.select(
                param.prompt, choices=param.options
            ).ask()
        elif param.kind == WORKSPACE:
            # TODO: use get spaces
            workspaces = resolve_workspaces(
                client=tfs_client,
                name_or_id=None,
                cluster_name_or_id=None,
                ignore_context=False,
            )
            # TODO (chiragjn): should display fqn here for same workspace name across clusters in case
            #                  cluster is not set in context
            workspace_choices = [
                Choice(title=w.name, value=w)
                for w in workspaces
                if w.status == "CREATE_SPACE_SUCCEEDED"
            ]
            workspace_choices.append(
                Choice(title=MSG_CREATE_NEW_SPACE, value=MSG_CREATE_NEW_SPACE)
            )
            workspace = questionary.select(
                param.prompt, choices=workspace_choices
            ).ask()

            if workspace == MSG_CREATE_NEW_SPACE:
                cluster = resolve_cluster_or_error(
                    name_or_id=None,
                    ignore_context=False,
                    non_interactive=False,
                    client=tfs_client,
                )
                new_space_name = questionary.text(
                    "Please provide a name for your workspace"
                ).ask()
                workspace = workspace_lib.create_workspace(
                    name=new_space_name,
                    cluster_name_or_id=cluster.id,
                    tail_logs=True,
                    non_interactive=False,
                    client=tfs_client,
                )
                console.print(
                    f"Done, created new workspace with name {new_space_name!r}"
                )
            parameters[param.id] = workspace.fqn

    sf_template.generate_project(parameters)

    if sf_template.post_init_instruction:
        console.print(
            sf_template.post_init_instruction.format(
                parameters=SimpleNamespace(**parameters)
            )
        )


def get_init_command():
    return init
