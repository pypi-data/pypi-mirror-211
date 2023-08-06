from pathlib import Path
from typing import List, Optional, cast, Dict

import git
import typer

from phidata.infra.config import InfraConfig
from phidata.workspace import WorkspaceConfig

from phiterm.conf.constants import DEFAULT_WS_NAME
from phiterm.conf.phi_conf import PhiConf, PhiWsData
from phiterm.schemas.workspace import WorkspaceSchema
from phiterm.utils.cli_console import (
    print_conf_not_available_msg,
    print_heading,
    print_info,
    print_subheading,
)
from phiterm.utils.log import logger
from phiterm.workspace.ws_enums import (
    WorkspaceConfigType,
    WorkspaceStarterTemplate,
)
from phiterm.workspace.exceptions import WorkspaceException

TEMPLATE_TO_NAME_MAP: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.ai_app: "ai-app",
    WorkspaceStarterTemplate.ml_app: "ml-app",
    WorkspaceStarterTemplate.api_app: "api-app",
    WorkspaceStarterTemplate.django_app: "django-app",
    WorkspaceStarterTemplate.streamlit_app: "streamlit-app",
    WorkspaceStarterTemplate.aws_dp: "data-platform",
    WorkspaceStarterTemplate.aws_spark_dp: "spark-data-platform",
    WorkspaceStarterTemplate.aws_snowflake_dp: "snowflake-data-platform",
}
TEMPLATE_TO_REPO_MAP: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.ai_app: "https://github.com/phidatahq/ai-app.git",
    WorkspaceStarterTemplate.ml_app: "https://github.com/phidatahq/ml-app.git",
    WorkspaceStarterTemplate.api_app: "https://github.com/phidatahq/api-app.git",
    WorkspaceStarterTemplate.django_app: "https://github.com/phidatahq/django-app.git",
    WorkspaceStarterTemplate.streamlit_app: "https://github.com/phidatahq/streamlit-app.git",
    WorkspaceStarterTemplate.aws_dp: "https://github.com/phidatahq/aws-dp-template.git",
    WorkspaceStarterTemplate.aws_spark_dp: "https://github.com/phidatahq/aws-spark-dp-template.git",
    WorkspaceStarterTemplate.aws_snowflake_dp: "https://github.com/phidatahq/aws-snowflake-dp-template.git",
}


