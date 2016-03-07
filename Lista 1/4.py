# -*- encoding: utf8 -*-
def dzieli(a, b):
	"""Zwraca czy liczba a jest podzielna przez b."""

	return b and not a % b

def cyfry(a):
	"""Zwraca listę cyfr liczby a."""

	return map(int, str(a))

def iloczyn(a):
	"""Zwraca iloczyn liczb z listy a."""

	return reduce(lambda x, y: x*y, a)

def fajna(n):
	"""Zwraca listę fajnych liczb. Liczbę nazwiemy fajną, jeżeli dzieli się 
	zarówno przez sumę swoich cyfr, jak i przez ich iloczyn."""

	return filter(
		lambda a: dzieli(a, sum(cyfry(a))) and dzieli(a, iloczyn(cyfry(a))),
		range(1, n + 1))

for i in fajna(1000):
	print(i)
