from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cafe, Booking
from .forms import CustomUserCreationForm, CafeForm, BookingForm
from django.utils import timezone
from django.db.models import Q
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import make_aware, now , localtime , is_aware , timedelta
import json
from .models import Booking, Cafe
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count

# ─────────────── LANDING & AUTH ─────────────── #

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('manager_home') if request.user.is_manager else redirect('user_home')
    return render(request, 'landing.html')

def register_view(request):
    role = request.GET.get('role')
    if role not in ['user', 'manager']:
        return render(request, 'choose_role.html')

    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = (role == 'manager')
            user.save()
            login(request, user)
            return redirect('manager_home' if user.is_manager else 'user_home')
    return render(request, 'register.html', {'form': form, 'role': role})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('manager_home' if user.is_manager else 'user_home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ─────────────── USER VIEWS ─────────────── #

@login_required
def user_home(request):
    if request.user.is_manager:
        return redirect('manager_home')
    return render(request, 'user_home.html')

@login_required
def cafe_list(request):
    cafes = Cafe.objects.all()
    return render(request, 'cafe_list.html', {'cafes': cafes})

# ─────────────── MANAGER VIEWS ─────────────── #

@login_required
def manager_home(request):
    if not request.user.is_manager:
        return redirect('user_home')
    return render(request, 'manager_home.html')

@login_required
def manager_bookings(request):
    if not request.user.is_manager:
        return redirect('user_home')

    # 1. Base queryset
    cafes = Cafe.objects.filter(owner=request.user)
    qs    = Booking.objects.filter(cafe__in=cafes).select_related('user','cafe')

    # 2. Named filters (today / upcoming)
    filter_val = request.GET.get('filter')
    today      = timezone.localdate()
    if filter_val == 'today':
        qs = qs.filter(date=today)
    elif filter_val == 'upcoming':
        qs = qs.filter(date__gt=today)

    # 3. Custom date‐range filters
    date_from = request.GET.get('date_from')  # expected format YYYY-MM-DD
    date_to   = request.GET.get('date_to')
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    # 4. Ordering, counts & summary
    qs = qs.order_by('-date','-time')
    total_count = qs.count()
    date_summary = (
        qs.values('date')
          .annotate(count=Count('id'))
          .order_by('date')
    )

    return render(request, 'manager_bookings.html', {
        'bookings':       qs,
        'current_filter': filter_val,
        'date_from':      date_from,
        'date_to':        date_to,
        'total_count':    total_count,
        'date_summary':   date_summary,
    })



@login_required
def manager_cafes(request):
    if not request.user.is_manager:
        return redirect('user_home')
    cafes = Cafe.objects.filter(owner=request.user)
    return render(request, 'manager_cafes.html', {'cafes': cafes})

@login_required
def add_cafe(request):
    if not request.user.is_manager:
        return redirect('user_home')

    if request.method == 'POST':
        form = CafeForm(request.POST)
        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.owner = request.user
            cafe.save()
            return redirect('manager_cafes')
    else:
        form = CafeForm()

    return render(request, 'add_cafe.html', {'form': form})

@login_required
def edit_cafe(request, cafe_id):
    if not request.user.is_manager:
        return redirect('user_home')

    cafe = get_object_or_404(Cafe, id=cafe_id, owner=request.user)

    if request.method == 'POST':
        form = CafeForm(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            return redirect('manager_cafes')
    else:
        form = CafeForm(instance=cafe)

    return render(request, 'edit_cafe.html', {'form': form})



@login_required
def book_table(request):
    if request.user.is_manager:
        return redirect('manager_home')

    form = BookingForm()
    message = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            dt = timezone.make_aware(
                timezone.datetime.combine(booking.date, booking.time)
            )

            # Check if booking is for a past time
            if dt < timezone.now():
                message = "You cannot book for a past time."

            # Check if user already has a booking at this time
            elif Booking.objects.filter(user=request.user, date=booking.date, time=booking.time).exists():
                message = "You already have a booking at this time."

            # Check if cafe has available tables
            elif booking.cafe.table_count <= 0:
                message = "No tables available at this café for the selected time."

            else:
                # Save the booking and decrease table count
                booking.save()
                booking.cafe.table_count -= 1
                booking.cafe.save()
                return redirect('my_bookings')

    return render(request, 'book_table.html', {'form': form, 'message': message})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'my_bookings.html', {'bookings': bookings})


# @login_required
# def cancel_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)
#     if not booking.is_past():
#         # Restore table count only if the booking was for future
#         booking.cafe.table_count += 1
#         booking.cafe.save()
#         booking.delete()
#     return redirect('my_bookings')
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Build an aware datetime for the booking
    dt = timezone.datetime.combine(booking.date, booking.time)
    if not is_aware(dt):
        dt = make_aware(dt)
    booking_time = localtime(dt)
    current_time = localtime(now())

    # Only allow cancellation if >1 hour ahead
    if booking_time > current_time + timedelta(hours=1):
        booking.cafe.table_count += 1
        booking.cafe.save()
        booking.delete()
        messages.success(request, "Your booking was successfully cancelled.")
    else:
        messages.error(
            request,
            "Sorry — you can only cancel at least 1 hour before your booking time."
        )

    return redirect('my_bookings')

@csrf_exempt
@require_POST
@login_required
def api_book_table(request):
    try:
        data = json.loads(request.body)
        cafe_id = data.get('cafe_id')
        date = data.get('date')
        time = data.get('time')

        cafe = get_object_or_404(Cafe, id=cafe_id)

        if cafe.table_count <= 0:
            return JsonResponse({'success': False, 'message': 'No tables available.'})

        dt = make_aware(timezone.datetime.combine(parse_date(date), parse_time(time)))

        if dt < now():
            return JsonResponse({'success': False, 'message': 'Cannot book for a past time.'})

        if Booking.objects.filter(user=request.user, date=date, time=time).exists():
            return JsonResponse({'success': False, 'message': 'You already have a booking at this time.'})

        Booking.objects.create(
            user=request.user,
            cafe=cafe,
            date=date,
            time=time
        )

        cafe.table_count -= 1
        cafe.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})