"""Recursive-descent parser for Vākya."""

from typing import List, Optional, Tuple
from ..ast.nodes import (
    Span,
    ASTNode,
    Program,
    Statement,
    Expression,
    Block,
    VarDecl,
    Assignment,
    IfStatement,
    WhileStatement,
    ForEachStatement,
    BreakStatement,
    ContinueStatement,
    ReturnStatement,
    FunctionDecl,
    ImportStatement,
    Param,
    ExpressionStatement,
    BinaryExpr,
    UnaryExpr,
    Literal,
    Identifier,
    ListLiteral,
    MapLiteral,
    IndexExpr,
    MemberExpr,
    CallExpr,
)
from ..lexer.tokens import Token, TokenType
from ..errors import (
    ParseError,
    E201_UNEXPECTED_TOKEN,
    E202_EXPECTED_TOKEN,
    E203_EXPECTED_EXPRESSION,
    E204_INVALID_PARAM,
    E205_INVALID_LOOP_SYNTAX,
    E105_INVALID_ASSIGNMENT_TARGET,
)


class Parser:
    """Parses a sequence of Vākya tokens into an AST."""

    def __init__(self, tokens: List[Token], source_code: str = "", filename: str = "<anonymous>"):
        self.tokens = tokens
        self.pos = 0
        self.source_code = source_code
        self.filename = filename

    # Helper methods
    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[idx]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, tok_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == tok_type

    def _advance(self) -> Token:
        tok = self._peek()
        if not self._is_at_end():
            self.pos += 1
        return tok

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, tok_type: TokenType, error_info, msg: str, help_text: Optional[str] = None) -> Token:
        tok = self._peek()
        if tok.type == tok_type:
            return self._advance()
        raise ParseError.from_info(
            error_info,
            f"{msg}, found {tok.value!r} ({tok.type.name})",
            filename=self.filename,
            line=tok.line,
            column=tok.column,
            length=tok.length,
            source_code=self.source_code,
            help_text=help_text,
        )

    def parse(self) -> Program:
        """Parse all tokens into a Program node."""
        statements: List[Statement] = []
        start_span = Span.from_token(self._peek()) if self.tokens else Span(1, 1, 1, 1, self.filename)

        while not self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                statements.append(stmt)

        end_span = Span.from_token(self._peek())
        span = Span.between(start_span, end_span)
        return Program(statements=statements, span=span)

    # Declarations
    def _declaration(self) -> Statement:
        tok = self._peek()
        if tok.type == TokenType.CHARA:
            return self._var_declaration(is_constant=False)
        elif tok.type == TokenType.DHRUVA:
            return self._var_declaration(is_constant=True)
        elif tok.type == TokenType.KARYA:
            return self._function_declaration()
        elif tok.type == TokenType.AAYAT:
            return self._import_statement()
        else:
            return self._statement()

    def _import_statement(self) -> ImportStatement:
        aayat_tok = self._advance()
        tok = self._peek()
        if tok.type in (TokenType.IDENTIFIER, TokenType.STRING):
            mod_tok = self._advance()
            module_name = str(mod_tok.value)
        else:
            raise ParseError.from_info(
                E202_EXPECTED_TOKEN,
                f"Expected module identifier after 'aayat', found {tok.value!r}",
                filename=self.filename,
                line=tok.line,
                column=tok.column,
                length=tok.length,
                source_code=self.source_code,
                help_text="Specify module name e.g. 'aayat math' or 'aayat strings'",
            )

        alias = None
        if self._check(TokenType.IDENTIFIER) and self._peek().value == "yatha":
            self._advance()
            alias_tok = self._consume(TokenType.IDENTIFIER, E202_EXPECTED_TOKEN, "Expected alias identifier after 'yatha'")
            alias = str(alias_tok.value)

        last_tok = self.tokens[self.pos - 1] if self.pos > 0 else aayat_tok
        return ImportStatement(module_name=module_name, alias=alias, span=Span.between(Span.from_token(aayat_tok), Span.from_token(last_tok)))

    def _var_declaration(self, is_constant: bool) -> VarDecl:
        decl_tok = self._advance()  # chara or dhruva
        start_span = Span.from_token(decl_tok)

        name_tok = self._consume(
            TokenType.IDENTIFIER,
            E202_EXPECTED_TOKEN,
            "Expected variable name after declaration keyword",
            help_text="Provide a valid identifier for the variable name.",
        )
        name = str(name_tok.value)

        type_annotation: Optional[str] = None
        if self._match(TokenType.COLON):
            type_tok = self._consume(
                TokenType.IDENTIFIER,
                E202_EXPECTED_TOKEN,
                "Expected type name after ':'",
                help_text="Use a valid type such as 'sankhya', 'dashamika', 'shabda', 'boolean', 'suchi', or 'naksha'.",
            )
            type_annotation = str(type_tok.value)

        initializer: Optional[Expression] = None
        if self._match(TokenType.EQ):
            initializer = self._expression()
        elif is_constant:
            raise ParseError.from_info(
                E202_EXPECTED_TOKEN,
                f"Constant '{name}' declared with 'dhruva' must be initialized",
                filename=self.filename,
                line=decl_tok.line,
                column=decl_tok.column,
                length=decl_tok.length,
                source_code=self.source_code,
                help_text="Provide an initial value using '= <expression>'.",
            )

        end_span = initializer.span if initializer else Span.from_token(name_tok)
        return VarDecl(
            name=name,
            type_annotation=type_annotation,
            initializer=initializer,
            is_constant=is_constant,
            span=Span.between(start_span, end_span),
        )

    def _function_declaration(self) -> FunctionDecl:
        fn_tok = self._advance()  # karya
        start_span = Span.from_token(fn_tok)

        name_tok = self._consume(
            TokenType.IDENTIFIER,
            E202_EXPECTED_TOKEN,
            "Expected function name after 'karya'",
            help_text="Provide an identifier for the function name.",
        )
        name = str(name_tok.value)

        self._consume(TokenType.LPAREN, E202_EXPECTED_TOKEN, "Expected '(' after function name")
        params: List[Param] = []

        if not self._check(TokenType.RPAREN):
            while True:
                param_name_tok = self._consume(
                    TokenType.IDENTIFIER,
                    E204_INVALID_PARAM,
                    "Expected parameter name",
                )
                param_start = Span.from_token(param_name_tok)
                param_type: Optional[str] = None
                param_end = param_start

                if self._match(TokenType.COLON):
                    ptype_tok = self._consume(
                        TokenType.IDENTIFIER,
                        E202_EXPECTED_TOKEN,
                        "Expected type annotation after ':' in parameter",
                    )
                    param_type = str(ptype_tok.value)
                    param_end = Span.from_token(ptype_tok)

                params.append(Param(name=str(param_name_tok.value), type_annotation=param_type, span=Span.between(param_start, param_end)))

                if not self._match(TokenType.COMMA):
                    break
                if self._check(TokenType.RPAREN):
                    break

        self._consume(TokenType.RPAREN, E202_EXPECTED_TOKEN, "Expected ')' after parameter list")

        return_type: Optional[str] = None
        if self._match(TokenType.ARROW):
            rt_tok = self._consume(
                TokenType.IDENTIFIER,
                E202_EXPECTED_TOKEN,
                "Expected return type after '->'",
            )
            return_type = str(rt_tok.value)

        body = self._block()
        return FunctionDecl(
            name=name,
            params=params,
            return_type=return_type,
            body=body,
            span=Span.between(start_span, body.span),
        )

    # Statements
    def _statement(self) -> Statement:
        tok = self._peek()
        if tok.type == TokenType.YADI:
            return self._if_statement()
        elif tok.type == TokenType.YAVAT:
            return self._while_statement()
        elif tok.type == TokenType.PRATYEKAM:
            return self._for_each_statement()
        elif tok.type == TokenType.VIRAMA:
            self._advance()
            return BreakStatement(span=Span.from_token(tok))
        elif tok.type == TokenType.AGACCHA:
            self._advance()
            return ContinueStatement(span=Span.from_token(tok))
        elif tok.type == TokenType.PRATYAVARTAYA:
            return self._return_statement()
        elif tok.type == TokenType.LBRACE:
            return self._block()
        else:
            return self._expr_or_assignment_statement()

    def _block(self) -> Block:
        lbrace = self._consume(TokenType.LBRACE, E202_EXPECTED_TOKEN, "Expected '{' to start block")
        start_span = Span.from_token(lbrace)
        statements: List[Statement] = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                statements.append(stmt)

        rbrace = self._consume(TokenType.RBRACE, E202_EXPECTED_TOKEN, "Expected '}' to close block")
        end_span = Span.from_token(rbrace)
        return Block(statements=statements, span=Span.between(start_span, end_span))

    def _if_statement(self) -> IfStatement:
        if_tok = self._advance()  # yadi
        start_span = Span.from_token(if_tok)

        condition = self._expression()
        self._match(TokenType.TARHI)  # optional tarhi keyword

        then_block = self._block()
        else_if_branches: List[Tuple[Expression, Block]] = []
        else_block: Optional[Block] = None

        while self._match(TokenType.ANYATHA):
            if self._match(TokenType.YADI):
                elif_cond = self._expression()
                self._match(TokenType.TARHI)
                elif_block = self._block()
                else_if_branches.append((elif_cond, elif_block))
            else:
                else_block = self._block()
                break

        end_span = else_block.span if else_block else (else_if_branches[-1][1].span if else_if_branches else then_block.span)
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_if_branches=else_if_branches,
            else_block=else_block,
            span=Span.between(start_span, end_span),
        )

    def _while_statement(self) -> WhileStatement:
        w_tok = self._advance()  # yavat
        start_span = Span.from_token(w_tok)

        condition = self._expression()
        body = self._block()

        return WhileStatement(condition=condition, body=body, span=Span.between(start_span, body.span))

    def _for_each_statement(self) -> ForEachStatement:
        for_tok = self._advance()  # pratyekam
        start_span = Span.from_token(for_tok)

        var_tok = self._consume(
            TokenType.IDENTIFIER,
            E205_INVALID_LOOP_SYNTAX,
            "Expected variable name after 'pratyekam'",
            help_text="Syntax: 'pratyekam <item> madhye <iterable> { ... }'",
        )
        var_name = str(var_tok.value)

        self._consume(
            TokenType.MADHYE,
            E205_INVALID_LOOP_SYNTAX,
            "Expected 'madhye' in 'pratyekam' loop",
            help_text="Syntax: 'pratyekam <item> madhye <iterable> { ... }'",
        )

        iterable = self._expression()
        body = self._block()

        return ForEachStatement(
            variable=var_name,
            iterable=iterable,
            body=body,
            span=Span.between(start_span, body.span),
        )

    def _return_statement(self) -> ReturnStatement:
        ret_tok = self._advance()  # pratyavartaya
        start_span = Span.from_token(ret_tok)

        value: Optional[Expression] = None
        # Check if next token could start an expression
        if not self._check(TokenType.RBRACE) and not self._is_at_end():
            # Check if it's another statement keyword or end
            next_t = self._peek().type
            if next_t not in (TokenType.VIRAMA, TokenType.AGACCHA, TokenType.PRATYAVARTAYA, TokenType.CHARA, TokenType.DHRUVA, TokenType.KARYA, TokenType.YADI, TokenType.YAVAT, TokenType.PRATYEKAM):
                value = self._expression()

        end_span = value.span if value else start_span
        return ReturnStatement(value=value, span=Span.between(start_span, end_span))

    def _expr_or_assignment_statement(self) -> Statement:
        expr = self._expression()

        # Check for assignment operators
        if self._peek().type in (TokenType.EQ, TokenType.PLUS_EQ, TokenType.MINUS_EQ, TokenType.STAR_EQ, TokenType.SLASH_EQ):
            op_tok = self._advance()
            # Validate assignment target
            if not isinstance(expr, (Identifier, IndexExpr, MemberExpr)):
                raise ParseError.from_info(
                    E105_INVALID_ASSIGNMENT_TARGET,
                    f"Target of assignment '{op_tok.value}' must be an identifier, index, or property",
                    filename=self.filename,
                    line=expr.span.line,
                    column=expr.span.column,
                    length=expr.span.length,
                    source_code=self.source_code,
                )
            value = self._expression()
            span = Span.between(expr.span, value.span)
            return Assignment(target=expr, operator=str(op_tok.value), value=value, span=span)

        return ExpressionStatement(expression=expr, span=expr.span)

    # Expressions
    def _expression(self) -> Expression:
        return self._logic_or()

    def _logic_or(self) -> Expression:
        expr = self._logic_and()

        while self._match(TokenType.VA):
            op_tok = self.tokens[self.pos - 1]
            right = self._logic_and()
            expr = BinaryExpr(left=expr, operator="va", right=right, span=Span.between(expr.span, right.span))

        return expr

    def _logic_and(self) -> Expression:
        expr = self._logic_not()

        while self._match(TokenType.EVAM):
            op_tok = self.tokens[self.pos - 1]
            right = self._logic_not()
            expr = BinaryExpr(left=expr, operator="evam", right=right, span=Span.between(expr.span, right.span))

        return expr

    def _logic_not(self) -> Expression:
        if self._match(TokenType.NA):
            op_tok = self.tokens[self.pos - 1]
            operand = self._logic_not()
            return UnaryExpr(
                operator="na",
                operand=operand,
                span=Span.between(Span.from_token(op_tok), operand.span),
            )
        return self._equality()

    def _equality(self) -> Expression:
        expr = self._relational()

        while self._match(TokenType.EQ_EQ, TokenType.NOT_EQ):
            op_tok = self.tokens[self.pos - 1]
            right = self._relational()
            expr = BinaryExpr(left=expr, operator=str(op_tok.value), right=right, span=Span.between(expr.span, right.span))

        return expr

    def _relational(self) -> Expression:
        expr = self._additive()

        while self._match(TokenType.LT, TokenType.LT_EQ, TokenType.GT, TokenType.GT_EQ):
            op_tok = self.tokens[self.pos - 1]
            right = self._additive()
            expr = BinaryExpr(left=expr, operator=str(op_tok.value), right=right, span=Span.between(expr.span, right.span))

        return expr

    def _additive(self) -> Expression:
        expr = self._multiplicative()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            op_tok = self.tokens[self.pos - 1]
            right = self._multiplicative()
            expr = BinaryExpr(left=expr, operator=str(op_tok.value), right=right, span=Span.between(expr.span, right.span))

        return expr

    def _multiplicative(self) -> Expression:
        expr = self._unary()

        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_tok = self.tokens[self.pos - 1]
            right = self._unary()
            expr = BinaryExpr(left=expr, operator=str(op_tok.value), right=right, span=Span.between(expr.span, right.span))

        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.MINUS, TokenType.PLUS):
            op_tok = self.tokens[self.pos - 1]
            operand = self._unary()
            return UnaryExpr(
                operator=str(op_tok.value),
                operand=operand,
                span=Span.between(Span.from_token(op_tok), operand.span),
            )
        return self._power()

    def _power(self) -> Expression:
        expr = self._postfix()

        if self._match(TokenType.POWER):
            op_tok = self.tokens[self.pos - 1]
            right = self._unary()  # right-associative power
            expr = BinaryExpr(left=expr, operator="**", right=right, span=Span.between(expr.span, right.span))

        return expr

    def _postfix(self) -> Expression:
        expr = self._primary()

        while True:
            if self._match(TokenType.LPAREN):
                # Call expression
                args: List[Expression] = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        args.append(self._expression())
                        if not self._match(TokenType.COMMA):
                            break
                        if self._check(TokenType.RPAREN):
                            break
                rparen = self._consume(TokenType.RPAREN, E202_EXPECTED_TOKEN, "Expected ')' after function arguments")
                expr = CallExpr(callee=expr, arguments=args, span=Span.between(expr.span, Span.from_token(rparen)))
            elif self._match(TokenType.LBRACKET):
                # Index expression
                idx_expr = self._expression()
                rbracket = self._consume(TokenType.RBRACKET, E202_EXPECTED_TOKEN, "Expected ']' after index")
                expr = IndexExpr(target=expr, index=idx_expr, span=Span.between(expr.span, Span.from_token(rbracket)))
            elif self._match(TokenType.DOT):
                # Member expression
                member_tok = self._consume(
                    TokenType.IDENTIFIER,
                    E202_EXPECTED_TOKEN,
                    "Expected property name after '.'",
                )
                expr = MemberExpr(
                    target=expr,
                    member=str(member_tok.value),
                    span=Span.between(expr.span, Span.from_token(member_tok)),
                )
            else:
                break

        return expr

    def _primary(self) -> Expression:
        tok = self._peek()

        if tok.type == TokenType.INTEGER:
            self._advance()
            return Literal(value=tok.value, literal_type="sankhya", span=Span.from_token(tok))

        if tok.type == TokenType.FLOAT:
            self._advance()
            return Literal(value=tok.value, literal_type="dashamika", span=Span.from_token(tok))

        if tok.type == TokenType.STRING:
            self._advance()
            return Literal(value=tok.value, literal_type="shabda", span=Span.from_token(tok))

        if tok.type == TokenType.SATYA:
            self._advance()
            return Literal(value=True, literal_type="boolean", span=Span.from_token(tok))

        if tok.type == TokenType.ASATYA:
            self._advance()
            return Literal(value=False, literal_type="boolean", span=Span.from_token(tok))

        if tok.type == TokenType.SHUNYA:
            self._advance()
            return Literal(value=None, literal_type="shunya", span=Span.from_token(tok))

        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(name=str(tok.value), span=Span.from_token(tok))

        if self._match(TokenType.LPAREN):
            start_tok = self.tokens[self.pos - 1]
            expr = self._expression()
            rparen = self._consume(TokenType.RPAREN, E202_EXPECTED_TOKEN, "Expected ')' after grouping expression")
            return expr

        if self._match(TokenType.LBRACKET):
            # List literal
            start_tok = self.tokens[self.pos - 1]
            elements: List[Expression] = []
            if not self._check(TokenType.RBRACKET):
                while True:
                    elements.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break
                    if self._check(TokenType.RBRACKET):
                        break
            rbracket = self._consume(TokenType.RBRACKET, E202_EXPECTED_TOKEN, "Expected ']' after list elements")
            return ListLiteral(
                elements=elements,
                span=Span.between(Span.from_token(start_tok), Span.from_token(rbracket)),
            )

        if self._match(TokenType.LBRACE):
            # Map literal
            start_tok = self.tokens[self.pos - 1]
            pairs: List[Tuple[Expression, Expression]] = []
            if not self._check(TokenType.RBRACE):
                while True:
                    # In map literal: key can be string literal or identifier or general expr
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING):
                        k_tok = self._advance()
                        if k_tok.type == TokenType.IDENTIFIER:
                            key_expr: Expression = Literal(value=str(k_tok.value), literal_type="shabda", span=Span.from_token(k_tok))
                        else:
                            key_expr = Literal(value=str(k_tok.value), literal_type="shabda", span=Span.from_token(k_tok))
                    else:
                        key_expr = self._expression()

                    self._consume(TokenType.COLON, E202_EXPECTED_TOKEN, "Expected ':' after map key")
                    val_expr = self._expression()
                    pairs.append((key_expr, val_expr))

                    if not self._match(TokenType.COMMA):
                        break
                    if self._check(TokenType.RBRACE):
                        break

            rbrace = self._consume(TokenType.RBRACE, E202_EXPECTED_TOKEN, "Expected '}' after map pairs")
            return MapLiteral(
                pairs=pairs,
                span=Span.between(Span.from_token(start_tok), Span.from_token(rbrace)),
            )

        raise ParseError.from_info(
            E203_EXPECTED_EXPRESSION,
            f"Unexpected token {tok.value!r} ({tok.type.name})",
            filename=self.filename,
            line=tok.line,
            column=tok.column,
            length=tok.length,
            source_code=self.source_code,
        )
