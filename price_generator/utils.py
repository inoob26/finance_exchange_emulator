from random import random


def gen_ticker_name(num: int) -> str:
    if num < 10:
        num = f"0{num}"
    return f"ticker_{num}"


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


def check_price(price: int) -> int:
    if price <= 0:
        return 0
    return price
