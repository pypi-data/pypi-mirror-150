import datetime
import logging
import textwrap

import dateutil.parser
import humanize
import pytz


def main(args):
    tz = pytz.timezone("US/Pacific")
    logging.debug(args.timestamp)

    ts = " ".join(args.timestamp)

    dt = dateutil.parser.parse(ts)
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
