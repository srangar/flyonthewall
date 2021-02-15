from equity_client import EquityClient


def test_equity_client():
    equity_client = EquityClient("AAPL")
    assert equity_client


def test_get_delta():
    equity_client = EquityClient("AAPL")
    assert isinstance(equity_client.get_delta(), float)
