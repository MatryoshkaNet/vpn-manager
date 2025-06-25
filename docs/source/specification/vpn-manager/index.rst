
``vpn-manager``
===============


Purpose
^^^^^^^

Centralized management of users, subscriptions, VPN nodes, and access rules. Provides a REST API for internal administration, data collection, traffic accounting, and sing-box configuration generation.



Models
^^^^^^


``User``
--------

* ``id``: UUIDv7 — unique user identifier
* ``username``: str — login name
* ``password_hash``: str — hashed password
* ``role``: enum(``superuser``, ``operator``) — access level
* A user may belong to one or more groups (``Group``)


``Group``
---------

Assigned to users to apply limits.

Fields:

* ``max_traffic``: int or null (in bytes)
* ``max_speed``: int or null (in bits per second)
* ``traffic_reset_period``: str or null (ISO 8601 duration, e.g. ``P30D``)

``null`` means no restriction.
Limits across multiple groups are aggregated using the **maximum** value per field.


``Subscription``
----------------

Represent an end-user VPN access point.

Fields:

* ``id``: UUIDv7 — public subscription identifier
* ``title``: optional str — display title
* ``description``: optional str — display description
* ``expires_at``: datetime or null — expiration; null = perpetual
* ``max_traffic``: int or null (limits)
* ``max_speed``: int or null (limits)
* ``traffic_reset_period``: ISO 8601 duration or null — usage reset interval
* ``is_suspended``: bool — manually disabled
* ``is_over_limit``: bool — set automatically by system

A subscription can be linked to multiple ``Inbound`` entries.

Subscription Behavior



- If ``is_suspended = true`` → no configuration is generated (HTTP 403 error)
- If ``is_over_limit = true`` → empty or limited config is returned
- If ``traffic_reset_period`` is set → usage is reset automatically


``Node``
--------

Represent physical or virtual VPN servers.

Fields:

- ``id``: UUIDv7
- ``description``: optional str
- ``geo``: optional str
- ``purpose``: optional str
- Associated with one or more ``Inbound`` entries

A node is considered active if statistics are received from it.


``NodeToken``
-------------

Used by the node agent for authentication.

Fields:

- ``id``: UUIDv7
- ``key``: str (32 characters)
- ``revoked_at``: datetime or null — manual revocation

Tokens have no TTL and remain valid until revoked.


``Inbound``
-----------

Represent connection entry points (e.g. sing-box inbounds).

Fields:

- ``id``: UUIDv7
- ``host``: str
- ``port``: int
- ``protocol``: str
- ``network``: str
- ``tls``: bool
- ``geo``: optional str
- ``purpose``: optional str
- ``is_active``: bool — controls inclusion in generated configs
- Linked to one ``Node``

``TrafficReport``
-----------------

Tracks traffic usage per subscription.

Fields:

- ``subscription_id``: UUIDv7
- ``inbound_id``: UUIDv7
- ``node_id``: UUIDv7
- ``bytes_up``: int
- ``bytes_down``: int
- ``timestamp``: datetime (UTC)

``AccessLog``
-------------

Records access to a subscription (no IP address or device data).

Fields:

- ``id``: UUIDv7 — unique access event identifier
- ``timestamp``: datetime (UTC) — connection time
- ``subscription_id``: UUIDv7 — the subscription used
- ``inbound_id``: UUIDv7 — inbound where the connection occurred
- ``node_id``: UUIDv7 — node where the inbound is hosted
- ``bytes_up``: int — uploaded traffic in bytes
- ``bytes_down``: int — downloaded traffic in bytes
- ``auth_token_id``: UUIDv7 or null — token used for reporting, if applicable
- ``note``: optional str — optional debug or system comment

``AuditLog``
------------

Records admin/operator actions.

Fields:

- ``id``: UUIDv7
- ``timestamp``: datetime
- ``actor_id``: UUIDv7
- ``action``: str
- ``target_type``: str
- ``target_id``: UUIDv7
- ``meta``: JSON (optional details)

Viewable only by ``superuser``.

Subscription Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Endpoint**: ``GET /s/{subscription_id}``
- **Format**: sing-box JSON only
- If ``is_suspended`` → HTTP 403 Forbidden
- If ``is_over_limit`` → return stub or empty config
- Uses Jinja2 templating + Pydantic model for config rendering
