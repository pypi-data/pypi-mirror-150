from promisio import Promise  # type: ignore
from ramda import if_else  # type: ignore


def handle_response(response):
    content_type_is_application_json = lambda x: "application/json" in x.headers.get(
        "content-type"
    )
    to_json = lambda x: x.json()

    def to_ok(x):
        return {"ok": x.ok, "msg": r.text}

    def check_response_ok_add_status(r):
        if response.ok:
            return r
        else:
            r["status"] = response.status_code
            return r

    def check_500_error(r):
        if response.status_code >= 500:
            return Promise.reject(r)
        else:
            return r

    return (
        Promise.resolve(response)
        .then(if_else(content_type_is_application_json, to_json, to_ok))
        .then(check_response_ok_add_status)
        .then(check_500_error)
    )
