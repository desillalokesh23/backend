from master.constants.tenant import REQUIRED_PROFILE_FIELDS


def check_profile_completion(tenant) -> tuple[bool, list[str]]:
    missing = []
    for field in REQUIRED_PROFILE_FIELDS:
        value = getattr(tenant, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    completed = len(missing) == 0
    if tenant.profile_completed != completed:
        tenant.profile_completed = completed
        tenant.save(update_fields=['profile_completed', 'updated_at'])
    return completed, missing
