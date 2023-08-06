import os
from urllib.parse import urlparse

try:
    from rasterio.session import AzureSession
except ImportError:
    pass

try:
    from azure.core.utils import parse_connection_string
except ImportError:
    raise ImportError('Azure dependencies not found: try "pip install adlfs" to install them.')


def sync_envvars() -> None:
    """Synchronizes envvars between GDAL and adlfs

    Returns
    -------
    None

    Notes
    -----
    GDAL and adlfs use slightly different environment variables for the same
    credential objects. This takes all the matching pairs and sets them to
    the same value.

    If you do not want max_ard to try to smooth this out, set the envvar
    MAXAR_KEEP_AZURE_ENVVARS to any truthy value
    """

    if os.getenv("MAXAR_KEEP_AZURE_ENVVARS"):
        return

    pairs = [
        ["AZURE_STORAGE_ACCOUNT_NAME", "AZURE_STORAGE_ACCOUNT"],
        ["AZURE_STORAGE_ACCOUNT_KEY", "AZURE_STORAGE_ACCESS_KEY"],
        ["AZURE_STORAGE_SAS_TOKEN", "AZURE_SAS"],  # GDAL < 3.5
    ]
    vals = [os.getenv(A) or os.getenv(B) for A, B in pairs]
    for keys, val in zip(pairs, vals):
        if val:
            for key in keys:
                os.environ[key] = val


def azure_gdal_options() -> dict:
    """Extracts envvars from an Azure connection string until GDAL is updated


    Returns
    -------
    dict
        working GDAL options to use for opening an asset

    Notes
    -----
    GDAL does not understand all connection string formats:
    See  https://github.com/OSGeo/gdal/issues/6870

    This function extracts the SAS-related credentials from
    a connection string and converts them to GDAL options to use

    If you do not want max_ard to try to smooth this out, set the envvar
    MAXAR_KEEP_AZURE_ENVVARS to any truthy value
    """
    if os.getenv("MAXAR_KEEP_AZURE_ENVVARS"):
        return {}

    conn_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    options = {}

    if "SharedAccessSignature" in conn_string:

        # SAS token is the SharedAccessSignature portion
        parsed = parse_connection_string(conn_string)
        sas_token = parsed["sharedaccesssignature"]

        # Account name starts the blob URL: https://ACCOUNT_NAME.blob.core.windows.net
        blob_url = urlparse(parsed["blobendpoint"]).netloc
        account_name = blob_url.split(".")[0]
        options["AZURE_STORAGE_ACCOUNT"] = account_name
        options["AZURE_STORAGE_SAS_TOKEN"] = sas_token
        options["AZURE_STORAGE_CONNECTION_STRING"] = ""
    else:
        options["AZURE_STORAGE_CONNECTION_STRING"] = conn_string

    return options
