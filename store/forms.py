from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import   Profile , CustomUser , Product , CartItem , zero_check


class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'country', )
		
class CustomerRegistrationForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
			model = CustomUser
			fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

	

	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_customer = True
		if commit:
			user.save()
		return user
	

class SellerRegistrationForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_seller = True
		if commit:
			user.save()
		return user
	def __init__(self, *args, **kwargs):
		super(SellerRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class UpdateUserForm(UserChangeForm):
	# Hide Password stuff
	password = None
	# Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
	image = forms.URLField(label="" , required=True ,widget=forms.URLInput(attrs={'class':'form-control','placeholder': 'Image URL'}) )

	name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}), required=True)
	description= forms.CharField(label="", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}), required=False)
	stock = forms.IntegerField(
        label='',
		required=	False,
        widget=forms.NumberInput(attrs={'min': '1', 'max': '100' , 'class':'form-control', 'placeholder':'Stock'})
    )
	price = forms.DecimalField(
		label='',
		required = True,
		max_digits=6,
		decimal_places=2,
		widget=forms.NumberInput(attrs={'step': '0.01', 'class':'form-control', 'placeholder':'Price'})
	)
	

	class Meta:
		model = Product
		fields = ['name', 'description', 'price' , 'category' , 'image' , 'stock']

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		product = super().save(commit=False)
		if self.user:
			product.seller = self.user  # Assume your Product model has a user field
		if commit:
			product.save()
		return product
	
class UpdateProductForm(forms.ModelForm):
	image = forms.URLField(label="" , required=True ,widget=forms.URLInput(attrs={'class':'form-control','placeholder': 'Image URL'}) )
	name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}), required=True)
	description= forms.CharField(label="", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}), required=False)
	stock = forms.IntegerField(
        label='',
		required=	False,
        widget=forms.NumberInput(attrs={'min': '1', 'max': '100' , 'class':'form-control', 'placeholder':'Stock'})
    )
	price = forms.DecimalField(
		label='',
		required = True,
		max_digits=6,
		decimal_places=2,
		widget=forms.NumberInput(attrs={'step': '0.01', 'class':'form-control', 'placeholder':'Price'})
	)

	class Meta:
		model = Product
		fields = ['name', 'description', 'price' , 'category' , 'image' , 'stock']


class CartForm(forms.ModelForm):
	quantity = forms.IntegerField(label=''  , required=True,widget=forms.NumberInput(attrs={'min': '1','placeholder':'Quantity' , 'class':'form-control'}))

	class Meta:
		model = CartItem
		fields = ['quantity']

	def __init__(self, *args, **kwargs):
		self.product = kwargs.pop('product', None)
		self.cart = kwargs.pop('cart', None)
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		cartitem = super().save(commit=False)
		if self.product:
			cartitem.product = self.product
		if self.cart:
			cartitem.cart = self.cart
		if commit:
			cartitem.save()
		return cartitem
	
class OrderForm(forms.Form):
	paymentMethod = forms.ChoiceField(label="",required=True,  widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Payment Method'}) , choices = [
        ('Credit Card', 'Credit Card'),
        ( 'Debit Card' ,'Debit Card' ),
        ('Cash', 'Cash'),
    ])
	address = forms.CharField(label="",required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Delivery Address'}))
	
class RatingForm(forms.Form):
	paymentMethod = forms.ChoiceField(label="Rating",required=True,  widget=forms.Select(attrs={'class':'form-control', 'placeholder':'PRate'}) , choices = [
         ((1, 'Poor') , (2, 'Bad') ,(3, 'OK') ,(4, 'Good') ,(5, 'Amazing')   )
    ])