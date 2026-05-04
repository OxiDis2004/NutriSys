from fastapi import APIRouter, Depends

from src.dependencies import ServiceContainer, get_services
from src.models.dto.user_dto import UserDTO
from src.models.dto.user_info_dto import UserInfoDTO

router = APIRouter(prefix="/api/user")


@router.post("/login", response_model=UserDTO)
async def login(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Authenticate an existing user.

    Args:
        user (UserDTO): User login data.
        services (ServiceContainer): Application service container.

    Returns:
        UserDTO: User data with resolved identifier and language.
    """
    return services.user_service.login(user)


@router.put("/register", response_model=UserDTO)
async def register(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Register a new user.

    Args:
        user (UserDTO): User registration data.
        services (ServiceContainer): Application service container.

    Returns:
        UserDTO: Created user data.
    """
    return services.user_service.register(user)


@router.put("/change_language", response_model=UserDTO)
async def change_language(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Update the user's interface language.

    Args:
        user (UserDTO): User data containing the selected language.
        services (ServiceContainer): Application service container.

    Returns:
        Response: HTTP response with accepted status.
    """
    return services.user_service.update_language(user)


@router.post("/get_info", response_model=UserInfoDTO)
async def get_info(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Return detailed user profile information.

    Args:
        user (UserDTO): User identifier data.
        services (ServiceContainer): Application service container.

    Returns:
        UserInfoDTO: User profile information.
    """
    return services.user_service.get_information(user)


@router.put("/update_info")
async def update_info(
        user: UserInfoDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Update user profile information.

    Args:
        user (UserInfoDTO): New user profile data.
        services (ServiceContainer): Application service container.

    Returns:
        Response: HTTP response with accepted status.
    """
    return services.user_service.update_information(user)


@router.post("/calculate_bmr")
async def calculate_bmr(
        user: UserDTO,
        services: ServiceContainer = Depends(get_services),  # noqa: B008
):
    """Calculate the user's daily calorie norm.

    Args:
       user (UserDTO): User identifier data.
       services (ServiceContainer): Application service container.

    Returns:
       dict[str, int]: Dictionary containing the calculated BMR value.
    """
    return services.user_service.calculate_bmr(user)
