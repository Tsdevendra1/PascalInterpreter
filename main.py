# Token Types
# EOF =  End of File
INTEGER, PLUS, EOF, MINUS = 'INTEGER', 'PLUS', 'EOF', 'MINUS'


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        # Token value can be 0,1,2,3,4,5,6,7,8,9, '+', or None
        self.value = value

    def __str__(self):
        return 'Token({token_type}, {value})'.format(token_type=self.token_type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        # text would be the input e.g. "5+3"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # Current token object instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input, unexpected token {}')

    def advance_pos(self):
        """
        advance the position pointer and set the current_char variable
        :return:
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """
        Advance the pointer to the next non whitespace character
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance_pos()

    def integer(self):
        """
        :return: A digit of varying size depending on the input given by the user
        """
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance_pos()

        return int(result)

    def get_next_token(self):
        """
        Lexical analyzer. Responsible for breaking a sentence down into tokens
        """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                # Continue makes the loop start from the top
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance_pos()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance_pos()
                return Token(MINUS, "-")

            # If it reached here it means it wasn't in one of the if statements hence, an error
            self.error()

        # If it skipped the while loop then it means it's the end of the file
        return Token(EOF, None)

    def eat(self, token_type):
        """
        If the current token being held matches the token passed in then we get the next token.
        :param token_type: A token type such as INTEGER, PLUS etc...
        """
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        # Get first input
        self.current_token = self.get_next_token()

        # We expect the first term to be an integer
        result = self.term()

        while self.current_token.token_type in (PLUS, MINUS):
            # This loop should always finish with a PLUS OR MINUS whilst there is one in the text
            token = self.current_token
            if token.token_type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.token_type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