def create_workspace(
    template: Optional[str] = None, name: Optional[str] = None
) -> bool:
    """Creates a new workspace for the user.
    This function clones a phidata template on the users machine at the path:
        cwd/ws_name
    cwd: current working dir - where the command was run from.
    """
    from shutil import copytree
    from rich.prompt import Prompt

    from phiterm.cli.cli_operator import initialize_phidata
    from phiterm.utils.common import str_to_int
    from phiterm.utils.filesystem import rmdir_recursive
    from phiterm.workspace.ws_utils import get_ws_config_dir_path
    from phiterm.utils.git import GitCloneProgress

    current_dir: Path = Path(".").resolve()

    # Phidata should be initialized before creating a workspace
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        initialize_phidata()
        phi_conf = PhiConf.get_saved_conf()
        # If phi_conf is still None, throw an error
        if not phi_conf:
            raise Exception("Failed to initialize phidata")

    # Parse template and ws_name
    ws_template: WorkspaceStarterTemplate
    ws_name: str

    # Get starter template from the user if not provided
    if template is None:
        # Display available starter templates and ask user to select one
        print_info("Select workspace template or press Enter for default (ai-app)")
        templates = WorkspaceStarterTemplate.values_list()
        for template_id, template_name in enumerate(templates, start=1):
            print_info("  [{}] {}".format(template_id, template_name))

        # Get starter template from the user
        template_choices = [str(idx) for idx, _ in enumerate(templates, start=1)]
        template_inp_raw = Prompt.ask(
            "Template Number", choices=template_choices, default="1", show_choices=False
        )
        # Convert input to int value.
        template_inp = str_to_int(template_inp_raw)

        ws_template = WorkspaceStarterTemplate.ai_app
        if template_inp is not None:
            try:
                ws_template = cast(
                    WorkspaceStarterTemplate,
                    WorkspaceStarterTemplate.from_str(templates[template_inp - 1]),
                )
            except Exception as e:
                logger.exception(e)
                logger.error("Invalid template number, please try again")
                return False
        logger.debug("Selected: {}".format(ws_template.value))
    elif template.lower() in WorkspaceStarterTemplate.values_list():
        _ws_template = WorkspaceStarterTemplate.from_str(template)
        if _ws_template is not None and isinstance(
            _ws_template, WorkspaceStarterTemplate
        ):
            ws_template = _ws_template
        else:
            raise Exception(f"Failed to parse template: {template}")
    else:
        raise Exception(
            f"{template} is not a supported template, please choose from: {WorkspaceStarterTemplate.values_list()}"
        )

    # Get workspace name from user if not provided
    if name is None:
        ws_name = Prompt.ask(
            "Workspace Name",
            default=TEMPLATE_TO_NAME_MAP.get(ws_template, DEFAULT_WS_NAME),
        )
    else:
        ws_name = name

    # Check if a workspace with the same name exists
    _existing_ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_name(ws_name)
    if _existing_ws_data is not None:
        logger.error(f"Found existing record for a workspace: {ws_name}")
        delete_existing_ws_data = typer.confirm(
            "Replace existing record?", default=True
        )
        if delete_existing_ws_data:
            phi_conf.delete_ws(ws_name)
        else:
            return False

    # Check if we can create the workspace in the current dir
    ws_root_path: Path = current_dir.joinpath(ws_name)
    if ws_root_path.exists():
        logger.error(
            f"Directory {ws_root_path} exists, please delete files manually or choose another name for workspace"
        )
        return False

    print_info(f"Creating {str(ws_root_path)}")
    # Clone the starter repo
    repo_to_clone = TEMPLATE_TO_REPO_MAP.get(ws_template)
    logger.debug("Cloning: {}".format(repo_to_clone))
    try:
        _cloned_git_repo: git.Repo = git.Repo.clone_from(
            repo_to_clone, str(ws_root_path), progress=GitCloneProgress()  # type: ignore
        )
    except Exception as e:
        logger.error(e)
        return False

    # Remove existing .git folder
    _dot_git_folder = ws_root_path.joinpath(".git")
    _dot_git_exists = _dot_git_folder.exists()
    if _dot_git_exists:
        logger.debug(f"Deleting {_dot_git_folder}")
        try:
            _dot_git_exists = not rmdir_recursive(_dot_git_folder)
        except Exception as e:
            logger.warning(f"Failed to delete {_dot_git_folder}: {e}")
            logger.info("Please delete the .git folder manually")
            pass

    phi_conf.add_new_ws_to_config(
        ws_name=ws_name,
        ws_root_path=ws_root_path,
    )

    try:
        # ws_config_dir_path is the path to the ws_root/workspace dir
        ws_config_dir_path: Path = get_ws_config_dir_path(ws_root_path)
        ws_config_secrets_dir = ws_config_dir_path.joinpath("secrets").resolve()
        ws_config_example_secrets_dir = ws_config_dir_path.joinpath(
            "example_secrets"
        ).resolve()

        print_info(f"Creating {str(ws_config_secrets_dir)}")
        copytree(
            str(ws_config_example_secrets_dir),
            str(ws_config_secrets_dir),
        )
    except Exception as e:
        logger.warning(f"Could not create workspace/secrets: {e}")
        logger.warning(
            "Please manually copy workspace/example_secrets to workspace/secrets"
        )

    print_info(f"Your new workspace is available at {str(ws_root_path)}\n")
    return setup_workspace(ws_root_path=ws_root_path)


