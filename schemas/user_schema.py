from voluptuous import Schema, Email, PREVENT_EXTRA

user = Schema(
    {
        "id": int,
        "email": Email,
        "name": str
    },
    extra=PREVENT_EXTRA,
    required=True
)