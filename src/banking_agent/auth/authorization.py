from fastapi import HTTPException, status

# Temporary authorization store for the project.
# Replace this later with a database / entitlement service.
USER_ACCOUNTS: dict[str, set[str]] = {
    "6065a318-4a9c-4467-992c-c82b760322e3": {
        "ACC-10001",
        "ACC-10004",
    },
}


def authorize_account_access(
    user_id: str,
    account_id: str,
) -> None:
    allowed_accounts = USER_ACCOUNTS.get(user_id, set())

    if account_id not in allowed_accounts:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this account",
        )
