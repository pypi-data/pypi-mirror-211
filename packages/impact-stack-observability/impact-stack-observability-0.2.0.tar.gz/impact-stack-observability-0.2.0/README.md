# Observability for Impact Stack

A package providing observability features for Flask apps.

## Health checks

The `Health` Flask extension provides health checks via an HTTP API.

The list of checks is extendable per app.

### How it works

When called the requested checks run and return `True` or `False`. When *all*
checks return `True` the service/app is considered healthy (i.e. in the
`running` state), otherwise it is considered to be in a `degraded` state.

Checks are expected to be a Python callable, which takes no arguments and
returns a boolean.

### Usage

Create an implementation module, e.g in a `health.py` file:

```python
"""Instantiate and configure checks."""

from impact_stack.observability import health as health_

health = health_.Health()


health.register_check("true", health_.checks.check_true, add_to_defaults=False)


@health.register_check("foo", add_to_defaults=False)
def check_foo():
    """Check for availability of foo."""
    return True
```

In `app.py`:

```python
import flask

from . import health

app = flask.Flask(__name__)
health.health.init_app(app)
```

No configuration is read from `app.config`. You are supposed to configure and
optionally extend the Health extension in the implementation module.

### Checking the liveliness of the app

You can do a simple liveliness check at `/health/ping` (default), which will
just return a `200 OK` text response.

### Checking the service health

A more comprehensive health check is available at `/health/` (default).
This returns a JSON response with following structure (prettyfied):

```javascript
{
  "health": "running",
  "available_checks": [
    "true",
    "foo"
  ],
  "checks": {
    "foo": true
  }
}
```

The `health` field can be of:

- `running`: All requested checks returned `true`
- `degraded`: At least one of the checks returned `false`

Specific checks can be requested with the `checks` parameter:

- `/health/?checks=_defaults`: Run all the checks registered as defaults, same
  as omitting the `checks` parameter alltogether
- `/health/?checks=true,foo`: Run the listed checks

Headers to prevent caching of the health responses are set.

### Provided checks

Some generic checks are providing in this module.

#### `check_true` and `check_false`

Dummy checks which return just `true` resp. `false`

#### `check_db`

(Requires `Flask-SQLAlchemy`.)

Checks if the DB (using the default SQLAlchemy engine) is available by trying a `SELECT 1`

#### `base_check_api_liveliness`

(Needs instantiation.)

Base check for checking the liveliness of an (external) HTTP API.

Example usage:

```python
import functools

from impact_stack.observability import health as health

check_example = functools.partial(
    health_.checks.base_check_api_liveliness,
    "GET",
    "https://api.example.com/v1/health/ping",
    200,  # expected response status code
    2.0,  # timeout
)
health.register_check("example", check_example)
```

### Authorization

A simple mechanism to prevent unrestricted calls to the `/health/` endpoint is
using a shared secret in the HTTP calls.

Set the required config variable `HEALTH_URL_SECRET` to a (random) string and
use the GET param `auth` in calls to the endpoint.
Returns `401` if the secret does not match.
Raises a `RuntimeError` if not set.

If the `HEALTH_URL_SECRET` is set to `None`, checking the secret is disabled.
