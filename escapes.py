"""Yaml escape parser"""

def interp_escapes(path):
    """Interpolate escaped characters based on their hex value
    when found in the scheme %<hex>"""
    known_escape_vals = {58}
    interped_path = ""
    i = 0
    path_len = len(path)
    while i < path_len:
        if path[i] == "\a":
            # processing a potential replacement character
            hex_chars = path[i + 1 : i + 3]
            try:
                esc_int = int(hex_chars, base=16)
                # valid hex may just be coincidence, ensure
                # value is one of expected escapes
                if esc_int in known_escape_vals:
                    rep_text = chr(esc_int)
                    interped_path = interped_path + rep_text
                    i += 3
                    continue
            except ValueError:
                # processed characters are not valid hex
                # and as such not a valid replacement
                interped_path = interped_path + path[i]
        else:
            interped_path = interped_path + path[i]
        i += 1
    return interped_path


def escape_colons(path):
    """Replaces colon characters with hex representation
    in yaml path arguments so long as the colon is properly escaped
    with respect to yaml syntax (between two single quotes)"""
    # Indicator that we are parsing within the context of a potential escape sequence
    # However, standalone single quotes are not an escape character and they
    # should be ignored here
    escaped_colon_idx = 0
    inside_escape = False
    path_tokens = []
    token = ""
    for current_char in path:
        if current_char == ":":
            path_tokens.append(token)
            token = ""
        elif current_char == "'" and not (token and token[-1] == "\\"):
            if inside_escape:
                token = "\a3a".join(path_tokens[escaped_colon_idx:] + [token])
                path_tokens[escaped_colon_idx:] = ""
                inside_escape = False
            else:
                escaped_colon_idx = len(path_tokens)
                inside_escape = True
            token += current_char
        else:
            token += current_char
    path_tokens.append(token)
    return ":".join(path_tokens)