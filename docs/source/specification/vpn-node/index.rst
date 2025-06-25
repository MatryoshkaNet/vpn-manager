``vpn-node``
============


Purpose
-------

Handles the delivery of traffic reports and access logs from ``Node`` to the central ``vpn-manager``.

Behavior
--------

- Runs as a separate background service on the node
- Sends:
  - ``TrafficReport``
  - ``AccessLog``
- Does not accept incoming requests
- Uses push model
- If HTTP 401 Unauthorized → agent shuts down

Security
--------

- Authentication via ``Authorization: Bearer <token>`` header
- Agent has no awareness of subscriptions
- All communication is outbound only
