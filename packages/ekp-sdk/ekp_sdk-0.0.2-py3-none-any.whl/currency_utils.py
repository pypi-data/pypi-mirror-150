from pycoingecko import CoinGeckoAPI


def selected_currency(event):
    """
    Returns selected currency if selected, otherwise None
    """
    if (event is None):
        return None

    if ("state" not in event.keys()):
        return None

    if ("client" not in event["state"].keys()):
        return None

    if ("selectedCurrency" not in event["state"]["client"].keys()):
        return None

    return event["state"]["client"]["selectedCurrency"]


def latest_price(tokenId, fiatId):
    cg = CoinGeckoAPI()

    if tokenId == "usd-coin" and fiatId == "usd":
        return 1

    result = cg.get_price(ids=tokenId, vs_currencies=fiatId)

    return result[tokenId][fiatId]