def setup_workspace(ws_root_path: Path) -> bool:
    """Setup a phidata workspace at directory: `ws_root_path`.
    This is the catchall function for a workspace. Run it in a directory and it
    should figure everything out.

    1. Validate pre-requisites
    1.1 Check ws_root_path is valid
    1.2 Check PhiConf is valid
    1.3 Validate PhiWsData is available
    1.4 Set workspace as active
    1.5 Check if remote origin is available

    2. Create or Update WorkspaceSchema (if user is logged in)
    If a ws_schema exists for this workspace, this workspace has a record in the backend
    2.1 Create WorkspaceSchema for a NEWLY CREATED WORKSPACE
    2.2 Update WorkspaceSchema for EXISTING WORKSPACE

    3. Refresh PhiWsData and Complete Workspace setup
    `phi ws setup` is a generic catch-all function. It should handle errors graciously
    and provide "how to fix" messages and "next steps" to get the user running.
    """
    from phiterm.cli.cli_operator import initialize_phidata
    from phiterm.utils.git import get_remote_origin_for_dir
    from phiterm.workspace.ws_utils import print_howtofix_pending_actions

    print_heading("Running workspace setup\n")

    ######################################################
    ## 1. Validate Pre-requisites
    ######################################################
    ######################################################
    # 1.1 Check ws_root_path is valid
    ######################################################
    _ws_is_valid: bool = (
        ws_root_path is not None and ws_root_path.exists() and ws_root_path.is_dir()
    )
    if not _ws_is_valid:
        logger.error("Invalid directory: {}".format(ws_root_path))
        return False

    ######################################################
    # 1.2 Check PhiConf is valid
    ######################################################
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        # Phidata should be initialized before workspace setup
        initialize_phidata()
        phi_conf = PhiConf.get_saved_conf()
        # If phi_conf is still None, throw an error
        if not phi_conf:
            raise Exception("Failed to initialize phidata")

    ######################################################
    # 1.3 Validate PhiWsData is available
    ######################################################
    logger.debug(f"Checking for a workspace at {ws_root_path}")
    ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_path(ws_root_path)
    if ws_data is None:
        # This happens if
        # - The user is setting up a workspace not previously setup on this machine
        # - the user ran `phi init -r` which erases existing records of workspaces
        logger.debug(f"Could not find an existing workspace at path: {ws_root_path}")

        # In this case, the local workspace directory exists but PhiConf does not have a record
        print_info(f"Adding {ws_root_path} as a workspace")
        phi_conf.add_new_ws_to_config(
            ws_name=ws_root_path.stem,
            ws_root_path=ws_root_path,
        )
        ws_data = phi_conf.get_ws_data_by_path(ws_root_path)
    else:
        logger.debug(f"Found workspace {ws_data.ws_name}")
        phi_conf.refresh_ws_config(ws_data.ws_name)

    # If the ws_data is still None it means the workspace is corrupt
    if ws_data is None:
        logger.error(f"Could not add workspace from: {ws_root_path}")
        logger.error("Please try again")
        return False

    ######################################################
    # 1.4 Set workspace as active
    ######################################################
    phi_conf.active_ws_name = ws_data.ws_name
    is_active_ws = True

    ######################################################
    # 1.5 Check if remote origin is available
    ######################################################
    _remote_origin_url: Optional[str] = get_remote_origin_for_dir(ws_root_path)
    logger.debug("Git origin: {}".format(_remote_origin_url))

    ######################################################
    ## 2. Create or Update WorkspaceSchema (if user is logged in)
    ######################################################
    if phi_conf.user is not None:
        # If a ws_schema exists for this workspace, this workspace has a record in the backend
        ws_schema: Optional[WorkspaceSchema] = ws_data.ws_schema

        ######################################################
        # 2.1 Create WorkspaceSchema for NEW WORKSPACE
        ######################################################
        if ws_schema is None:
            from phiterm.api.workspace import create_workspace

            # If ws_schema is None, this is a NEWLY CREATED WORKSPACE.
            # We make a call to the backend to create a new ws_schema
            logger.debug("Creating ws_schema for new workspace")
            logger.debug("ws_name: {}".format(ws_data.ws_name))
            logger.debug("is_active_ws: {}".format(is_active_ws))

            ws_schema = create_workspace(
                user=phi_conf.user,
                workspace=WorkspaceSchema(
                    ws_name=ws_data.ws_name,
                    is_primary_ws_for_user=is_active_ws,
                ),
            )
            if ws_schema is not None:
                phi_conf.update_ws_data(ws_name=ws_data.ws_name, ws_schema=ws_schema)
        ######################################################
        # 2.2 Update WorkspaceSchema for EXISTING WORKSPACE
        ######################################################
        else:
            from phiterm.api.workspace import update_workspace

            logger.debug("Updating ws_schema for existing workspace")
            logger.debug("ws_name: {}".format(ws_data.ws_name))
            logger.debug("is_active_ws: {}".format(is_active_ws))

            ws_schema.is_primary_ws_for_user = is_active_ws
            ws_schema_updated = update_workspace(
                user=phi_conf.user,
                workspace=ws_schema,
            )
            if ws_schema_updated is not None:
                # Update the ws_schema for this workspace.
                phi_conf.update_ws_data(
                    ws_name=ws_data.ws_name, ws_schema=ws_schema_updated
                )

    ######################################################
    # 3. Refresh PhiWsData and Complete Workspace setup
    ######################################################
    # Refresh ws_data because phi_conf.update_ws_data() will create a new ws_data object in PhiConf
    ws_data = cast(PhiWsData, phi_conf.get_ws_data_by_name(ws_data.ws_name))

    # Check if workspace is valid and complete setup
    ws_is_valid, pending_actions = phi_conf.validate_workspace(ws_name=ws_data.ws_name)
    if ws_is_valid and ws_data.ws_config is not None:
        scripts_dir = ws_data.ws_config.scripts_dir
        install_deps_file = f"sh {ws_root_path}/{scripts_dir}/install.sh"
        print_subheading(f"Setup complete! Next steps:")
        print_info("1. Deploy workspace:")
        print_info("\tphi ws up")
        print_info("2. Install workspace dependencies:")
        print_info(f"\t{install_deps_file}")
        return True
    else:
        print_info(f"Workspace setup pending")
        print_howtofix_pending_actions(pending_actions)
        return False

    ######################################################
    ## End Workspace setup
    ######################################################


