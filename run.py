import argparse
import datetime
from src.map import ledger_mapping, apply_mapping
from src.analyze import analyze
from src.parse import parse

PROJECTS = ledger_mapping.keys()

START_YEAR = 2018
END_YEAR = 2024


def valid_date(date_string):
    try:
        time_list = [int(i) for i in date_string.split('-')]
        if len(time_list) == 3:
            datetime.date(time_list[0], time_list[1], time_list[2])
        elif len(time_list) == 2:
            datetime.date(time_list[0], time_list[1], 1)
        elif len(time_list) == 1:
            datetime.date(time_list[0], 1, 1)
    except ValueError:
        raise argparse.ArgumentTypeError("Please use the format YYYY-MM-DD for the timeframe argument "
                                         "(day and / or month can be omitted).")
    return date_string


def main(projects, timeframes, force_parse, entropy_alpha):
    print(f"The ledgers that will be analyzed are: {','.join(projects)}")
    for project in projects:
        parse(project, force_parse)
        apply_mapping(project, timeframes)

    analyze(projects, timeframes, entropy_alpha)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--ledgers',
        nargs="*",
        type=str.lower,
        default=PROJECTS,
        choices=[ledger for ledger in PROJECTS],
        help='The ledgers that will be analyzed.'
    )
    parser.add_argument(
        '--timeframe',
        nargs="?",
        type=valid_date,
        default=None,
        help='The timeframe that will be analyzed.'
    )
    parser.add_argument(
        '--force-parse',
        action='store_true',
        help='Flag to specify whether to parse the raw data, regardless if the parsed data file exists.'
    )
    parser.add_argument(
        '--entropy-alpha',
        nargs="?",
        type=int,
        default=1,
        help='The alpha parameter for entropy computation. Default Shannon entropy. Examples: -1: min, 0: Hartley, '
             '1: Shannon, 2: collision.'
    )
    args = parser.parse_args()

    projects = args.ledgers

    timeframe = args.timeframe
    if timeframe:
        timeframes = [timeframe]
    else:
        timeframes = []
        for year in range(START_YEAR, END_YEAR):
            for month in range(1, 13):
                timeframes.append(f'{year}-{str(month).zfill(2)}')

    main(projects, timeframes, args.force_parse, args.entropy_alpha)
