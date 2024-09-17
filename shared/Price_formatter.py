# shared/price_formatter.py

def format_price_usd(price: str) -> str:
    """
    Formatea el precio en formato USD.
    Convierte el precio de str a float antes de formatearlo.
    Ejemplo: "55.83" -> "USD 55,83"
    """
    try:
        price_float = float(price)
        return f"USD {price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except ValueError:
        return "Invalid price format"

def format_price_arg(price: str) -> str:
    """
    Formatea el precio en formato ARG.
    Convierte el precio de str a float antes de formatearlo.
    Ejemplo: "5204.00" -> "ARG 5204,00"
    """
    try:
        price_float = float(price)
        return f"ARG {price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except ValueError:
        return "Invalid price format"