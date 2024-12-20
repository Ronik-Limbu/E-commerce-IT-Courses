from django.db.models import Q
from .models import Course

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart_list = self.session.get('cart', [])
        self.item_list = [Course.objects.get(id=course_id) for course_id in self.cart_list]

    def add(self, course_id):
        if course_id not in self.cart_list:
            self.cart_list.append(course_id)
            self.session['cart'] = self.cart_list
            self.item_list = [Course.objects.get(id=course_id) for course_id in self.cart_list]

    def remove(self, course_id):
        if course_id in self.cart_list:
            self.cart_list.remove(course_id)
            self.session['cart'] = self.cart_list
            self.item_list = [Course.objects.get(id=course_id) for course_id in self.cart_list]

    def clear(self):
        self.session['cart'] = []
        self.cart_list = []
        self.item_list = []

    def get_total_price(self):
        return sum(Course.objects.get(id=course_id).price for course_id in self.cart_list)