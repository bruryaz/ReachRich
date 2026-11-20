from app.core.database import get_client


def get_user_transactions(user_id: str) -> list[dict]:
    client = get_client()
    response = (
        client.table("transactions")
        .select("*, accounts!inner(user_id)")
        .eq("accounts.user_id", user_id)
        .execute()
    )
    return response.data