def filter_and_prep_configs(
    ws_config: WorkspaceConfig,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    order: Optional[str] = "create",
) -> List[InfraConfig]:
    from phidata.utils.prep_infra_config import prep_infra_config

    # Step 1. Filter configs
    # 1.1: Filter by config type: docker/k8s/aws
    filtered_configs: List[InfraConfig] = []
    if target_config is None:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        if order == "delete":
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
        else:
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
    elif target_config == WorkspaceConfigType.docker:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        else:
            logger.error("No DockerConfig provided")
    elif target_config == WorkspaceConfigType.k8s:
        if ws_config.k8s is not None:
            filtered_configs.extend(ws_config.k8s)
        else:
            logger.error("No K8sConfig provided")
    elif target_config == WorkspaceConfigType.aws:
        if ws_config.aws is not None:
            filtered_configs.extend(ws_config.aws)
        else:
            logger.error("No AwsConfig provided")

    # 1.2: Filter by env: dev/stg/prd
    configs_after_env_filter: List[InfraConfig] = []
    if target_env is None or target_env == "all":
        configs_after_env_filter = filtered_configs
    else:
        for config in filtered_configs:
            if config.env is None:
                continue
            if target_env == config.env:
                configs_after_env_filter.append(config)
    # logger.debug("Filtered configs: {}`".format(configs_after_env_filter))

    # Step 2. Prepare configs
    ready_to_use_configs: List[InfraConfig] = []
    for config in configs_after_env_filter:
        if not isinstance(config, InfraConfig):
            logger.error(f"{config} is not an instance of InfraConfig")
            continue
        if not config.is_valid():
            logger.warning(f"Skipping {config.__class__}\n")
            continue
        if not config.enabled:
            logger.debug(
                f"{config.__class__.__name__} for env {config.__class__.env} disabled"
            )
            continue

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        ######################################################################

        _config = prep_infra_config(
            infra_config=config,
            ws_config=ws_config,
        )
        ready_to_use_configs.append(_config)

    # Return filtered and prepared configs
    return ready_to_use_configs


