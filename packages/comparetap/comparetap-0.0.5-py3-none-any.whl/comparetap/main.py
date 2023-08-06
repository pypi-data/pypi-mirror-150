import datetime
import logging
import textwrap

import dateutil.parser
import humanize
import pytz


class EpochParser:
    @classmethod
    def parse(cls, timestamp: str):
        epochtime = float(timestamp)
        logging.warning(f"assuming {epochtime} is UTC")
        return datetime.datetime.fromtimestamp(epochtime).astimezone(pytz.utc)


class DateStampParser:
    @classmethod
    def parse(cls, timestamp: str):
        return dateutil.parser.parse(timestamp)


def main(args):
    tz = pytz.timezone("US/Pacific")
    logging.debug(args.timestamp)

    ts = " ".join(args.timestamp)
    epoch = None
    try:
        epoch = float(ts)
    except ValueError:
        ...

    logging.debug(f"{ts=}, {type(ts)=}, {epoch=}")

    dt = (
        EpochParser.parse(ts) if isinstance(epoch, float) else DateStampParser.parse(ts)
    )

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
