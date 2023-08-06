from .utils.wrapper import Wrapper
from .utils.utils import MappedDict
from django.conf import settings

"""
    Most methods use Model as parameter if you give an updated 
    model then the cart will update its values
"""
class MultiCart(object):
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

    def add(self, cart_id, product, quantity = 1, custom_product_id=None):
        if self.cart.get(cart_id, None) is None:
            self.cart[cart_id] = MappedDict()
        last_index = custom_product_id or int(self.cart.get_last_key() or -1) + 1
        print("last_index: ",last_index)
        self.cart[cart_id][last_index] = Wrapper(product)
        self.cart[cart_id][last_index]["quantity"] = quantity
        self.save()
        return self

    def add_to(self, cart_id, product_id, product, quantity=1, secure=True):
        assert not secure or quantity > 0, "Please ensure that you are using a quantity higher than 0" 
        if not self.cart.keys().__contains__(str(cart_id)) or not self.cart[cart_id].keys().__contains__(str(product_id)):
            return self.add(cart_id, product, quantity, product_id)
        MultiCart.merge(self.cart[cart_id][product_id], Wrapper(product))
        self.cart[cart_id][product_id]["quantity"] =  self.cart[cart_id][product_id]["quantity"] + quantity
        if self.cart[cart_id][product_id]["quantity"] == 0:
            del self.cart[cart_id][product_id]
        self.save()
        return self

    def decrease_from(self, cart_id, product_id, product, quantity=1):
        assert quantity > 0, "Please use a positive value or instead use add_to"
        return self.add_to(cart_id, product_id, product, -quantity, False)

    def clear_product(self, cart_id, product_id):
        assert self.cart.keys().__contains__(cart_id), "Cart doesnt exists"
        if self.cart[cart_id].keys().__contains__(product_id):
            del self.cart[cart_id][product_id]
        self.save()
        return self
    def clear_cart(self, cart_id):
        if self.cart.keys().__contains__(cart_id):
            del self.cart[cart_id]
        self.save()
        return self

    def clear(self,):
        self.cart = MappedDict({})
        self.save()
        return self

    def get_cart(self, cart_id):
        return self.cart.get(cart_id, None)

    def get_product(self, cart_id, product_id, default=None):
        return self.cart.get(cart_id, {}).get(product_id, default)

    def get(self, ):
        return self.cart

    def __str__(self, ):
        return str(self.session[settings.CART_SESSION_ID])

    def find(self, product_id):
        def lookup(target):
            for p_id in target.keys():
                if p_id == product_id:
                    return target[p_id]
        for cart_id in self.cart.keys():
            res = lookup(self.cart[cart_id])
            if res:
                return res
        return None

    def find_by(self, key, value):
        def lookup(target):
            for p_id in target.keys():
                if target[p_id].keys().__contains__(key) and target[p_id][key] == value:
                    return target[p_id]
        for cart_id in self.cart.keys():
            res = lookup(self.cart[cart_id])
            if res:
                return res
        return None

    def save(self, ):
        # upload changes to the session...
        self.session[settings.CART_SESSION_ID] = self.cart
        #self.session.modified = True

