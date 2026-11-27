from fastapi import APIRouter, Depends
from supabase_auth.types import User

from app.core.auth import get_current_user
from app.services.transactions import get_user_transactions

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
def list_transactions(user: User = Depends(get_current_user)):
    return get_user_transactions(user.id)

# Add Transaction endpoint
# @router.post("")
# def add_transaction(transaction: dict, user: User = Depends(get_current_user)):
