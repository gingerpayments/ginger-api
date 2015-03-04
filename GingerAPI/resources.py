import decimal
import isodate
import re
import endpoints

from exceptions import *


class AttrDict(dict):
    def load(self, payload):
        if not isinstance(payload, dict):
            raise GingerAPIError('Error loading attributed dict %s' % self)

        for key, value in payload.iteritems():
            # manipulate possible iso-datetime
            test = re.compile('(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z))')
            if isinstance(value, basestring) and test.match(value):
                value = isodate.parse_datetime(value)

            # manipulate possible iso-date
            test = re.compile('(\d{4}-[01]\d-[0-3]\d)')
            if isinstance(value, basestring) and test.match(value):
                value = isodate.parse_date(value)

            setattr(self, key, value)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        self.pop(attr, None)

    def __init__(self, result={}):
        self.load(result)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id if self.id else '')


class Merchant(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        result['phone_numbers'] = result.get('phone_numbers', [])
        self.load(result)

        # define endpoint structure
        self.balances = endpoints.Balances(gapi, self.id)
        self.invoices = endpoints.Invoices(gapi, self.id)
        self.projects = endpoints.Projects(gapi, self.id)
        self.roles = endpoints.Roles(gapi, self.id)
        self.users = endpoints.Users(gapi, self.id)


class IdealIssuer(AttrDict):
    pass


class Order(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        result['amount'] = decimal.Decimal(result['amount']) / decimal.Decimal(100)
        self.load(result)

        # for consistency we remove the property as it is also an endpoint
        del self.transactions

        # define endpoint structure
        self.transactions = endpoints.Transactions(gapi, self.id)
        self.logs = endpoints.Logs(gapi, self.id)
        self.refunds = endpoints.Refunds(gapi, self.id)


class SearchedOrder(AttrDict):
    def __init__(self, result):
        # fill properties
        result['amount'] = decimal.Decimal(result['amount']) / decimal.Decimal(100)
        self.load(result)


class Partner(AttrDict):
    def __init__(self, gapi, result):
        # fill properties
        self.load(result)

        # define endpoint structure
        self.merchants = endpoints.PartnerMerchants(gapi, self.id)


class User(AttrDict):
    pass


class Invoice(AttrDict):
    def __init__(self, result):
        # fill properties
        for i, item in enumerate(result['items']):
            result['items'][i]['amount'] = decimal.Decimal(result['items'][i]['amount']) / decimal.Decimal(100)
            result['items'][i]['total'] = decimal.Decimal(result['items'][i]['total']) / decimal.Decimal(100)
            result['items'][i]['vat'] = decimal.Decimal(result['items'][i]['vat']) / decimal.Decimal(100)

        result['total'] = decimal.Decimal(result['total']) / decimal.Decimal(100)
        result['total_incl_vat'] = decimal.Decimal(result['total_incl_vat']) / decimal.Decimal(100)
        result['vat'] = decimal.Decimal(result['vat']) / decimal.Decimal(100)
        self.load(result)

    @property
    def lines(self):
        """
        .items in a python builin method, so we use lines.
        """
        return self.get('items')


class Token(AttrDict):
    pass


class Project(AttrDict):
    pass


class Transaction(AttrDict):
    def __init__(self, result):
        # fill properties
        result['amount'] = decimal.Decimal(result['amount']) / decimal.Decimal(100)
        self.load(result)


class Log(AttrDict):
    pass


class Refund(AttrDict):
    pass


class Balance(AttrDict):
    pass


class Role(AttrDict):
    pass
