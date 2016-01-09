from Systems.Network.TokenBuffer import TokenBuffer
import unittest


class TokenBufferTest(unittest.TestCase):

    def test_push_get(self):
        buff = TokenBuffer()
        msg = "some_random_buffer_data"

        buff.push(msg)
        buff_content = buff.get()

        self.assertEqual(msg, buff_content)

    def test_peek_not_modyfing(self):
        buff = TokenBuffer()
        msg = "some_random_buffer_data"

        buff.push(msg)
        buff_content1 = buff.peek()
        buff_content2 = buff.peek()

        self.assertEqual(msg, buff_content1)
        self.assertEqual(msg, buff_content2)

    def test_get_clears(self):
        buff = TokenBuffer()
        msg = "some_random_buffer_data"

        buff.push(msg)
        buff_content1 = buff.get()
        buff_content2 = buff.get()

        self.assertEqual(msg, buff_content1)
        self.assertEqual("", buff_content2)

    def test_tokenizer(self):
        buff = TokenBuffer()
        msg = "abc!some@!random@!buffer_data@def"

        buff.push(msg)
        token1 = buff.get_first_token(prefix='!', suffix='@')
        token2 = buff.get_first_token(prefix='!', suffix='@')
        token3 = buff.get_first_token(prefix='!', suffix='@')
        token4 = buff.get_first_token(prefix='!', suffix='@')

        self.assertEqual(token1, "some")
        self.assertEqual(token2, "random")
        self.assertEqual(token3, "buffer_data")
        self.assertEqual(token4, "")
