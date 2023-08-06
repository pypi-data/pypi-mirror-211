"""
This library provides an easy way to interact with workspace API.

"""

from googleapiclient.discovery import build
from google.oauth2 import service_account


def create_service(serviceName, version, credentials):
    """
    Create the necessary service to interact with a specific Google Workspace service in a specific version of its API.

    Parameters:
    ----------
        serviceName: Name of the service.
        version: Version of the service.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
        authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.

    """
    service = build(serviceName, version, credentials=credentials)
    return service


def user_exist(credentials, work_email, domain):
    """
    Returns true if the user email exists in the Google Workspce domain specificated, and false if not.

    Parameters:
    ----------
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
        authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
        work_email: Primary email address of the user to search for.
        domain: The domain name where you want to search for.
    """
    service = create_service("admin", "directory_v1", credentials)
    result = (
        service.users()
        .list(query=work_email, orderBy="email", domain=domain)
        .execute()
    )

    if "users" in result and len(result["users"]) > 0:
        exists = True
    else:
        exists = False

    return exists


def update_license(
    currentProductId, currentSkuId, userId, licenseInstance, credentials
):
    """
    Update the Google Workspace license of a user already created.

    Parameters:
    ----------
        currentProductId: The current product's unique identifier. You can check it in this link https://developers.google.com/admin-sdk/licensing/v1/how-tos/products
        currentSkuId: The current product SKU's unique identifier. You can check it in this link https://developers.google.com/admin-sdk/licensing/v1/how-tos/products
        userId: The user's current primary email address.
        licenseInstance: License object instance for the updated.
        Example: {
                    'productId': "Google-Apps",
                    'skuId': "1010020030",
                    'userId': xxxxxx
                    }
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
        authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
    """
    service = create_service("licensing", "v1", credentials)
    service.licenseAssignments().update(
        productId=currentProductId,
        skuId=currentSkuId,
        userId=userId,
        body=licenseInstance,
    ).execute()


def get_workspace_impersonate_credentials_sa(
    credentials_info, scopes, impersonate_mail
):
    """
    Obtain the credentials with the permissions of the service account, in an impersonal way.

    Parameters:
    ----------
        credentials_info: json access key of the service account.
        scopes: Array of the granular permissions that determine what specific resources and operations the service
                account can access.
        impersonate_mail: Email to impersonate the service account.

    Returns:
    -------
    The impersonate credentials with the service account and scope permissions.
    """
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info
    )

    scoped_credentials = credentials.with_scopes(scopes)

    impersonate_credentials = scoped_credentials.with_subject(impersonate_mail)

    return impersonate_credentials
