"""
    Script to delete all data from database and populate it with dummy data. 
"""

from dj_app.models import Company, Transaction
from decimal import Decimal


COMPANY_NAME = "APL Apollo"
COMPANY_SLUG = "apl-apollo"


TRANSACTIONS = [
    {'txn_date': '2020-11-21',  'qty': 10,
     'rate': Decimal(1389.55), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-22',  'qty': 3,
     'rate': Decimal(1531.58), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-23',  'qty': 13,
     'rate': Decimal(1376.2), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-24', 'qty': 10,
     'rate': Decimal(1394.12), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-25', 'qty': 10,
     'rate': Decimal(1383.49), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-26', 'qty': 4,
     'rate': Decimal(1903.68), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-27', 'qty': 22,
     'rate': Decimal(1600.04), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-28', 'qty': 37,
     'rate': Decimal(1702.58), "txn_type": Transaction.SELL},
    {'txn_date': '2020-11-29', 'qty': 22,
     'rate': Decimal(1813.93), "txn_type": Transaction.BUY},
    {'txn_date': '2020-11-30', 'qty': 7,
     'rate': Decimal(1907.71), "txn_type": Transaction.BUY},
    {'txn_date': '2020-12-1', 'qty': 32,
     'rate': Decimal(2472.56), "txn_type": Transaction.SELL},
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
        txn['total'] = txn['rate'] * txn['qty']
        obj = Transaction(**txn)
        txn_objs.append(obj)

    Transaction.objects.bulk_create(txn_objs)

    print('Database seeded successfully.')


def run():
    truncate_db()
    seed_db()
