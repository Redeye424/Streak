import csv
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from datetime import datetime, date, timedelta
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from .models import Profile, Streak, StreakCompletion
from django.contrib.auth.models import User
import calendar
from django.http import HttpResponse


def user_csv_path(User):
    safe_name = f'user_{User.id}.csv'
    return settings.USER_CSV_DIR / safe_name

def create_user_csv(User):
    settings.USER_CSV_DIR.mkdir(parents=True, exist_ok=True)
    path = user_csv_path(User)
    if not path.exists():
        with path.open('w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['title', 'description', 'urgency', 'due_date_check', 'due_date', 'repeat_check', 'repeat', 'day_of_week',"day_of_month", "yearly_day", "yearly_month", 'time', 'when_made', 'done'])

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    extra_context = {
        "active_page": "accounts"
    }

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("make_todo")
        else:
            print("FORM ERRORS:")
            print(form.errors)
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
            "active_page": "accounts"
        }
    )



def home(request):

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        # Reset streaks if they have not been completed for more than one day
        for streak in profile.streaks.all():
            if streak.last_completed is not None:
                days_since_last = (date.today() - streak.last_completed).days

                if days_since_last > 1:
                    streak.count = 0
                    streak.save()

        # -------------------------
        # Get the month to display
        # -------------------------

        today = date.today()

        try:
            selected_year = int(request.GET.get("year", today.year))
            selected_month = int(request.GET.get("month", today.month))

            if selected_month < 1 or selected_month > 12:
                raise ValueError

        except (ValueError, TypeError):
            selected_year = today.year
            selected_month = today.month

        # -------------------------
        # Previous month
        # -------------------------

        if selected_month == 1:
            previous_month = 12
            previous_year = selected_year - 1
        else:
            previous_month = selected_month - 1
            previous_year = selected_year

        # -------------------------
        # Next month
        # -------------------------

        if selected_month == 12:
            next_month = 1
            next_year = selected_year + 1
        else:
            next_month = selected_month + 1
            next_year = selected_year

        # -------------------------
        # Create calendar
        # -------------------------

        cal = calendar.Calendar(firstweekday=6)

        month_days = cal.monthdatescalendar(
            selected_year,
            selected_month
        )

        # -------------------------
        # Add calendar to each streak
        # -------------------------

        streaks = profile.streaks.all()

        for streak in streaks:

            streak.completed_today = streak.completions.filter(
                completed_date=today
            ).exists()

            completed_dates = set(
                streak.completions.values_list(
                    "completed_date",
                    flat=True
                )
            )

            streak.calendar = []

            for week in month_days:
                calendar_week = []

                for current_date in week:
                    if current_date.month != selected_month:
                        calendar_week.append({
                            "day": 0,
                            "date": current_date,
                            "completed": False,
                        })
                    else:
                        calendar_week.append({
                            "day": current_date.day,
                            "date": current_date,
                            "completed": current_date in completed_dates,
                        })

                streak.calendar.append(calendar_week)

        return render(request, "home.html", {
            "profile": profile,
            "streaks": streaks,
            "active_page": "home",

            "month_name": date(
                selected_year,
                selected_month,
                1
            ).strftime("%B"),

            "selected_year": selected_year,
            "selected_month": selected_month,

            "previous_month": previous_month,
            "previous_year": previous_year,

            "next_month": next_month,
            "next_year": next_year,
        })

    return render(request, "home.html")
    


def accounts(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'logout':
            logout(request)
            print("LOGGED OUT")
            return redirect('home')

    return render(request, 'accounts.html', {
        "active_page": "accounts"
    })

def about_us(request):
    return render(request, "about_us.html", {
        "active_page": "about_us",
    })

@login_required
def create_streak(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            profile = Profile.objects.get(user=request.user)

            Streak.objects.create(
                profile=profile,
                name=name
            )

            return redirect("home")

    return render(request, "create_streak.html")