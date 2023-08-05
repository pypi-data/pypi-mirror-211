import time
from report_ranger.imports import vulnerability
from report_ranger.config import get_config  # Configuration settings within report ranger
from report_ranger.errors import InputError
from report_ranger.report import Report
from report_ranger.template import Template
from report_ranger.templatemapper import process_templatemapper
import os
import jinja2
import logging
from watchdog.observers import Observer
from report_ranger.watcher import Watcher
import argparse

from report_ranger.utils.jinja_helpers import log_jinja2_error

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Report Manager collects together a bunch of markdown files to create a master markdown file that is suitable to use with Pandoc and Latex to build a PDF file.")
    parser.add_argument('-i', '--input', type=str,
                        help='The main report file to process')
    parser.add_argument('-o', '--output', type=str,
                        help='The file to output the final markdown to. If given a directory, the filename will be whatever is suggested by the report or template.')
    parser.add_argument('-f', '--format', type=str,
                        default='', help='The format to target (options are "latex", "pdf", "docx"). Defaults to whatever the extension tells us.')
    parser.add_argument('-w', '--watch', action='store_true', default=False,
                        help='Watch files for changes and recompile if they are identified')
    parser.add_argument('--watch_mode', type=str, default='',
                        help='Watch file mode, can be set to "os" or "modified"')
    parser.add_argument('-m', '--templatemapper', type=str, default='',
                        help='A template mapper file which holds a YAML mapping from a template name to a related file.')
    parser.add_argument('-c', '--config', type=str, default='',
                        help='The location of a config file in YAML format.')
    parser.add_argument('-t', '--template', type=str, default='',
                        help='The template file. Associated images should be in the same directory. Defaults to what is set in the report.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help=f'Turn on verbose mode.')

    args = parser.parse_args()

    # Turn on verbose mode
    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=logging.WARNING)

    config = get_config(args.config)

    input = args.input if args.input else config['default_input_file'] if 'default_input_file' in config else None
    if input == None:
        raise Exception("Could not figure out an input file")
    output_file = args.output if args.output else config['default_output_file'] if 'default_output_file' in config else None
    if output_file == None:
        raise Exception("Could not figure out an output file")

    parentdir = os.path.dirname(os.path.join(os.path.curdir, input))

    # We need to change the current working directory to the directory of the template otherwise relative
    # paths inside the template won't work. For instance you won't be able to include executivesummary.md
    rr_parent_folder = os.path.abspath(os.path.curdir)

    ctm = config['templatemapper'] if 'templatemapper' in config else {}        
    ctms = config['templatemappers'] if 'templatemappers' in config else []

    templatemapper = process_templatemapper(args.templatemapper, ctm, ctms)

    if args.template:
        if args.template in templatemapper:
            templatefile = templatemapper[args.template]
        else:
            templatefile = os.path.abspath(args.template)
    else:
        templatefile = ''

    os.chdir(parentdir)
    parentdir = '.'
    mdfile = os.path.basename(input)

    # Get the template
    report = Report(
        mdfile,
        templatefile=templatefile,
        templatemapper=templatemapper,
        default_template=config['default_template'])

    # Get the extension of the output file
    if output_file:
        fn, ext = os.path.splitext(output_file)
    else:
        ext = 'md'

    # Figure out what target we have
    if args.format == "pdf":
        target = "latex"
        docformat = "pdf"
    if args.format == "pdf-latex":
        target = "latex"
        docformat = "pdf"
    elif args.format == "markdown-latex":
        target = "latex"
        docformat = "markdown"
    elif args.format == "typst":
        target = "typst"
        docformat = "typst"
    elif args.format == "markdown":
        target = "markdown"
        docformat = "markdown"
    elif args.format == "docx":
        target = "docx"
        docformat = "docx"
    elif args.format == "html":
        target = "html"
        docformat = "html"
    elif args.format == "csv":
        target = "csv"
        docformat = "csv"
    else:
        if ext == ".docx":
            target = "docx"
            docformat = "docx"
            log.info("Setting target and format to docx")
        elif ext == ".md" or ext == ".rr":
            target = "markdown"
            docformat = "md"
            log.info("Setting target to markdown and format to md")
        elif ext == ".typ":
            target = "typst"
            docformat = "typst"
            log.info("Setting target to markdown and format to md")
        elif ext == ".html":
            target = "html"
            docformat = "html"
            log.info("Setting target and format to html")
        elif ext == ".csv":
            target = "csv"
            docformat = "csv"
            log.info("Setting target and format to csv")
        else:  # Default to PDF
            target = "latex"
            docformat = "pdf"
            log.info("Setting target to latex and format to pdf")

    # Pandoc does not support PDF output to stdout, so we need to hack it by
    # making a symlink to /dev/stdout and outputting to that file
    stdout_link = None
    if docformat.lower() == 'pdf' and output_file == '-':
        stdout_link = '/tmp/stdout.pdf'
        os.symlink('/dev/stdout', stdout_link)
        output_file = stdout_link

    # Convert output file path into full path if relative path is given
    if output_file and output_file[0] != '/':
        output_file = os.path.join(rr_parent_folder, output_file)


    if args.watch:
        log.info("Starting watch")
        try:
            watcher = Watcher(log.info, "Callback")
            watcher.set_callback(report.process_file, mdfile, target, docformat, output_file, default_output_file=config.get('default_output_file'), watcher=watcher)
            watcher.set_watch_mode(args.watch_mode)
            output = report.process_file(mdfile, target, docformat, output_file, default_output_file=config.get('default_output_file'), watcher=watcher)
            if args.watch_mode != "modified":
                log.info("Setting watch mode to os")
                observer = Observer()
                observer.schedule(watcher, parentdir, recursive=True)
                observer.start()
                try:
                    while True:
                        time.sleep(5)
                        watcher.run()
                finally:
                    observer.stop()
                    observer.join()
            else:
                log.info("Setting watch mode to modification time")
                while True:
                    try:
                        time.sleep(5)
                        watcher.run()
                    except InputError as ie:
                        log.error("Input Error: {}".format(ie.message))
                        exit()
                    except jinja2.exceptions.TemplateSyntaxError as error:
                        log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                            error.message, error.lineno, error.filename))
                        log_jinja2_error(mdfile, error)
                        exit()

        except InputError as ie:
            log.error("Input Error: {}".format(ie.message))
        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                error.message, error.lineno, error.filename))
            log_jinja2_error(mdfile, error)
    else:
        try:
            output = report.process_file(mdfile, target, docformat, output_file, default_output_file=config.get('default_output_file'))
        except InputError as ie:
            log.error("Input Error: {}".format(ie.message))
            exit()
        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error("Final report processing Jinja2 error: {} at lineno {} for file {}".format(
                error.message, error.lineno, error.filename))
            log_jinja2_error(mdfile, error)
            exit()

        # If we're outputting to stdout, remove the link
        if stdout_link and os.path.exists(stdout_link):
            os.remove(stdout_link)
