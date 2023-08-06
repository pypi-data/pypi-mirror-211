import requests
import json
from caqui.exceptions import WebDriverError
from caqui.helper import get_element

HEADERS = {
    "Accept-Encoding": "identity",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "keep-alive",
}


def __get(url, payload):
    try:
        return requests.request("GET", url, headers=HEADERS, data=payload).json()
    except Exception as error:
        raise WebDriverError("'GET' request failed.") from error


def __post(url, payload):
    try:
        return requests.request("POST", url, headers=HEADERS, data=payload).json()
    except Exception as error:
        raise WebDriverError("'POST' request failed.") from error


def __delete(url):
    try:
        return requests.request("DELETE", url, headers={}, data={}).json()
    except Exception as error:
        raise WebDriverError("'DELETE' request failed.") from error


def find_elements(driver_url, session, locator_type, locator_value):
    try:
        url = f"{driver_url}/session/{session}/elements"
        payload = json.dumps({"using": locator_type, "value": locator_value})
        response = __post(url, payload)
        return [x.get("ELEMENT") for x in response.get("value")]
    except Exception as error:
        raise WebDriverError(
            f"Failed to find elements by '{locator_type}'-'{locator_value}'."
        ) from error


def get_property(driver_url, session, element, property):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/property/{property}"
        response = __get(url, {})
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get value from element.") from error


def go_to_page(driver_url, session, page_url):
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = json.dumps({"url": page_url})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to navigate to '{page_url}'") from error


def close_session(driver_url, session):
    try:
        url = f"{driver_url}/session/{session}"
        __delete(url)
        return True
    except Exception as error:
        raise WebDriverError("Failed to close session.") from error


def get_text(driver_url, session, element):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        response = __get(url, {})
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get text from element.") from error


def send_keys(driver_url, session, element, text):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = json.dumps({"text": text, "value": [*text], "id": element})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to send key '{text}'.") from error


def click(driver_url, session, element):
    try:
        url = f"{driver_url}/session/{session}/element/{element}/click"
        payload = json.dumps({"id": element})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError("Failed to click on element.") from error


def __get_session(response):
    # Firefox response
    value = response.get("value")
    session_id = value.get("sessionId")
    if session_id:
        return session_id

    # Chrome response
    return response.get("sessionId")


def get_session(driver_url, capabilities):
    try:
        url = f"{driver_url}/session"
        data = json.dumps(capabilities)
        response = __post(url, payload=data)
        return __get_session(response)
    except Exception as error:
        raise WebDriverError("Failed to open session.") from error


def find_element(driver_url, session, locator_type, locator_value):
    try:
        url = f"{driver_url}/session/{session}/element"
        payload = json.dumps({"using": locator_type, "value": locator_value})
        response = __post(url, payload)
        return get_element(response)
    except Exception as error:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error
