from ..delivery._data import _data_provider


# ---------------------------------------------------------------------------
#   Raw data parser
# ---------------------------------------------------------------------------


class ErrorParser(_data_provider.Parser):
    def process_failed_response(self, raw_response):
        parsed_data = super().process_failed_response(raw_response)
        status = parsed_data.get("status", {})
        error = status.get("error", {})
        errors = error.get("errors", [])
        error_code = parsed_data.get("error_code")
        error_message = parsed_data.get("error_message", "")
        err_msgs = []
        err_codes = []
        for err in errors:
            reason = err.get("reason")
            if reason:
                err_codes.append(error_code)
                err_msgs.append(f"{error_message}: {reason}")

        if err_msgs and err_codes:
            parsed_data["error_code"] = err_codes
            parsed_data["error_message"] = err_msgs

        return parsed_data


# ---------------------------------------------------------------------------
#   Content data validator
# ---------------------------------------------------------------------------


def get_invalid_universes(universes):
    result = []
    for universe in universes:
        if universe.get("Organization PermID") == "Failed to resolve identifier(s).":
            result.append(universe.get("Instrument"))
    return result


def get_universe_from_raw_response(raw_response):
    universe = raw_response.url.params["universe"]
    universe = universe.split(",")
    return universe


class UniverseContentValidator(_data_provider.ContentValidator):
    def validate(self, data, *args, **kwargs):
        is_valid = super().validate(data)
        if not is_valid:
            return is_valid

        content_data = data.get("content_data", {})
        error = content_data.get("error", {})
        universes = content_data.get("universe", [])
        invalid_universes = get_invalid_universes(universes)

        if error:
            is_valid = False
            data["error_code"] = error.get("code")

            error_message = error.get("description")
            if error_message == "Unable to resolve all requested identifiers.":
                universe = get_universe_from_raw_response(data["raw_response"])
                error_message = f"{error_message} Requested items: {universe}"

            if not error_message:
                error_message = error.get("message")
                errors = error.get("errors")
                if isinstance(errors, list):
                    errors = "\n".join(map(str, errors))
                    error_message = f"{error_message}:\n{errors}"
            data["error_message"] = error_message

        elif invalid_universes:
            data["error_message"] = f"Failed to resolve identifiers {invalid_universes}"

        return is_valid


# ---------------------------------------------------------------------------
#   Provider layer
# ---------------------------------------------------------------------------


class ContentProviderLayer(_data_provider.DataProviderLayer):
    def __init__(self, content_type, **kwargs):
        _data_provider.DataProviderLayer.__init__(
            self,
            data_type=content_type,
            **kwargs,
        )
