from .multi import MultiCart
from .utils.utils import MappedDict, Wrapper
from django.conf import settings

class SingleCart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = MappedDict(self.session.get(settings.CART_SESSION_ID, {}))

    @staticmethod
    def merge(dict1:dict, dict2:dict):
        for i in dict2.keys():
            dict1[i] = dict2[i]
        return dict1

    def all(self, ):
        return self.cart.values()

    def decrease_from(self, product_id, product, quantity=1):
        assert quantity > 0, "Please use a positive value or instead use add_to"
        return self.add_to(product_id, product, -quantity, False)

    def clear_product(self, product_id):
        if self.cart.keys().__contains__(product_id):
            del self.cart[product_id]
        self.save()
        return self

    def clear(self,):
        self.cart = MappedDict()
        self.save()
        return self

    def get_product(self, product_id, default=None):
        return self.cart.get(product_id, default)

    def get(self, ):
        return self.session[settings.CART_SESSION_ID]

    def __str__(self, ):
        return str(self.session[settings.CART_SESSION_ID])

    def find(self, product_id):
        def lookup(target):
            for p_id in target.keys():
                if p_id == product_id:
                    return target[p_id]
            return None
        return lookup(self.cart)

    def find_by(self, key, value):
        def lookup(target):
            for p_id in target.keys():
                if target[p_id].keys().__contains__(key) and target[p_id][key] == value:
                    return target[p_id]
        return lookup(self.cart)

    def add(self, product, quantity = 1, custom_product_id=None):
        last_index = custom_product_id or int(self.cart.get_last_key() or -1) + 1
        self.cart[last_index] = Wrapper(product)
        self.cart[last_index]["quantity"] = quantity
        self.save()
        return self

    def add_to(self, product_id, product, quantity=1, secure=True):
        assert not secure or quantity > 0, "Please ensure that you are using a quantity higher than 0" 
        if not self.cart.keys().__contains__(str(product_id)):
            return self.add(product, quantity, product_id)
        MultiCart.merge(self.cart[product_id], Wrapper(product))
        self.cart[product_id]["quantity"] =  self.cart[product_id]["quantity"] + quantity
        if self.cart[product_id]["quantity"] == 0:
            del self.cart[product_id]
        self.save()
        return self

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
