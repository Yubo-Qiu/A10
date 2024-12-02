from project.models import Permission


def has_custom_permission(user, permission_name):
    """
    Check if the user has the specified permission based on their role.
    :param user: User object (from request.user)
    :param permission_name: Name of the permission attribute (e.g., 'can_manage_users')
    :return: Boolean indicating whether the user has the permission
    """
    # Handle cases where the user is not logged in
    if not user.is_authenticated:
        return False  # Visitors (unauthenticated users) have no permissions

    # Get the user's role from their profile
    profile = user.project_profiles.first()  # Assuming each user has one profile
    if not profile:
        return False  # User has no profile, so no permissions

    # Query the Permission model for the user's role
    permission = Permission.objects.filter(role=profile.role).first()
    if not permission:
        return False  # Role not found in the Permission model

    # Check if the permission attribute exists and return its value
    return getattr(permission, permission_name, False)
