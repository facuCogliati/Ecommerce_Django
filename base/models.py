
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
		user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
		name = models.CharField(max_length=200, null=True)
		email = models.EmailField(unique=True)

		def __str__(self):
			return str(self.name)

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	image = models.ImageField(null=True, blank=True, default="placeholder.png")

	def __str__(self):
		return self.name
    

class Order(models.Model):
	client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	
	def __str__(self):

		return str(self.id)


	@property
	def total_cart(self):
		orderitems = self.orderitems_set.all()
		total = sum([item.total_price for item in orderitems])
		return total 

	@property
	def total_cart_items(self):
		orderitems = self.orderitems_set.all()
		total = sum([item.quantify for item in orderitems])
		return total  
		

class orderItems(models.Model):
		product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
		order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
		quantify = models.PositiveIntegerField(default= 0, blank= True, null=True)
		date_added = models.DateTimeField(auto_now_add=True)

		def __str__(self):
			return f' "{self.product}" para la orden {self.order}'

		@property
		def total_price(self):
			total = self.product.price * self.quantify
			return total


class ClientAddres(models.Model):
	client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


    
   