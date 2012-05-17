# Test for flatten.py 
import tempfile 
import unittest2
import flatex

class FlattenTest(unittest2.TestCase):

    def setUp(self):
        file_text = """
Here is some stuff
\input{foo.tex}
And here is some more stuff.
        """
        f = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file_name = f.name
        #f = open("/tmp/flatex_test.tex", "w")
        f.write(file_text)
        f.close() 
        g = open("/tmp/foo.tex", "w")
        g.write("BONZAI!\n")
        g.close() 
    
    def test_is_input_true(self): 
        true_line = "\input{foo.tex}" 
        m = flatex.is_input(true_line)
        self.assertEqual(m.group() is not None, True)

    def test_is_input_false_comment(self): 
        true_line = "%\input{foo.tex}" 
        m = flatex.is_input(true_line)
        self.assertEqual(m is None, True)

    def test_is_input_false(self): 
        false_line = "bar bar bar" 
        m = flatex.is_input(false_line)
        self.assertEqual(m is None, True)
        
    def test_get_input(self): 
        true_line = "\input{foo.tex}" 
        self.assertEqual(flatex.get_input(true_line), 'foo.tex')

    def test_get_input_dash(self): 
        true_line = "\input{foo-bar.tex}" 
        self.assertEqual(flatex.get_input(true_line), 'foo-bar.tex')

    def test_combine_path(self): 
        base_path = "/tmp"
        relative_ref = "test.tex"
        result = "/tmp/test.tex"
        self.assertEqual(flatex.combine_path(base_path, 
                                              relative_ref), result)

    def test_combine_path_dot_notation(self): 
        base_path = "/tmp"
        relative_ref = "./includes/test.tex"
        result = "/tmp/includes/test.tex"
        self.assertEqual(flatex.combine_path(base_path, 
                                              relative_ref), result)


    def test_expand_file_open_file(self): 
         combined_file = flatex.expand_file(self.temp_file_name)
         expected_results = """
Here is some stuff
BONZAI!
And here is some more stuff.
        """
         self.assertEqual(''.join(combined_file),expected_results)

if __name__ == '__main__':
    unittest2.main()
