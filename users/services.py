import stripe
from django.conf import settings

stripe.api_key = settings.STRIP_API_KEY


def create_product(product):
    """Функция создания продукта в Stripe"""

    title_product = f'{product.paid_course}' if product.paid_course else f'{product.paid_lesson}'
    stripe_product = stripe.Product.create(name=f'{title_product}')
    return stripe_product['id']


def create_price(product, id_product):
    """Create a new price for a given amount"""

    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=product.amount * 100,
        product=id_product,
    )
    return stripe_price['id']


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
