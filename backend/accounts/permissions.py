from rest_framework.exceptions import PermissionDenied
from .models import StoreMembership

#valiedate the user has access to the store
def get_active_store(user, store_id):
    membership = StoreMembership.objects.filter(user=user, store_id=store_id).first()
    if not membership:
        raise PermissionDenied("You do not have access to this store.")
    return membership.store, membership

#check if user has the required role for the store
def require_role(user, store_id, allowed_roles):
   
    store, membership = get_active_store(user, store_id)
    if membership.role not in allowed_roles:
        raise PermissionDenied("Your role does not permit this action.")
    return store, membership