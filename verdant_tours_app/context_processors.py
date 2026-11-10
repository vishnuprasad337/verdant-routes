from .models import Destination, TourPackage


def booking_packages(request):

    packages = TourPackage.objects.all().order_by("name")

    # Unique locations for the navbar Destination dropdown (case-insensitive)
    seen = {}

    locations = (
        Destination.objects
        .exclude(location="")
        .order_by("location")
        .values_list("location", flat=True)
    )

    for loc in locations:
        loc = loc.strip()
        if loc and loc.lower() not in seen:
            seen[loc.lower()] = loc

    return {
        "booking_packages": packages,
        "nav_locations": list(seen.values()),
    }