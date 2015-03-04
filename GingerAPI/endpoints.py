import json
from resources import *
from exceptions import *
from utils import GingerJSONEncoder


class Base(object):

    def __init__(self, gapi):
        self.gapi = gapi

    def __repr__(self):
        return '<%s: I\'m a red-headed endpoint, please use one of my functions >' % self.__class__.__name__

    """
    HTTP functions
    """

    def get(self, resource_id=None):
        if resource_id:
            # get single resource
            result = self.gapi.call_api('GET', self.path + '/' + resource_id, None, None)

            return self.resource(result)

        else:
            # get all resources
            result = self.gapi.call_api('GET', self.path, None, None)

            # replace the results with resource objects
            for i, r in enumerate(result):
                result[i] = self.resource(r)

            return result

    def post(self, data):
        try:
            data = json.dumps(data, cls=GingerJSONEncoder)
        except Exception as e:
            raise GingerAPIError('Error encoding parameters into JSON: "%s"' % e.message)
        result = self.gapi.call_api('POST', self.path, data, None)

        return self.resource(result)

    def put(self, resource_id, resource):
        # strip endpoints on resource
        attr_to_delete = list()
        for key, value in resource.iteritems():
            if isinstance(value, Base):
                attr_to_delete.append(key)
        for key in attr_to_delete:
            delattr(resource, key)

        # perform request
        try:
            data = json.dumps(resource, cls=GingerJSONEncoder)
        except Exception as e:
            raise GingerAPIError('Error encoding parameters into JSON: "%s"' % e.message)
        result = self.gapi.call_api('PUT', self.path + '/' + resource_id, data, None)

        return self.resource(result)

    def delete(self, resource_id):
        result = self.gapi.call_api('DELETE', self.path + '/' + resource_id, None, None)

        return self.resource(result)

    def options(self):
        pass

    """
    HTTP functions natural language
    """

    def add(self, data):
        return self.post(data)

    def all(self):
        return self.get(None)

    def create(self, data):
        return self.post(data)

    def first(self):
        return self.get(None)[0]

    def update(self, resource_id, resource):
        return self.put(resource_id, resource)


    """
    Other functions
    """

    def resource(self, result=None):
        # for each endpoint the resulting resource
        raise NotImplementedError()


class Merchants(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'merchants'

    def resource(self, result):
        return Merchant(self.gapi, result)


class Orders(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'orders'

    def post(self, data):
        # filter amount
        if isinstance(data['amount'], decimal.Decimal):
            data['amount'] = int(round(data['amount'] * 100))

        return super(Orders, self).post(data)

    def resource(self, result):
        return Order(self.gapi, result)


class IdealIssuers(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'ideal/issuers'

    def resource(self, result):
        return IdealIssuer(result)


class Partners(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'partners'

    def resource(self, result):
        return Partner(self.gapi, result)


class PartnerMerchants(Base):
    def __init__(self, gapi, partner_id):
        self.gapi = gapi
        self.path = 'partners/%s/merchants' % partner_id

    def resource(self, result):
        return Merchant(self.gapi, result)


class Users(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/users' % merchant_id

    def resource(self, result):
        return User(result)


class Projects(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/projects' % merchant_id

    def resource(self, result):
        return Project(result)


class Invoices(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/invoices' % merchant_id

    def resource(self, result):
        return Invoice(result)


class Tokens(Base):
    def __init__(self, gapi):
        self.gapi = gapi
        self.path = 'tokens'

    def resource(self, result):
        return Token(result)


class Transactions(Base):
    def __init__(self, gapi, order_id):
        self.gapi = gapi
        self.path = 'orders/%s/transactions' % order_id

    def resource(self, result):
        return Transaction(result)


class Logs(Base):
    def __init__(self, gapi, order_id):
        self.gapi = gapi
        self.path = 'orders/%s/logs' % order_id

    def resource(self, result):
        return Log(result)


class Refunds(Base):
    def __init__(self, gapi, order_id):
        self.gapi = gapi
        self.path = 'orders/%s/refunds' % order_id

    def post(self, data):
        # filter amount
        if isinstance(data['amount'], decimal.Decimal):
            data['amount'] = int(round(data['amount'] * 100))

        return super(Refunds, self).post(data)

    def resource(self, result):
        return Order(self.gapi, result)


class Balances(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'reports/balance/merchants/%s' % merchant_id

    def get(self, resource_id=None):
        # response is not a list, but a dict in a dict. Lets transform
        result = self.gapi.call_api('GET', self.path, None, None)
        result_new = dict()
        for i, r in enumerate(result):
            if 'EUR' in result[r]:
                result_new[r] = decimal.Decimal(result[r]['EUR']) / decimal.Decimal(100)
            else:
                result_new[r] = 0
        return self.resource(result_new)

    def resource(self, result):
        return Balance(result)


class Roles(Base):
    def __init__(self, gapi, merchant_id):
        self.gapi = gapi
        self.path = 'merchants/%s/roles' % merchant_id

    def resource(self, result):
        return Role(result)
