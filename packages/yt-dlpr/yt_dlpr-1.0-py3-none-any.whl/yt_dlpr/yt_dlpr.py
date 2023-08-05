import re
import sys

import yt_dlp
from rich.console import Console
from rich.markup import escape
from rich.style import Style

# Regexes
STARTS_WITH_BRACKET_RE = re.compile(r"^\[(\w+)\] ?(.*)", re.DOTALL)
STARTS_WITH_DELET_RE = re.compile(r"^delet", re.IGNORECASE)

# Extractor names
IE_NAMES = [i.IE_NAME for i in yt_dlp.list_extractors(None)]


def actual_main(namespace):
    # Load from namespace (config file)
    globals().update(namespace)

    # Rich Console
    c = Console(
        highlighter=YtDLPHighlighter(),
        theme=YTDLP_THEME,
        log_time_format=RICH_LOG_TIME_FORMAT,
        log_path=False,
    )

    class RichYoutubeDL(yt_dlp.YoutubeDL):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.rich_console = c
            self.rich_warning_previous = set()

        def rich_log(self, input_message, skip_eol, quiet):
            if quiet:
                return
            if m := STARTS_WITH_BRACKET_RE.match(input_message):
                lvl, msg = m.group(1), m.group(2)

                # Try to pad
                if len(lvl) > (MAX_LEVEL_WIDTH - 2):
                    overflow = 1
                else:
                    overflow = MAX_LEVEL_WIDTH - len(lvl) - 2

                if lvl in RICH_STYLES:
                    style = RICH_STYLES[lvl]
                elif lvl in IE_NAMES:
                    style = Style(underline=True)
                else:
                    style = Style()

                # Log output
                self.rich_console.log(
                    fr"\[[{style}]{lvl}[/]]"            # Level
                    fr"{' ' * overflow}{escape(msg)}",  # Message
                    end="" if skip_eol else "\n",       # End
                )
            elif STARTS_WITH_DELET_RE.match(input_message):
                if "delete" in RICH_STYLES:
                    delete_style = str(RICH_STYLES["delete"])
                else:
                    delete_style = ""
                self.rich_console.log(
                    fr"\[[{delete_style}]deleting[/]] "  # Level
                    fr"{escape(input_message)}",         # Message
                    end="" if skip_eol else "\n",        # End
                )
            else:
                self.rich_console.log(escape(input_message), end="" if skip_eol else "\n")

        def to_screen(self, message, skip_eol=False, quiet=None):
            self.rich_log(message, skip_eol, quiet)

        def to_stdout(self, message, skip_eol=False, quiet=False):
            self.rich_log(message, skip_eol, quiet)

        def report_warning(self, message, only_once=False):
            if self.params.get("logger") is not None:
                self.params["logger"].warning(message)
            else:
                if self.params.get("no_warnings"):
                    return
                if only_once:
                    if message in self.rich_warning_previous:
                        return
                    self.rich_warning_previous.add(message)
                if "WARNING" in RICH_STYLES:
                    warning_style = str(RICH_STYLES["WARNING"])
                else:
                    warning_style = ""
                self.rich_log(
                    fr"\[[{warning_style}]WARNING[/]] "  # Level
                    fr"{escape(message)}",               # Message
                    skip_eol=False, quiet=False          # End
                )

    if "--examples" in sys.argv:
        c.print(EXAMPLES)
        sys.exit(0)

    yt_dlp.workaround_optparse_bug9161()

    yt_dlp.setproctitle('yt-dlp')

    # ℹ️ See the public functions in yt_dlp.YoutubeDL for for other available functions.
    # Eg: "ydl.download", "ydl.download_with_info_file"
    parser, opts, args, old_ydl_opts = yt_dlp.parse_options()

    ydl_opts = {**old_ydl_opts, **RICH_YDL_OPTS}

    if opts.dump_user_agent:
        ua = yt_dlp.traverse_obj(
            opts.headers,
            "User-Agent",
            casesense=False,
            default=yt_dlp.std_headers["User-Agent"],
        )
        c.log(ua)

    with RichYoutubeDL(ydl_opts) as ydl:
        actual_use = args or opts.load_info_filename

        # Remove cache dir
        if opts.rm_cachedir:
            ydl.cache.remove()

        # Update version
        if opts.update_self:
            # If updater returns True, exit. Required for windows
            if yt_dlp.run_update(ydl):
                if actual_use:
                    sys.exit("ERROR: The program must exit for the update to complete")
                sys.exit()

        # Maybe do nothing
        if not actual_use:
            if opts.update_self or opts.rm_cachedir:
                sys.exit()

            ydl.warn_if_short_id(sys.argv[1:] if sys.argv is None else sys.argv)
            parser.error(
                "You must provide at least one URL.\n"
                "Type yt-dlp --help to see a list of all options."
            )

        try:
            if opts.load_info_filename is not None:
                retcode = ydl.download_with_info_file(
                    yt_dlp.expand_path(opts.load_info_filename)
                )
            else:
                retcode = ydl.download(args)
        except yt_dlp.DownloadCancelled:
            ydl.to_screen("Aborting remaining downloads")
            retcode = 101

    sys.exit(retcode)
