from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Profile, Streak


class StreakRestartTests(TestCase):
	def test_expired_zero_streak_can_be_restarted(self):
		user = User.objects.create_user(username="streak-user", password="test-pass")
		profile = Profile.objects.get(user=user)
		today = timezone.localdate()
		streak = Streak.objects.create(
			profile=profile,
			name="Exercise",
			count=4,
			last_completed=today - timedelta(days=2),
		)
		self.client.force_login(user)

		self.client.get(reverse("home"))
		streak.refresh_from_db()
		self.assertEqual(streak.count, 0)
		self.assertIsNone(streak.last_completed)

		response = self.client.post(
			reverse("home"),
			{"action": "complete_streak", "streak_id": streak.id},
		)

		streak.refresh_from_db()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(streak.count, 1)
		self.assertEqual(streak.last_completed, today)
