from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse
from .models import Service, Order, Car
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm, OrderCreateUpdateForm


# Create your views here.

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f'El. paštas negali būti tuščias!')
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {new_email} jau užregistruotas!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)


def index(request):
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status="i").count()
    num_cars = Car.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_services': num_services,
        'num_orders_done': num_orders_done,
        'num_cars': num_cars,
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=6)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {"cars": paged_cars}
    return render(request, template_name="cars.html", context=context)


def car(request, car_id):
    context = {"car": Car.objects.get(pk=car_id)}
    return render(request, template_name="car.html", context=context)


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 5


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.order = self.object
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get('query')
    car_search_results = Car.objects.filter(
        Q(client_name__icontains=query) | Q(client_name__icontains=query) | Q(car_model__make__icontains=query) | Q(
            car_model__model__icontains=query) | Q(license_plate__icontains=query) | Q(vin_code__icontains=query))
    context = {
        "query": query,
        "cars": car_search_results,
    }
    return render(request, template_name="search.html", context=context)


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "user_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    template_name = 'order_form.html'
    success_url = "/autoservice/user_orders/"
    form_class = OrderCreateUpdateForm
    # fields = ['car', 'deadline']

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    template_name = 'order_form.html'
    success_url = "/autoservice/user_orders/"
    form_class = OrderCreateUpdateForm
    # fields = ['car', 'deadline']

    def test_func(self):
        return self.get_object().client == self.request.user

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = 'order_delete.html'
    success_url = "/autoservice/user_orders/"
    context_object_name = "order"

    def test_func(self):
        return self.get_object().client == self.request.user


