""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import List, Optional

from mcli import config
from mcli.api.model.run_model import RunModel
from mcli.models import PartialRunInput, RunInput
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.platforms.platform import PriorityLabel
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_kube import (PodStatusEpilog, delete_config_map, delete_job, delete_service, stream_pod_logs,
                                   wait_for_job_pods, wait_for_pod_start, watch_pod_events)
from mcli.utils.utils_logging import FAIL, INFO, OK, console, get_indented_block

logger = logging.getLogger(__name__)


def run_entrypoint(
    file: str,
    experimental: Optional[List[ExperimentalFlag]] = None,
    priority: Optional[PriorityLabel] = None,
    tail: bool = True,
    **kwargs,
) -> int:
    del kwargs
    # TODO: Reintroduce experimental
    del experimental
    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    partial_run_input = PartialRunInput.from_file(path=file)
    run_input = RunInput.from_partial_run_input(partial_run_input)
    mcli_job = run(run_input=run_input, priority=priority)

    if tail:
        with MCLIPlatform.use(mcli_job.platform.mcli_platform) as platform:
            logger.info(f'{INFO} Run {mcli_job.run_name} submitted. Waiting for it to start...')
            logger.info(f'{INFO} Press Ctrl+C to quit and follow your run manually.')
            with console.status('Waiting for run to be scheduled...') as status:
                epilog = PodStatusEpilog(status)
                logger.debug(f'Getting pods for job: {mcli_job.unique_name}')
                pod_names = wait_for_job_pods(name=mcli_job.unique_name, namespace=platform.namespace)
                pod_name = pod_names[0]
                logger.debug(f'Found pod: {pod_name}')
                last_event = watch_pod_events(platform.namespace, epilog, name=pod_name, timeout=300)
                pod_created = False
                if last_event and last_event.status == 'Started':
                    status.update('Verifying run has fully started...')
                    pod_created = wait_for_pod_start(pod_name, platform.namespace)
                elif last_event and last_event.status == 'Failed':
                    status.stop()
                    logger.error(
                        f'{FAIL} [bold bright red]Run {mcli_job.unique_name} failed to start and will be deleted.[/]\n')
                    if 'docker login' in last_event.message:
                        error_message = f"""
                            Could not find Docker image "{run_input.image}". If this is a private image, check
                            `mcli get secret` to ensure that you have a Docker secret created. If not, create one
                            using `mcli create secret docker`. Otherwise, double-check your image name.
                        """
                        logger.error(get_indented_block(error_message))
                    else:
                        logger.error('Reason:\n')
                        logger.error(get_indented_block(str(last_event)))
                    status.start()
                    status.update('Deleting failed run...')
                    delete_job(name=mcli_job.unique_name, namespace=platform.namespace)
                    delete_config_map(name=mcli_job.unique_name, namespace=platform.namespace)
                    delete_service(name=mcli_job.unique_name, namespace=platform.namespace)
                    return 1
                elif last_event and last_event.type == 'Warning':
                    status.stop()
                    logger.error(f'{FAIL} Run {mcli_job.unique_name} seems to have failed.')
                    return 1

            if pod_created:
                logger.info(f'{OK} Run {mcli_job.run_name} started')
                logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')
                for line in stream_pod_logs(pod_name, platform.namespace):
                    print(line)
            else:
                # TODO: Figure out what else to do here. Where do we want to redirect people
                # to if we don't assume kubectl install?
                logger.warning(('Run is taking awhile to start, returning you to the command line.\n'
                                'Common causes are the run is queued because the resources are not available '
                                'yet, or the docker image is taking awhile to download.\n\n'
                                'To continue to view job status, use `mcli get runs` and `mcli logs`.'))

    return 0


def run(run_input: RunInput, priority: Optional[PriorityLabel] = None) -> MCLIJob:
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        run_model = RunModel.from_run_input(run_input=run_input)
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs.create_run import create_run
        if not create_run(run_model):
            logger.warning(f'{FAIL} Failed to persist run')

    # Populates the full MCLI Job including user defaults
    mcli_job = MCLIJob.from_run_input(run_input=run_input)

    runner = Runner()
    priority_class = priority.value if priority else None
    runner.submit(job=mcli_job, priority_class=priority_class)
    return mcli_job


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.',
    )

    parser.add_argument(
        '--priority',
        choices=list(PriorityLabel),
        type=PriorityLabel.ensure_enum,
        help='Priority level at which runs should be submitted. '
        '(default None)',
    )

    parser.add_argument(
        '--no-tail',
        action='store_false',
        dest='tail',
        help='Do not automatically try to follow the run\'s logs',
    )
