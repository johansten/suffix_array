
import unittest
import suffix_array

from os.path import commonprefix

#-------------------------------------------------------------------------------

class SuffixArray_Test(unittest.TestCase):

	def setUp(self):

		self.input = "SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES"

	def test_suffix_array(self):

		sa1 = _suffix_array_original(self.input)
		sa2 = suffix_array._suffix_array(self.input)
		self.assertEqual(sa1, sa2)

	def test_lcp_array(self):

		sa  = suffix_array._suffix_array(self.input)
		lcp = suffix_array._lcp_array(self.input, sa)

		n = len(self.input)
		for i in xrange(n - 1):
			length = len(commonprefix(
				(buffer(self.input, sa[i]), buffer(self.input, sa[i + 1]))
			))
			self.assertEqual(length, lcp[i])

#-------------------------------------------------------------------------------

def _suffix_array_original(s):

	sa = range(len(s))
	sa.sort(key=lambda x: buffer(s, x))
	return sa

#-------------------------------------------------------------------------------

unittest.main()

#-------------------------------------------------------------------------------
