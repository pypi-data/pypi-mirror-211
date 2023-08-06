from personnummer import personnummer
from personnummer.personnummer import PersonnummerException


def validate_ssn(ssn, country="SE", fail_as_none=False):
    """Validates SSN and normalizes it.

    Supports
        - SE, including coordination numbers

    Args:
        ssn (str): SSN to validate.
        country (str): Country code, ISO 3166-1 alpha-2.
            default: "SE"

    Returns:
        str or None: Normalized SSN.
    """
    if country == "SE":
        try:
            pn = personnummer.parse(ssn)
            if pn.valid():
                return pn.format(long_format=True)
        except PersonnummerException as e:
            if fail_as_none:
                return None
            else:
                raise ValueError(f"Invalid SSN: {ssn}") from e
    else:
        raise ValueError(f"Unsupported country: {country}")
