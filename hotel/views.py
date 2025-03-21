from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import HotelForm, MenuForm
from django.utils.html import strip_tags
from .models import Menu,Hotel, Order
from django.views.generic import ListView, UpdateView, DeleteView


# Create your views here.

def hotel_home(request):
    try:
        hotel = Hotel.objects.get(owner_id=request.user)
        menu = Menu.objects.filter(hotel=hotel.id)
        order = Order.objects.filter(hotel=hotel.id).order_by('-created_at')[:6]
        number_order = Order.objects.filter(hotel=hotel.id)

        revenue = 0
        for order_item in number_order:
            revenue += order_item.cost

        context = {
            'menu': menu,
            'order': order,
            'number_orders': number_order,
            'revenue':revenue
        }
    except Hotel.DoesNotExist:
        return redirect('hotel_not_found')

    return render(request,'hotel/hotel_home.html', context)

def hotel_not_found(request):
    return render(request,'hotel/hotel_not_found.html')

def add_hotel(request):
    form = HotelForm()
    if request.method == 'POST':
        form = HotelForm(request.POST)

        if form.is_valid():
            
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()

            messages.success(request,f"{hotel.name} has been registered successfully. Please wait for admin confirmation.")
            return redirect('home')
        else: 
            error = strip_tags(form.errors)
            messages.error(request,f"Error: {error}")
            
    
    return render(request,'hotel/add_hotel.html',{'form':form})
    
def add_menu(request):
    categories = Menu.Category.choices
    menu_form = MenuForm()

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, request.FILES)

        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            hotel_ins = Hotel.objects.get(owner=request.user)
            menu.hotel = hotel_ins 
            menu.save()

            messages.success(request,f"{menu.title} has been added successfully")
            return redirect('menu-list')
        else:
            error = strip_tags(menu_form.errors)
            messages.error(request,f"Error: {error}")

    context = {
        'categories':categories
    }
    return render(request,'hotel/add_menu.html', context)

class MenuListView(ListView):
    model = Menu
    template_name = 'hotel/menu_list.html'
    context_object_name = 'menus'

    def get_queryset(self):
        hotel_id = Hotel.objects.get(owner = self.request.user)
        return Menu.objects.filter(hotel=hotel_id).order_by('-updated_at')
    
class MenuUpdateView(UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'hotel/menu_update.html'
    
    def form_valid(self, form):
        # Debug uploaded file
        menu_image = self.request.FILES.get('menu_image')
        print(f"Uploaded menu_image: {menu_image}")
        
        # Save form and handle any additional processing
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('menu-list')
    
class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'hotel/menu_delete_confirm.html'
    
    def get_success_url(self):
        return reverse('menu-list')
    
def hotel_orders(request):
    hotel = Hotel.objects.get(owner_id=request.user)
    order = Order.objects.filter(hotel=hotel.id).order_by('-created_at')

    context = {
        'orders' :order
    }

    return render(request, 'hotel/orders_list.html', context)


