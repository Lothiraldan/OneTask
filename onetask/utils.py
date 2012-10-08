import datetime


def format_timestamp(ts, date_format="%Y-%m-%d"):
    "Formats a timestamp to a human readable date."
    return datetime.datetime.fromtimestamp(ts).strftime(date_format)


def format_duration(seconds):
    "Formats a duration expressed in seconds to a human readable string."
    if seconds < 60:
        return "%d seconds" % seconds
    if seconds < 120:
        return "about a minute"
    if seconds < 3600:
        return "%d minutes" % (seconds / 60)
    if seconds < 7200:
        return "about one hour"
    if seconds < 86400:
        return "%d hours" % (seconds / 3600)
    days = seconds / 86400
    if days <= 1:
        return "about one day"
    if days < 7:
        return "%d days" % days
    if days < 31:
        return "%d weeks" % (days / 7)
    if days < 365:
        return "%d months" % (days / 30)
    return "%d years" % (days / 365)


def pprinttable(rows):
    "Returns an ascii table from data."
    lines = []
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]],
                key=lambda x: len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(['-' * n for n in lens])
        lines.append(separator)
        lines.append(hpattern % tuple(headers))
        lines.append(separator)
        for line in rows:
            lines.append(pattern % tuple(line))
        lines.append(separator)
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields, key=lambda x: len(x)))
        for i in range(len(row)):
            lines.append("%*s = %s" % (hwidth, row._fields[i], row[i]))
    return "\n".join(lines)
