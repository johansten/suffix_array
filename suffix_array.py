
#-------------------------------------------------------------------------------

class SuffixArray:

	def __init__(self, s):
		self.input	= s
		self.sa 	= _suffix_array(s)
		self.lcp	= _lcp_array(s, self.sa)

	def find_all_duplicates(self):

		"""
		Finds all duplicate substrings

		Iterates over the LCP array, and uses a stack structure to maintain
		spans of different-length matches.

		For an input of

			index:	0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11

			LCP:	1, 1, 1, 7, 3, 0, 1, 1, 9, 5, 5, 0

		these are the spans

			index:	0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11

			spans:	1, 1, 1, 1, 1, 1  1, 1, 1, 1, 1, 1
					         3, 3, 3        5, 5, 5, 5 
					         7, 7           9, 9

		with each span corresponding to a repeated substring of a certain length.

		E.g. The span (7,7) is for two repeats of a substring of length 4-7,
		with substrings starting at SA[3] and SA[4]

		"""

		dupes = []
		stack = [(0, 0)]

		max_length = 0
		for index, length in enumerate(self.lcp):

			if length != max_length:
				if length > max_length:
					stack.append((length, index))
					max_length = length
				else:
					while length < max_length:
						top = stack.pop()
						start_index = top[1]
						end_index   = index
						if max_length >= 2:
							indices = [self.sa[n] for n in xrange(start_index, end_index + 1)]
							min_length = max(length, stack[-1][0])
							min_length = max(2, min_length + 1)
							dupes.append((min_length, max_length, indices))
						max_length = stack[-1][0]

					if length != max_length:
						stack.append((length, top[1]))
						max_length = length

		return dupes

#-------------------------------------------------------------------------------

def _suffix_array(s):

	n = len(s)

	bucket = [0 for i in xrange(256)]
	for i in xrange(n):
		bucket[ord(s[i])] += 1

	sum = 0
	for i in xrange(256):
		curr = bucket[i]
		bucket[i] = sum
		sum += curr

	sa = [0 for i in xrange(n)]
	for i in xrange(n):
		char = ord(s[i])
		sa[bucket[char]] = i
		bucket[char] += 1

	end = 0
	for i in xrange(256):
		start, end	  = end, bucket[i]
		sa[start:end] = sorted(sa[start:end], key=lambda x: buffer(s, x))

	return sa

#-------------------------------------------------------------------------------

def _lcp_array(s, sa):

	"""
	Kasai's algorithm
	"""

	n	= len(s)
	lcp	= [0 for i in xrange(n)]
	isa	= [0 for i in xrange(n)]

	for i in xrange(n):
		isa[sa[i]] = i

	k = 0
	for a in xrange(n):
		i = isa[a] - 1
		b = sa[i]

		if a > b:
			while a + k < n and s[a + k] == s[b + k]:
				k += 1
		else:
			while b + k < n and s[a + k] == s[b + k]:
				k += 1
		lcp[i] = k

		k -= 1
		if k < 0:
			k = 0

	return lcp

#-------------------------------------------------------------------------------
