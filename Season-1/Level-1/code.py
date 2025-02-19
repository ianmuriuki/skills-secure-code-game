# code.py
from collections import namedtuple
from decimal import Decimal, getcontext

# Increase precision if needed
getcontext().prec = 28

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

def validorder(order: Order):
    """
    Checks whether an order is valid based on:
    1) Item type ('payment' or 'product')
    2) Total cost limit
    3) Net balance (must be 0 for "Full payment received")
    """

    # Define a maximum allowed total for product costs
    MAX_ORDER_AMOUNT = Decimal('999999')

    net = Decimal('0')
    total_product_cost = Decimal('0')

    for item in order.items:
        # Convert the numeric fields to Decimal
        amount = Decimal(str(item.amount))
        quantity = Decimal(str(item.quantity))

        if item.type == 'payment':
            # Add to net
            net += amount

        elif item.type == 'product':
            # Calculate cost of these items
            cost = amount * quantity

            # Check if adding this cost goes beyond the max allowed
            if total_product_cost + cost > MAX_ORDER_AMOUNT:
                return "Total amount payable for an order exceeded"

            # Update total product cost and net
            total_product_cost += cost
            net -= cost

        else:
            # Invalid item type
            return "Invalid item type: %s" % item.type

    # After processing all items, check net
    if net != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    else:
        return "Order ID: %s - Full payment received!" % order.id
