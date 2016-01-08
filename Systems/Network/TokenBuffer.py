
class TokenBuffer(object):
    def __init__(self):
        self._buffer = ""  # empty buffer

    # Clears buffer
    def clear(self):
        self._buffer = ""

    # Retrieves buffered data without clearing it
    def peek(self):
        result = self._buffer
        return result

    # Retrieves buffered data and clears it
    def get(self):
        result = self.peek()
        self.clear()
        return result

    # Returns first valid token without removing it from buffer
    def peek_first_token(self, prefix, suffix):
        return self._retrieve_first_token(prefix, suffix, remove=False)

    # Returns first valid token and removes it from buffer
    def get_first_token(self, prefix, suffix):
        return self._retrieve_first_token(prefix, suffix, remove=True)

    # Returns list of all valid tokens without removing them from buffer
    def peek_all_tokens(self, prefix, suffix):
        return self._retrieve_all_tokens(prefix, suffix, remove=False)

    # Returns list of all valid tokens and effectivly removes them from buffer
    def get_all_tokens(self, prefix, suffix):
        return self._retrieve_all_tokens(prefix, suffix, remove=True)

    # Pushes new raw data to buffer
    def push(self, data):
        self._buffer += data

    # Retrieves first token starting with 'prefix' and ending with 'suffix' and consumes it when remove == True
    def _retrieve_first_token(self, prefix, suffix, remove):
        prefix_index = self._buffer.find(prefix)
        suffix_index = self._buffer[prefix_index+1:].find(suffix)

        if prefix_index == - 1 or suffix_index == -1:
            return ""

        first_token = self._buffer[prefix_index+1:suffix_index+prefix_index+1]

        if len(first_token) > 0 and remove:
            self._buffer = self._buffer[suffix_index+prefix_index+2:]

        return first_token

    # Retrieves all valid tokens and consumes them if remove == True
    def _retrieve_all_tokens(self, prefix, suffix, remove):
        tokens = []

        while True:
            token = self._retrieve_first_token(prefix, suffix, remove=remove)
            if len(token) > 0:
                tokens.append(token)
            else:
                break

        return tokens
