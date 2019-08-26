from django import template

register = template.Library()


@register.filter(name='div')
def div(divident, divisor):
	try:
		res = float(divident)/float(divisor)
		return float(int(res) if res//1 == res else res)
	except (ValueError, ZeroDivisionError):
		return None

@register.filter(name='mul')
def mul(a, b):
	try:
		res = float(a)*float(b)
		return float(int(res) if res//1 == res else res)
	except (ValueError, ZeroDivisionError):
		return None