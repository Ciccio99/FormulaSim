from django import template
from formulaSim.models import *

register = template.Library()


@register.filter
def get_laptime_list(raceid, driverid):
	# Custome templates can only take on arguments, so I'm sending driverid and raceid as a tuple
	laptimes = Laptime.objects.filter(driverid = driverid).filter(raceid = raceid)
	if len(laptimes) > 0:
		return laptimes
	else:
		return None