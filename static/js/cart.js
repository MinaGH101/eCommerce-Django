var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var size = this.dataset.size
		console.log('productId:', productId, 'Action:', action, 'Size:', size)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action, size)
		}
	})
}

function updateUserOrder(productId, action, size){
	console.log('User is authenticated, sending data...')

		var url = '/shop/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'Size':size})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}




var updateBtns = document.getElementsByClassName('delete-item')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var size = this.dataset.size
		console.log('productId:', productId, 'Action:', action, 'Size', size)
		console.log('USER:', user)

		DeleteItem(productId, action, size)
		
	})
}

function DeleteItem(productId, action, size){
	console.log('User is authenticated, sending data...')

		var url = '/shop/cart/delete_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'Size':size})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}



var DropBtn = document.getElementById("Dropdown")

function SortFunction() {
	DropBtn.classList.toggle("show");
  }

window.onclick = function(event) {
	if (!event.target.matches('.dropbtn')) {
	  var dropdowns = document.getElementsByClassName("dropdown-menu");
	  var i;
	  for (i = 0; i < dropdowns.length; i++) {
		var openDropdown = dropdowns[i];
		if (openDropdown.classList.contains('show')) {
		  openDropdown.classList.remove('show');
		}
	  }
	}
  }
  
  function SortProducts(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/shop/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}




var updateBtns = document.getElementsByClassName('add-to-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		AddFuction(productId, action)
	})
}
  
  function AddFuction(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/shop/add-to-cart/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}




var updateBtns = document.getElementById('discount-apply')

updateBtns.addEventListener('click', function(){
	var cartId = this.dataset.cart
	var action = this.dataset.action
	console.log('cartId:', cartId, 'Action:', action)
	console.log('USER:', user)

	DiscountFuction(cartId, action)
})

  function DiscountFuction(cartId, action){
	console.log('User is authenticated, sending data...')

		var url = '/shop/discount/'
		var value = document.getElementById('code').value

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'cartId':cartId, 'action':action, 'value':value})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}