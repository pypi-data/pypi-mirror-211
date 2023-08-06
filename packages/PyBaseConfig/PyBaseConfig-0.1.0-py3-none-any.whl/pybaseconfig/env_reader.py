import os

from typing import Type, Any


class BaseException(Exception):
    pass


class MissingRequiredEnvironmentVariables(BaseException):
    """Exception raised when a required key, values not found in the environment variables."""
    def __init__(self, key):
        self.message = f"Required Key: '{key}' is not set in the enviroment variables "
        super().__init__(self.message)


class TypeConversionException(BaseException):
    """Exception raised when there's a failure in converting a value."""
    def __init__(self, value, conversion_error):
        self.message = f"Failed to convert setting '{value}' due to error: {conversion_error}"
        super().__init__(self.message)


class TypeConverter:
    @staticmethod
    def convert(value:str, to_type:Type) -> Any:
        """
        Converts a string value to the specified type.

        Parameters
        ----------
        value : str
            The value to be converted.
        
        to_type : Type
            The type to convert the value to.

        Raises
        ------
        TypeConversionException
            If conversion of the value to the specified type fails.

        Returns
        -------
        Any
            The converted value.
        """
        try:
            return to_type(value)
        except TypeError as e:
            raise TypeConversionException(value, conversion_error=e)


class BaseSettings:
    """
    Base class for settings. On subclass initialization, environment variables are read based on subclass attributes.
    
    Examples
    --------
    >>> class Config(BaseSettings):
    ...     email: str
    ...     password: str
    ...     server: str
    ...     port: int
    ...
    >>> config = Config()
    ... print(config.email)  # assuming EMAIL environment variable is set
    'your-email@example.com'
    
    Raises
    ------
    MissingRequiredEnvironmentVariables
    If a required environment variable (based on subclass attributes) is not found.
    
    """
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for key, value in cls.__annotations__.items():
            env_value = os.environ.get(key)
            if env_value is None:
                raise MissingRequiredEnvironmentVariables(key=key)
            setattr(cls, key, TypeConverter.convert(value=env_value, to_type=value))
