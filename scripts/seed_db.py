"""
    Script to delete all data from database and populate it with dummy data. 
"""

from decimal import Decimal
from dj_app.models import Company, Transaction

COMPANY_NAME = "Axis Bank"
COMPANY_SLUG = "axis-bank"

TRANSACTIONS = [
    {'txn_date': '2020-11-25',  'qty': 10,
        'rate': Decimal(98), 'total': Decimal(980)},
    {'txn_date': '2020-11-26',  'qty': 20,
        'rate': Decimal(100), 'total': Decimal(2000)},
    {'txn_date': '2020-11-27',  'qty': 20,
        'rate': Decimal(105), 'total': Decimal(2100)},
    {'txn_date': '2020-11-28', 'qty': 30,
        'rate': Decimal(110), 'total': Decimal(3300)},
]


def truncate_db():
    Company.objects.all().delete()
    Transaction.objects.all().delete()


def seed_db():
    payload = {
        'name': COMPANY_NAME,
        'slug': COMPANY_SLUG
    }

    company = Company.objects.create(**payload)

    txn_objs = []

    for txn in TRANSACTIONS:
        txn['company'] = company
        obj = Transaction(**txn)
        txn_objs.append(obj)

    Transaction.objects.bulk_create(txn_objs)


def run():
    truncate_db()
    seed_db()