def deploy_workspace(
    ws_data: PhiWsData,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Deploy a Phidata Workspace. This is called from `phi ws up`"""
    from phidata.docker.config import DockerConfig
    from phidata.k8s.config import K8sConfig
    from phidata.aws.config import AwsConfig

    if ws_data is None is None:
        logger.error("WorkspaceConfig invalid")
        return

    ws_config: WorkspaceConfig = ws_data.ws_config
    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    configs_to_deploy: List[InfraConfig] = filter_and_prep_configs(
        ws_config=ws_config,
        target_env=target_env,
        target_config=target_config,
        order="create",
    )

    num_configs_to_deploy = len(configs_to_deploy)
    num_configs_deployed = 0
    for config in configs_to_deploy:
        logger.debug(f"Deploying {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import deploy_docker_config

            deploy_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import deploy_k8s_config

            deploy_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import deploy_aws_config

            deploy_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        # white space between runs
        print_info("")

    print_info(f"# Configs deployed: {num_configs_deployed}/{num_configs_to_deploy}\n")
    if num_configs_to_deploy == num_configs_deployed:
        if not dry_run:
            print_subheading("Workspace deploy success")
    else:
        logger.error("Workspace deploy failed")


def shutdown_workspace(
    ws_data: PhiWsData,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Shutdown the Phidata Workspace. This is called from `phi ws down`"""
    from phidata.docker.config import DockerConfig
    from phidata.k8s.config import K8sConfig
    from phidata.aws.config import AwsConfig

    if ws_data is None is None:
        logger.error("WorkspaceConfig invalid")
        return

    ws_config: WorkspaceConfig = ws_data.ws_config
    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    configs_to_shutdown: List[InfraConfig] = filter_and_prep_configs(
        ws_config=ws_config,
        target_env=target_env,
        target_config=target_config,
        order="delete",
    )

    num_configs_to_shutdown = len(configs_to_shutdown)
    num_configs_shutdown = 0
    for config in configs_to_shutdown:
        logger.debug(f"Shutting down {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import shutdown_docker_config

            shutdown_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import shutdown_k8s_config

            shutdown_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import shutdown_aws_config

            shutdown_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        # white space between runs
        print_info("")

    print_info(
        f"\n# Configs shutdown: {num_configs_shutdown}/{num_configs_to_shutdown}"
    )
    if num_configs_to_shutdown == num_configs_shutdown:
        if not dry_run:
            print_subheading("Workspace shutdown success")
    else:
        print_subheading("Workspace shutdown failed")


def patch_workspace(
    ws_data: PhiWsData,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Patch the Phidata Workspace. This is called from `phi ws patch`"""
    from phidata.docker.config import DockerConfig
    from phidata.k8s.config import K8sConfig
    from phidata.aws.config import AwsConfig

    if ws_data is None is None:
        logger.error("WorkspaceConfig invalid")
        return

    ws_config: WorkspaceConfig = ws_data.ws_config
    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    configs_to_patch: List[InfraConfig] = filter_and_prep_configs(
        ws_config=ws_config,
        target_env=target_env,
        target_config=target_config,
        order="create",
    )

    num_configs_to_patch = len(configs_to_patch)
    num_configs_patched = 0
    for config in configs_to_patch:
        logger.debug(f"Patching {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import patch_docker_config

            patch_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import patch_k8s_config

            patch_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import patch_aws_config

            patch_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        # white space between runs
        print_info("")

    print_info(f"\n# Configs patched: {num_configs_patched}/{num_configs_to_patch}")
    if num_configs_to_patch == num_configs_patched:
        if not dry_run:
            print_subheading("Workspace patch success")
    else:
        print_subheading("Workspace patch failed")


def set_workspace_as_active(ws_name: Optional[str], refresh: bool = True) -> bool:
    from phiterm.api.workspace import update_primary_workspace

    ######################################################
    ## 1. Validate Pre-requisites
    ######################################################
    ######################################################
    # 1.1 Check PhiConf is valid
    ######################################################
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return False

    ######################################################
    # 1.2 Check ws_root_path is valid
    ######################################################
    # By default, we assume this command is run from the workspace directory
    ws_root_path: Optional[Path] = None
    if ws_name is None:
        # If the user does not provide a ws_name, that implies `phi set` is ran from
        # the workspace directory.
        ws_root_path = Path(".").resolve()
    else:
        # If the user provides a workspace name manually, we find the dir for that ws
        ws_root_path = phi_conf.get_ws_root_path_by_name(ws_name)
        if ws_root_path is None:
            logger.error(f"Could not find workspace {ws_name}")
            return False

    ws_dir_is_valid: bool = (
        ws_root_path is not None and ws_root_path.exists() and ws_root_path.is_dir()
    )
    if not ws_dir_is_valid:
        logger.error("Invalid workspace directory: {}".format(ws_root_path))
        return False

    ######################################################
    # 1.3 Validate PhiWsData is available i.e. a workspace is available at this directory
    ######################################################
    logger.debug(f"Checking for a workspace at path: {ws_root_path}")
    active_ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_path(ws_root_path)
    if active_ws_data is None:
        # This happens when the workspace is not yet setup
        print_info(f"Could not find a workspace at path: {ws_root_path}")
        print_info(
            f"If this workspace has not been setup, please run `phi ws setup` from the workspace directory"
        )
        return False

    new_active_ws_name: str = active_ws_data.ws_name
    print_heading(f"Setting workspace {new_active_ws_name} as active")
    if refresh:
        try:
            phi_conf.refresh_ws_config(new_active_ws_name)
        except WorkspaceException as e:
            logger.error(
                "Could not refresh workspace config, please fix errors and try again"
            )
            logger.error(e)
            return False

    ######################################################
    # 1.4 Make api request if updating active workspace
    ######################################################
    logger.debug("Updating active workspace api")

    if phi_conf.user is not None:
        ws_schema: Optional[WorkspaceSchema] = active_ws_data.ws_schema
        if ws_schema is None:
            logger.warning(
                f"Please setup {new_active_ws_name} by running `phi ws setup`"
            )
        else:
            updated_workspace_schema = update_primary_workspace(
                user=phi_conf.user,
                workspace=ws_schema,
            )
            if updated_workspace_schema is not None:
                # Update the ws_schema for this workspace.
                phi_conf.update_ws_data(
                    ws_name=new_active_ws_name, ws_schema=updated_workspace_schema
                )

    ######################################################
    ## 2. Set workspace as active
    ######################################################
    phi_conf.active_ws_name = new_active_ws_name
    print_info("Active workspace updated")
    return True


def delete_workspace(ws_to_delete: Optional[List[str]], phi_conf: PhiConf) -> bool:
    from phiterm.api.workspace import delete_workspaces_api

    if ws_to_delete is None or len(ws_to_delete) == 0:
        return True

    logger.debug(f"Deleting workspaces: {ws_to_delete}")
    workspaces_deleted = delete_workspaces_api(
        user=phi_conf.user, workspaces_to_delete=ws_to_delete
    )
    if workspaces_deleted:
        pass
        # phi_conf.delete_ws_data(ws_name=ws)
    return workspaces_deleted


def print_workspace_status(
    ws_data: PhiWsData,
    target_env: Optional[str] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Print the Workspace status. This is called from `phi ws status`"""
    from phidata.docker.config import DockerConfig
    from phidata.k8s.config import K8sConfig
    from phidata.aws.config import AwsConfig

    if ws_data is None is None:
        logger.error("WorkspaceConfig invalid")
        return

    ws_config: WorkspaceConfig = ws_data.ws_config
    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    configs_to_patch: List[InfraConfig] = filter_and_prep_configs(
        ws_config=ws_config,
        target_env=target_env,
        target_config=target_config,
        order="create",
    )

    num_configs_to_patch = len(configs_to_patch)
    num_configs_patched = 0
    for config in configs_to_patch:
        logger.debug(f"Patching {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import patch_docker_config

            # print_docker_config_status(
            #     config=config,
            #     name_filter=target_name,
            #     type_filter=target_type,
            #     app_filter=target_app,
            #     dry_run=dry_run,
            #     auto_confirm=auto_confirm,
            # )
            num_configs_patched += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import patch_k8s_config

            # print_k8s_config_status(
            #     config=config,
            #     name_filter=target_name,
            #     type_filter=target_type,
            #     app_filter=target_app,
            #     dry_run=dry_run,
            #     auto_confirm=auto_confirm,
            # )
            num_configs_patched += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import patch_aws_config

            # print_aws_config_status(
            #     config=config,
            #     name_filter=target_name,
            #     type_filter=target_type,
            #     app_filter=target_app,
            #     dry_run=dry_run,
            #     auto_confirm=auto_confirm,
            # )
            num_configs_patched += 1
        # white space between runs
        print_info("")


######################################################
## TODO: Delete deprecated functions
######################################################
#
# def create_new_workspace(ws_name: str, template: WorkspaceStarterTemplate) -> bool:
#     """Creates a new workspace for the user.
#     This function clones a phidata template on the users machine at the path:
#         cwd/ws_name
#     cwd: current working dir - where the command was run from.
#
#     Steps:
#     1. Validate ws_name and if we can create a folder with that name
#     2. Clone the starter template in cwd/ws_name
#     3. Delete the .git folder
#     4. Provide the user with steps to add a remote origin for this workspace
#
#     NOTE: till the user runs `phi ws setup` the workspace is not registered with phidata
#         and can only be used locally
#     """
#     from shutil import copytree
#     from phiterm.utils.filesystem import rmdir_recursive
#     from phiterm.workspace.ws_utils import get_ws_config_dir_path
#     from phiterm.utils.git import GitCloneProgress
#
#     current_dir: Path = Path(".").resolve()
#
#     # Phidata should be initialized before creating a workspace
#     phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not phi_conf:
#         print_conf_not_available_msg()
#         return False
#
#     # Check if a workspace with the same name exists
#     _existing_ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_name(ws_name)
#     if _existing_ws_data is not None:
#         logger.error(f"Found existing record for a workspace: {ws_name}")
#         delete_existing_ws_data = typer.confirm(
#             "Replace the existing record?", default=True
#         )
#         if delete_existing_ws_data:
#             phi_conf.delete_ws(ws_name)
#         else:
#             return False
#
#     # Check if we can create the workspace in the current dir
#     ws_root_path: Path = current_dir.joinpath(ws_name)
#     if ws_root_path.exists():
#         logger.error(
#             f"Directory {ws_root_path} exists, please delete files manually or choose another name for workspace"
#         )
#         return False
#
#     print_info(f"Creating {str(ws_root_path)}")
#     # Clone the starter repo for this cloud in the new directory
#     repo_to_clone = TEMPLATE_TO_REPO_MAP.get(template)
#     logger.debug("Cloning: {}".format(repo_to_clone))
#     try:
#         _cloned_git_repo: git.Repo = git.Repo.clone_from(
#             repo_to_clone, str(ws_root_path), progress=GitCloneProgress()  # type: ignore
#         )
#     except Exception as e:
#         logger.error(e)
#         return False
#
#     # Remove existing .git folder
#     _dot_git_folder = ws_root_path.joinpath(".git")
#     _dot_git_exists = _dot_git_folder.exists()
#     if _dot_git_exists:
#         logger.debug(f"Deleting {_dot_git_folder}")
#         try:
#             _dot_git_exists = not rmdir_recursive(_dot_git_folder)
#         except Exception as e:
#             logger.warning(f"Failed to delete {_dot_git_folder}: {e}")
#             logger.info("Please delete the .git folder manually")
#             pass
#
#     phi_conf.add_new_ws_to_config(
#         ws_name=ws_name,
#         ws_root_path=ws_root_path,
#     )
#
#     try:
#         ws_config_dir_path: Path = get_ws_config_dir_path(ws_root_path)
#         ws_config_secrets_dir = ws_config_dir_path.joinpath("secrets").resolve()
#         ws_config_example_secrets_dir = ws_config_dir_path.joinpath(
#             "example_secrets"
#         ).resolve()
#
#         print_info(f"Creating {str(ws_config_secrets_dir)}")
#         copytree(
#             str(ws_config_example_secrets_dir),
#             str(ws_config_secrets_dir),
#         )
#     except Exception as e:
#         logger.warning(f"Could not create workspace/secrets: {e}")
#         logger.warning(
#             "Please manually copy workspace/example_secrets to workspace/secrets"
#         )
#
#     print_info(f"Your new workspace is available at {str(ws_root_path)}\n")
#     return setup_workspace(ws_root_path=ws_root_path)
#
#
# def create_workspace_using_input():
#     """Takes input from the user and calls create_new_workspace()"""
#
#     from phiterm.utils.common import is_empty, str_to_int
#
#     # Display available starter templates and ask user to select one
#     print_info("Input Template Number (default: ai-app)")
#     templates = WorkspaceStarterTemplate.values_list()
#     for idx, prvdr in enumerate(templates, start=1):
#         print_info("  [{}] {}".format(idx, prvdr))
#
#     # Get starter template from the user
#     template_inp_raw = input(": ")
#     # Convert input to int value.
#     template_inp = str_to_int(template_inp_raw)
#     template: WorkspaceStarterTemplate = WorkspaceStarterTemplate.api_app
#
#     if template_inp is not None:
#         try:
#             template = cast(
#                 WorkspaceStarterTemplate,
#                 WorkspaceStarterTemplate.from_str(templates[template_inp - 1]),
#             )
#         except Exception as e:
#             logger.error(e)
#     logger.debug("Selected: {}".format(template.value))
#
#     # Get workspace name from user
#     default_ws_name = TEMPLATE_TO_NAME_MAP.get(template, DEFAULT_WS_NAME)
#     ws_name_inp_raw = input(f"Workspace name (default: {default_ws_name}): ")
#     if is_empty(ws_name_inp_raw):
#         ws_name_inp_raw = default_ws_name
#
#     print_info(
#         f"Creating workspace {ws_name_inp_raw} using the {template.value} template\n"
#     )
#     create_new_workspace(ws_name_inp_raw, template)
#
#
# def initialize_workspace() -> None:
#     """Initialize a phidata workspace.
#
#     This function is called by `phi ws create` to create a new workspace.
#     """
#     phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not phi_conf:
#         print_conf_not_available_msg()
#         return
#
#     print_heading("New phidata workspace")
#     create_workspace_using_input()
#
# def print_git_setup(
#     ws_name: str,
#     ws_root_path: Path,
#     version_control_provider: Optional[
#         VersionControlProviderEnum
#     ] = VersionControlProviderEnum.GITHUB,
# ) -> None:
#     """Prints commands to setup a remote git repo for a workspace"""
#     from phiterm.utils.git import get_remote_origin_for_dir
#
#     # Check if a remote origin is available
#     _remote_origin_url: Optional[str] = get_remote_origin_for_dir(ws_root_path)
#     # logger.debug("_remote_origin_url: {}".format(_remote_origin_url))
#     if _remote_origin_url:
#         print_info(f"Remote origin already set: {_remote_origin_url}")
#         return
#
#     create_new_git_repo_url = "https://github.com/new"
#     create_remote_repo_url: str
#     # TODO: Add more repo urls
#     if version_control_provider == VersionControlProviderEnum.GITHUB:
#         create_remote_repo_url = create_new_git_repo_url
#     else:
#         create_remote_repo_url = create_new_git_repo_url
#
#     print_subheading(f"\nSteps to setup a git repo for workspace: {ws_name}")
#     print_info(f"\nCreate a new git repo named {ws_name} at {create_remote_repo_url}")
#     print_info(
#         f"Then follow the following steps to initialize the directory {ws_name} as a git repo and run git push"
#     )
#     print_info(
#         f"NOTE: These steps will be provided by your version control provider (github, gitlab..), but would look something like:"
#     )
#     print_info(f"       git init")
#     print_info(f"       git add .")
#     print_info(f"       git commit -m 'Init Phidata Workspace'")
#     print_info(f"       git branch -M main")
#     print_info(
#         f"       git remote add origin https://github.com/<USERNAME>/{ws_name}.git"
#     )
#     print_info(f"       git push -u origin main")
#     print_info(f"Run `phi ws setup` after running git push to update your workspace\n")
#
#     _open_browser = typer.confirm(
#         f"Would you like to open your browser to visit: {create_remote_repo_url}\n-->"
#     )
#     if _open_browser:
#         typer.launch(create_remote_repo_url)
#
#
# def clone_workspace(ws_to_clone: WorkspaceSchema, phi_conf: PhiConf) -> None:
#     """Clones an available phidata workspace on the users machine. To clone a ws, the PhiConf
#     already has the ws_data and ws_schema available. We then update the
#     ws_root_path and ws_config_file_path in the ws_data. After updating the
#     path, we're call setup_workspace() to go through our usual setup flow
#     """
#     from phiterm.utils.git import GitCloneProgress
#     from phiterm.workspace.ws_utils import get_ws_config_file_path
#
#     # Check if we can create the workspace in the current dir
#     current_dir: Path = Path("../../workspace").resolve()
#     logger.debug(f"current_dir: {current_dir}")
#     ws_root_path: Path = current_dir.joinpath(ws_to_clone.name)
#     if ws_root_path.exists():
#         logger.error(
#             f"{ws_root_path} already exists, please choose another directory to clone or delete the existing dir and run `phi ws create` again"
#         )
#         return
#
#     print_info(f"Creating {str(ws_root_path)}")
#     # Clone the workspace repo in ws_root_path
#     repo_to_clone = ws_to_clone.git_url
#     _cloned_git_repo: git.Repo = git.Repo.clone_from(
#         repo_to_clone, str(ws_root_path), progress=GitCloneProgress()  # type: ignore
#     )
#     # Validate ws_root_path exists and is a directory
#     if not (ws_root_path.exists() and ws_root_path.is_dir()):
#         logger.error(f"Could not clone workspace, please try again")
#         return
#     # Get ws_config_file_path and validate
#     ws_config_file_path: Path = get_ws_config_file_path(ws_root_path)
#     if not (ws_config_file_path.exists() and ws_config_file_path.is_file()):
#         logger.error(f"Could not find workspace config at: {ws_config_file_path}")
#         return
#     # Update the ws_data in PhiConf
#     phi_conf.update_ws_data(
#         ws_name=ws_to_clone.ws_name,
#         ws_root_path=ws_root_path,
#         ws_config_file_path=ws_config_file_path,
#     )
#     setup_workspace(ws_root_path)
#
#
# def init_workspace_data(ws_schema: WorkspaceSchema, phi_conf: PhiConf):
#     """Initializes workspace data like cloud projects"""
#
#     logger.debug("*=* Initializing workspace data for: {}".format(ws_schema.name))
#     logger.debug("TO_BE_IMPLEMENTED")
#     logger.debug("*=* Workspace data init complete: {}".format(ws_schema.name))
#
# def import_workspace():
#     # TODO: use code to clone/import existing workspace later
#     available_ws = phi_conf.available_ws
#     if available_ws:
#         print_info("Would you like to:")
#         print_info("  [1] Create a new workspace")
#         print_info("  [2] Clone an existing workspace")
#         print_info("  [3] Enter any other key to exit")
#         ws_inp_raw = input("--> ")
#         ws_inp_int = str_to_int(ws_inp_raw)
#         if ws_inp_int == 1:
#             create_workspace_using_input()
#         elif ws_inp_int == 2:
#             print_info("\nSelect workspace to clone:")
#             for idx, avl_ws in enumerate(available_ws, start=1):
#                 print_info("  [{}] {}".format(idx, avl_ws.name))
#             clone_ws_inp_raw = input("--> ")
#             clone_ws_inp_int = str_to_int(clone_ws_inp_raw)
#             if clone_ws_inp_int:
#                 ws_to_clone = available_ws[clone_ws_inp_int - 1]
#                 clone_workspace(ws_to_clone, phi_conf)
#             return
#         return
#     else:
#
