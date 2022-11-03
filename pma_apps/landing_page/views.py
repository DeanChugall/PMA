from django.shortcuts import render
from django.views.generic import View


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "landing_page/landing_page.html")
