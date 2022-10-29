import datetime
from django.db.models import F, Sum
from dj_app.models import Company, Transaction
from dj_app.utils import CustomAPIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class SplitShareAPIView(APIView):

    def post(self, request, company_slug):
        current_fv = request.data.get('current_fv')
        new_fv = request.data.get('new_fv')

        try:
            assert current_fv and type(current_fv) == int, \
                "'current_fv' is required and should be an integer."

            assert new_fv and type(new_fv) == int, \
                "'new_fv' is required and should be an integer."

            company = Company.objects.get(slug=company_slug)
            factor = current_fv / new_fv

            total_shares_bought = company.transactions.\
                filter(txn_type=Transaction.BUY).\
                aggregate(total_qty=Sum('qty')).get('total_qty')

            total_shares_sold = company.transactions.\
                filter(txn_type=Transaction.SELL).\
                aggregate(total_qty=Sum('qty')).get('total_qty')

            total_shares_held = total_shares_bought - total_shares_sold
            total_shares_post_split = factor * total_shares_held

            params = {
                'company': company,
                'qty': total_shares_post_split,
                'txn_type': Transaction.SPLIT,
                'txn_date': datetime.datetime.now()
            }

            Transaction.objects.create(**params)

            return Response('ok')
        except Company.DoesNotExist:
            raise CustomAPIException(
                'Company does not exist.', status.HTTP_404_NOT_FOUND
            )
        except AssertionError as e:
            raise CustomAPIException(e, status.HTTP_400_BAD_REQUEST)
        except BaseException:
            raise CustomAPIException()


# class SellSharesAPIView(APIView):

#     def validate(self, company_slug):
#         # check if company exists
#         company = Company.objects.filter(slug=company_slug).first()
#         assert company, 'Company does not exist.'

#         # get shares to sell from payload
#         shares_to_sell = self.request.data.get('qty')

#         # run validations on shares_to_sell
#         assert type(shares_to_sell) == int, \
#             "'shares_to_sell' is required and should be an integer."

#         assert shares_to_sell, "'shares_to_sell' should be >= 1."

#         # get total shares held
#         total_shares_held = company.transactions.\
#             aggregate(Sum('qty')).get('qty__sum') or 0

#         # check if user has sufficient shares to sell
#         assert shares_to_sell <= total_shares_held, \
#             f"Insufficient shares to sell. Available: {total_shares_held} shares."

#     def process_sell_order(self, company_slug):
#         # get txns
#         # since we have validated the data, we don't need to check if company exists here
#         txns = Transaction.objects.select_related('company').\
#             filter(company__slug=company_slug).order_by('txn_date')

#         # get qty of shares to be sold
#         qty = self.request.data.get('qty')

#         with transaction.atomic():
#             for txn in txns:
#                 if qty < txn.qty:
#                     txn.qty -= qty
#                     qty = 0
#                     txn.save()
#                 else:
#                     qty -= txn.qty
#                     txn.delete()

#                 if qty == 0:
#                     break

#     def patch(self, request, company_slug):
#         try:
#             # run basic validations
#             self.validate(company_slug)

#             # process sell order
#             self.process_sell_order(company_slug)

#             return Response('ok')
#         except AssertionError as e:
#             raise CustomAPIException(e, status.HTTP_400_BAD_REQUEST)
#         except Exception:
#             raise CustomAPIException()


class HoldingDetailsAPIView(APIView):

    def get_holding_details(self, company):
        total_shares_sold = company.transactions.\
            filter(txn_type=Transaction.SELL).\
            aggregate(total_qty=Sum("qty")).get('total_qty') or 0

        value = total_shares_sold * -1

        txns = company.transactions.filter(txn_type=Transaction.BUY).\
            order_by('txn_date')

        amt_invested = 0

        for txn in txns:
            value += txn.qty
            if value > 0:
                amt_invested += min(txn.qty, value) * txn.rate

        # check if there is a split
        split_record = company.transactions.\
            filter(txn_type=Transaction.SPLIT).\
            order_by('-txn_date').first()

        # update qty if there is a split
        if split_record:
            value = split_record.qty

        data = {
            'company_name': company.name,
            'qty': value,
            'amount_invested': amt_invested,
            'avg_buy_price': amt_invested / value
        }

        return data

    def get(self, request, company_slug):
        try:
            company = Company.objects.get(slug=company_slug)

            cmp = float(self.request.query_params.get('cmp'))

            resp = self.get_holding_details(company)
            resp['cmp'] = cmp
            resp['current_value'] = cmp * resp['qty']

            return Response(resp)
        except Company.DoesNotExist:
            raise CustomAPIException('Company does not exist.',
                                     status.HTTP_400_BAD_REQUEST)
        except ValueError:
            raise CustomAPIException('CMP should be an integer or float.',
                                     status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if isinstance(e, CustomAPIException):
                raise e
            raise CustomAPIException()
