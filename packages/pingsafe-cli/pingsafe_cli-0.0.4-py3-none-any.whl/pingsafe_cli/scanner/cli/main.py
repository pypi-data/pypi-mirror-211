import logging
import sys
from sentry_sdk import start_transaction, configure_scope
import pingsafe_cli.scanner.cli.command_line_arguments as CommandLineArgs
from pingsafe_cli.scanner.cli.codescanner import code_scanner
from pingsafe_cli.scanner.cli.config import config
from pingsafe_cli.sentry import init_sentry, drain_sentry
from pingsafe_cli.scanner.cli.registry import MainSubParser, MissingConfig, MissingRequiredFlags, PlatformNotSupported, \
    RequestTimeout, HttpConnectionError, MissingDependencies, SENTRY_TAGS
from pingsafe_cli.scanner.cli.utils import delete_all_cache, \
    initialize_logger, get_cache_directory, get_exit_code_on_crash, send_exception_to_sentry,\
    add_sentry_tags, DownloadException

LOGGER = logging.getLogger("cli")


def main(args, cache_directory):
    if cache_directory != "" and args.invalidate_cache:
        delete_all_cache(cache_directory)
        LOGGER.info("Cache invalidated!")
        return 0

    if args.main_sub_parser == MainSubParser.CODE:
        return code_scanner.handle_code_sub_parser(args, cache_directory)
    elif args.main_sub_parser == MainSubParser.CONFIG:
        return config.set_configs(args)


def start():
    cache_directory = ""
    log_level = 20
    args = None
    try:
        # when pingsafe-cli invoked without any arguments.
        if len(sys.argv) < 2:
            sys.argv.append("--help")

        args = CommandLineArgs.evaluate_command_line_arguments()

        if args.debug:
            log_level = 10
        initialize_logger("cli", log_level)

        cache_directory = get_cache_directory()

        if cache_directory and not args.disable_sentry:
            init_sentry(cache_directory)

        with start_transaction(name=args.main_sub_parser) as transaction:
            exit_code = main(args, cache_directory)
            LOGGER.debug(f"Exiting with code {exit_code}")

            with configure_scope() as scope:
                add_sentry_tags(scope, cache_directory)
                transaction.finish()
                sys.exit(exit_code)
    except MissingDependencies as e:
        LOGGER.warning("Missing some required dependencies.")
        send_exception_to_sentry(e, cache_directory)
        sys.exit(get_exit_code_on_crash(cache_directory))
    except HttpConnectionError as e:
        LOGGER.warning("Something went wrong. Please check your internet connection or contact PingSafe customer "
                       "support.")
        send_exception_to_sentry(e, cache_directory)
        sys.exit(get_exit_code_on_crash(cache_directory))
    except RequestTimeout as e:
        LOGGER.warning("The request timed out.")
        send_exception_to_sentry(e, cache_directory)
        sys.exit(get_exit_code_on_crash(cache_directory))
    except MissingConfig as e:
        LOGGER.warning(
            "Missing required configurations\nTry reconfiguring: pingsafe-cli config --api-token <pingsafe-api-token> "
            "...")
        send_exception_to_sentry(e, cache_directory)
        sys.exit(1)
    except MissingRequiredFlags as e:
        LOGGER.warning(e)
        send_exception_to_sentry(e, cache_directory)
        sys.exit(1)
    except PlatformNotSupported as e:
        LOGGER.warning(e)
        send_exception_to_sentry(e, cache_directory)
        sys.exit(0)
    except DownloadException as e:
        LOGGER.error("Failed to download some required dependencies")
        LOGGER.debug(e)
        msg = str(e) + f", \n\nurl : `{e.url}`" + f", \n\nfile: `{e.filename}`"
        send_exception_to_sentry(DownloadException(msg), cache_directory)
        sys.exit(1)
    except Exception as e:
        if log_level == 10:
            LOGGER.error(str(e))
        code = get_exit_code_on_crash(cache_directory)
        send_exception_to_sentry(e, cache_directory)
        LOGGER.error(f"Something went wrong. Exiting with status code: {code}")
        sys.exit(code)
    finally:
        if args and not args.disable_sentry:
            drain_sentry()


if __name__ == "__main__":
    start()
