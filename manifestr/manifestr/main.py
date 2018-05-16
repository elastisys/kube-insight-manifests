import argparse
import importlib.util
import logging
import os
import re
import shutil
import sys
import traceback

from jinja2 import Environment, FileSystemLoader, Template

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=logging._nameToLevel[LOG_LEVEL],
                    format="%(asctime)s [%(levelname)5.5s] %(message)s")
LOG = logging.getLogger(__name__)

def template_files(root_dir):
    template_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Strip template root path
        dirpath = os.path.relpath(dirpath, root_dir)

        template_paths += [
            os.path.join(dirpath, f) for f in filenames if f.endswith(".j2")
        ]
    return template_paths

def render(root_dir, value_dict, output_dir):
    # LOG.debug("templates: %s", template_files(root_dir))
    for template in template_files(root_dir):
        LOG.debug("rendering %s ...", template)

        # strip trailing .j2
        out_filename = re.sub(r'.j2$', '', os.path.basename(template))
        out_dir = os.path.join(output_dir, os.path.dirname(template))
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_filename)
        LOG.debug("output path: %s", out_path)

        env = Environment(loader=FileSystemLoader([root_dir]))
        template = env.get_template(template)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(template.render(vars=value_dict))


def cli():
    parser = argparse.ArgumentParser(
        prog="manifestr",
        description="A Jinja2 template renderer.")
    parser.add_argument(
        "--values-dict", dest="value_dict_path", required=True,
        help="A .py file containing a single `values` dict with values to be "
        "used for substitutions in template placeholders.")
    parser.add_argument(
        "--template-root-dir", dest="root_dir", required=True,
        help="Directory that will be (recursively) scanned for .j2 files to"
        "be rendered.")
    parser.add_argument(
        "--output-dir", dest="out_dir", default="output",
        help="Directory to which rendered templates are written (with their"
        " .j2 file-ending stripped).")
    parser.add_argument(
        "--overwrite", action="store_true", default=False,
        help="If output directory already exists remove its content prior to"
        "running.")    

    args = parser.parse_args()

    if not os.path.isfile(args.value_dict_path):
        raise ValueError("--values-dict: no such file: {}".format(
            args.value_dict_path))
    # import the value dict as a Python module
    spec = importlib.util.spec_from_file_location(
        "valuedict.module", args.value_dict_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not "values" in module.__dict__:
        raise ValueError("values-dict module {} does not declare a `values` dict".format(args.value_dict_path))
    value_dict = module.values
    if not isinstance(value_dict, dict):
        raise ValueError("values-dict module {}: `values` is of type {}, needs to be a dict".format(args.value_dict_path, type(value_dict)))

    if not os.path.isdir(args.root_dir):
        raise ValueError("--template-root-dir: not a directory: {}".format(
            args.root_dir))
    os.makedirs(args.root_dir, exist_ok=True)

    if os.path.isdir(args.out_dir):
        if (args.overwrite or
            input("overwrite {} (y/n)?".format(args.out_dir)) in ["y","yes"]):
            shutil.rmtree(args.out_dir)
        else:
            LOG.info("aborting ...")
            sys.exit(0)
    
    try:
        render(args.root_dir, value_dict, args.out_dir)
    except Exception as e:
        traceback.print_exc()
        LOG.error("rendering failed: %s", str(e))
