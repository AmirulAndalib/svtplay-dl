from math import ceil

QUOTED_ATTRS = {
    "URI",
    "KEYFORMAT",
    "KEYFORMATVERSIONS",
    "ID",
    "CLASS",
    "START-DATE",
    "END-DATE",
    "SCTE35-CMD",
    "SCTE35-OUT",
    "SCTE35-IN",
    "BYTERANGE",
}


def _format_attr_tuple(d):
    parts = []
    for k, v in d.items():
        if k in QUOTED_ATTRS:
            parts.append(f'{k}="{v}"')
        else:
            parts.append(f"{k}={v}")
    return ",".join(parts)


def _format_extinf(value):
    duration = value["duration"]
    title = value.get("title")
    if title is None:
        return f"#EXTINF:{duration}"
    return f"#EXTINF:{duration},{title}"


def _format_tag(tag, value):
    if tag == "EXTINF":
        return _format_extinf(value)
    elif tag == "EXT-X-BYTERANGE":
        return f"#EXT-X-BYTERANGE:{value['n']}@{value['o']}"
    elif tag == "EXT-X-DISCONTINUITY":
        return "#EXT-X-DISCONTINUITY"
    elif tag == "EXT-X-KEY":
        return "#EXT-X-KEY:" + _format_attr_tuple(value)
    elif tag == "EXT-X-MAP":
        d = {k: v for k, v in value.items() if k != "EXT-X-BYTERANGE"}
        return "#EXT-X-MAP:" + _format_attr_tuple(d)
    elif tag == "EXT-X-PROGRAM-DATE-TIME":
        return f"#EXT-X-PROGRAM-DATE-TIME:{value}"
    elif tag == "EXT-X-DATERANGE":
        return "#EXT-X-DATERANGE:" + _format_attr_tuple(value)
    else:
        raise ValueError(f"Unknown media segment tag: {tag}")


def media_segment_to_m3u8(media_segment):
    """Reconstruct m3u8 media playlist text from an M3U8.media_segment list."""
    target_duration = ceil(max(seg["EXTINF"]["duration"] for seg in media_segment if "EXTINF" in seg))

    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:7",
        f"#EXT-X-TARGETDURATION:{target_duration}",
        "#EXT-X-MEDIA-SEQUENCE:0",
        "#EXT-X-PLAYLIST-TYPE:VOD",
    ]

    for seg in media_segment:
        for tag, value in seg.items():
            if tag == "URI":
                continue
            lines.append(_format_tag(tag, value))
        lines.append(seg["URI"])

    lines.append("#EXT-X-ENDLIST")
    return "\n".join(lines) + "\n"


def m3u8_to_file(m3u8, path):
    """Write an M3U8 object's media_segment out as a standalone .m3u8 playlist file."""
    with open(path, "w") as fd:
        fd.write(media_segment_to_m3u8(m3u8.media_segment))
    return path
