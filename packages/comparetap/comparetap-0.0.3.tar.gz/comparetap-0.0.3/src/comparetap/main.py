import argparse
import datetime
import textwrap

import dateutil.parser
import humanize
import pytz


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("timestamp")
    args = parser.parse_args()

    tz = pytz.timezone("US/Pacific")

    dt = dateutil.parser.parse(args.timestamp)
    dt2 = dt.astimezone(tz)

    now = datetime.datetime.now(tz)

    meta = "from now" if now < dt else "ago"

    relative = humanize.naturaldelta(now - dt2)
    out = textwrap.dedent(
        f"""\
    input:     {args.timestamp}
    asiso:     {dt.isoformat()}
    epoch:     {dt.timestamp()}
    converted: {dt}
    mytime:    {dt2}
    relative:  {relative} {meta}\
    """
    )

    print(out)
