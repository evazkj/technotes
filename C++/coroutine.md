# Coroutine

```c++
generator<char> get_char() {
    while (!eof) {
        co_yield c;
    }
} // reader

generator<token> get_token() {
    while (auto c = get_char()) {
        co_yield t;
    }
} // lexer

generator<ast_node> parse_expression() {
    auto t = get_token();
    
    co_yield node;
}
```

## Keywords

*   `co_await`: suspends coroutine while waiting for another compuatation to finish
*   `co_yield`
*   `co_return`

```c++
co_awai
```

