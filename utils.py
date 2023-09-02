import argparse
import json
import logging
import re
from itertools import chain
from rapidfuzz import process, fuzz

# LOGGING AND CONFIG

def setup_logging():
    # 'INFO' level by default, could be specified by the user (for later)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def parse_arguments():
    parser = argparse.ArgumentParser(description="goodreads_rebot")
    parser.add_argument('--config', type=str, required=True, help="Path to configuration JSON file")
    args = parser.parse_args()
    return args

def load_config(args):
    """
    Load config dictionary from json path provided by user
    :param args: arguments parsed (with argparse library)
    :return: Dictionary
    """
    try:
        with open(args.config, 'r') as json_file:
            config_dict = json.load(json_file)
        return config_dict
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"The file {args.config} is not a valid JSON file: {str(e)}")

config = load_config(parse_arguments())


# MATCHING TITLES UTILS:

def extract_braces(comment_body):
    sub_parts = re.findall(r'\{\{([^}]*)\}\}', comment_body)
    return sub_parts

def partial_ratio(s1, s2):
    return fuzz.partial_ratio(str.lower(s1), str.lower(s2))

def top_k_matches_list(s, lst, k=3, func="partial", lateralize=True):
    scorer=fuzz.partial_ratio
    if func != "partial":
        scorer=fuzz.ratio
    if lateralize:
        lst = [ss.ljust(len(s), '#') for ss in lst]
    logging.info(f"Matching {s} with a list of len {len(lst)}")
    return process.extract(s, lst, scorer=scorer, limit=k)

def top_k_matches_dic(s, dic, keys, k=3, func="partial", lateralize=True):
    scorer=fuzz.partial_ratio
    if func != "partial":
        scorer=fuzz.ratio
    lst = list(chain(*[dic[key] for key in keys]))
    if lateralize:
        lst = [ss.ljust(len(s), '#') for ss in lst]
    logging.info(f"Matching {s} with a dic on keys : {keys} for a total title list of len {len(lst)}")
    return process.extract(s, lst, scorer=scorer, limit=k)


