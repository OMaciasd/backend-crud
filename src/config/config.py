import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise an error if not found."""
    value = os.getenv(var_name, default)
    if value is None and default is None:
        logger.error(f"Missing environment variable '{var_name}'.")
        raise EnvironmentError(f"Missing environment variable: {var_name}")
    return value


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TF_VAR_postgres_url'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv(
        'DEBUG',
        'False').lower() in ['true', '1']

    @classmethod
    def validate(cls):
        """Validate required environment variables."""
        required_vars = {
            'TF_VAR_postgres_url': cls.SQLALCHEMY_DATABASE_URI
        }

        missing_vars = [
            var for var, value in required_vars.items()
            if not value
        ]

        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            logger.error("Missing environment variables: %s", missing_vars_str)
            raise EnvironmentError(
                "Required environment variables are missing: "
                f"{missing_vars_str}"
            )

        logger.info("All required environment variables are present.")
