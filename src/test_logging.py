from src.logger_config import logger
from src.exceptions import InvalidAmountError

try:
    raise InvalidAmountError(
        "Amount must be greater than zero."
    )

except InvalidAmountError as error:

    logger.error(error)

    print("Error logged successfully.")