#!/bin/python3

# The MIT License
#
# Copyright 2022 David Kleszyk <dkleszyk@gmail.com>.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import itertools
import os
import os.path
import shutil
import textwrap

type_names = {
    "void": None,
    "object": "",
    "boolean": "Boolean",
    "byte": "Byte",
    "char": "Char",
    "double": "Double",
    "float": "Float",
    "int": "Int",
    "long": "Long",
    "short": "Short",
    "object[]": "ArraySegment",
    "boolean[]": "BooleanArraySegment",
    "byte[]": "ByteArraySegment",
    "char[]": "CharArraySegment",
    "double[]": "DoubleArraySegment",
    "float[]": "FloatArraySegment",
    "int[]": "IntArraySegment",
    "long[]": "LongArraySegment",
    "short[]": "ShortArraySegment",
}

types = tuple(type_names.keys())

fn_ordinals = (None, "", "Bi", "Tri", "Tetra")

op_ordinals = (None, "Unary", "Binary", "Ternary", "Quaternary")

pos_ordinals = (None, "first", "second", "third", "fourth")

cnt_ordinals = (None, None, "two", "three", "four")

in_params = (None, "T", "U", "V", "W")
out_params = (None, "R", "S", "Q", "P")
elem_params = (None, "E", "F", "G", "H")

built_ins = (
    "Runnable",
    "BiConsumer",
    "BiFunction",
    "BinaryOperator",
    "BiPredicate",
    "BooleanSupplier",
    "Consumer",
    "DoubleBinaryOperator",
    "DoubleConsumer",
    "DoubleFunction",
    "DoublePredicate",
    "DoubleSupplier",
    "DoubleToIntFunction",
    "DoubleToLongFunction",
    "DoubleUnaryOperator",
    "Function",
    "IntBinaryOperator",
    "IntConsumer",
    "IntFunction",
    "IntPredicate",
    "IntSupplier",
    "IntToDoubleFunction",
    "IntToLongFunction",
    "IntUnaryOperator",
    "LongBinaryOperator",
    "LongConsumer",
    "LongFunction",
    "LongPredicate",
    "LongSupplier",
    "LongToDoubleFunction",
    "LongToIntFunction",
    "LongUnaryOperator",
    "ObjDoubleConsumer",
    "ObjIntConsumer",
    "ObjLongConsumer",
    "Predicate",
    "Supplier",
    "ToDoubleBiFunction",
    "ToDoubleFunction",
    "ToIntBiFunction",
    "ToIntFunction",
    "ToLongBiFunction",
    "ToLongFunction",
    "UnaryOperator",
)

# helpers for documentation
def aan(s):
    return "an" if s[:1] in "AEIOUaeiou" else "a"


def Aan(s):
    return aan(s).capitalize()


def javadoc(
    description,
    *,
    indent=0,
    authors=None,
    parameters=None,
    result=None,
    output_as_generator=False,
):
    # when generating documentation,
    # use letters instead of symbols
    # to prevent javadoc elements
    # from getting split while wrapping
    #
    # use tilde for non-breaking space
    sym2let = str.maketrans("{}@~", "ÍÌÆµ")
    let2sym = str.maketrans("ÍÌÆµ", "{}@ ")

    base_width = 80 - 3 - indent

    authors = tuple(authors) if authors is not None else ()
    parameters = tuple(parameters) if parameters is not None else ()
    result = str(result) if result is not None else ""

    def wrap_iter(s):
        yield s
        w = f"{' '*len(s)}"
        while True:
            yield w

    def generator():
        yield f"{' '*indent}/**"

        for line in textwrap.wrap(
            description.translate(sym2let),
            width=base_width,
            break_on_hyphens=False,
            break_long_words=False,
        ):
            yield f"{' '*indent} * {line.translate(let2sym)}"

        if authors:
            yield f"{' '*indent} *"
            for author in authors:
                yield f"{' '*indent} * @author {author}"

        if parameters:
            yield f"{' '*indent} *"
            align = 1 + max((len(name) for name, _ in parameters))
            for name, desc in parameters:
                for wrap, line in zip(
                    wrap_iter(f"@param {name:<{align}}"),
                    textwrap.wrap(
                        desc.translate(sym2let),
                        width=base_width - 7 - align,
                        break_on_hyphens=False,
                        break_long_words=False,
                    ),
                ):
                    yield f"{' '*indent} * {wrap}{line.translate(let2sym)}"

        if result:
            yield f"{' '*indent} *"
            for wrap, line in zip(
                wrap_iter("@return "),
                textwrap.wrap(
                    result.translate(sym2let),
                    width=base_width - 8,
                    break_on_hyphens=False,
                    break_long_words=False,
                ),
            ):
                yield f"{' '*indent} * {wrap}{line.translate(let2sym)}"

        yield f"{' '*indent} */"

    return generator() if output_as_generator else list(generator())


# reset directory tree
base_dir = os.path.join("src", "main", "java")
base_pkg = "me.dkleszyk.java.function.extra"

base_pkg_dir = os.path.join(*([base_dir] + base_pkg.split(".")))
if os.path.isdir(base_pkg_dir):
    shutil.rmtree(base_pkg_dir)

# collect names for diagnostics
names = []

for argc in range(0, 4 + 1):
    # types[1:] -- exclude 'void' from argv
    assert types[0] == "void"
    for argv in itertools.product(types[1:], repeat=argc):
        args = set(argv)

        # filter input
        if (
            argc > 1
            and len(args) > 1
            and (argv[0] != "object" or len(set(argv[1:])) > 1)
        ):
            # exclude mixed argument types unless obj + 1 other type
            continue
        if argc > 2 and args != {"object"}:
            # exclude more than two args unless all objs
            continue
        if sum((1 for a in argv if a.endswith("[]"))) > 1:
            # exclude more than one array segment argument
            continue

        for ret in types:
            # filter output
            if ret.endswith("[]"):
                # exclude array segment result
                continue
            if True in (a.endswith("[]") for a in argv):
                if (
                    ret not in ("object", "boolean", "void", "int", "long", "double")
                    and f"{ret}[]" not in argv
                ):
                    # only allow Function, Predicate, and Consumer variants for array segments
                    # plus ToIntFunction and ToLongFunction, for returning indicies or counts
                    # plus ToDoubleFunction, for returning aggregates
                    # plus the ToXFunction variant where X is the element type, for returning array elements
                    continue
            else:
                if (
                    argc > 1
                    and ret not in ("object", "boolean", "void")
                    and ret not in argv
                ):
                    # only allow Function, BiFunction, Predicate, Consumer, and Operator and ObjXToXFunction variants if > 1 argument
                    # i.e. no ShortToFloatBiFunction
                    if argc > 2 or args != {"object"}:
                        # plus ToXBiFunction
                        continue
                if argc > 2 and ret not in ("object", "boolean"):
                    # only allow Function and Predicate variants if > 2 arguments
                    continue

            # get name and filter against built-ins
            if argc == 0:
                if ret == "void":
                    name = "Runnable"
                    mthd = "run"
                else:
                    name = f"{type_names[ret]}Supplier"
                    mthd = f"getAs{type_names[ret]}" if ret != "object" else "get"
            elif ret == "void":
                if len(args) == 1:
                    name = f"{type_names[argv[0]]}{fn_ordinals[argc]}Consumer"
                else:
                    name = (
                        "".join(
                            ("Obj" if a == "object" else type_names[a] for a in argv)
                        )
                        + "Consumer"
                    )
                mthd = "accept"
            elif ret != "object" and {ret} == args:
                name = f"{type_names[argv[0]]}{op_ordinals[argc]}Operator"
                mthd = f"applyAs{type_names[ret]}"
            elif ret == "boolean":
                if len(args) == 1:
                    name = f"{type_names[argv[0]]}{fn_ordinals[argc]}Predicate"
                else:
                    name = (
                        "".join(
                            ("Obj" if a == "object" else type_names[a] for a in argv)
                        )
                        + "Predicate"
                    )
                mthd = "test"
            elif ret == "object":
                if len(args) == 1:
                    name = f"{type_names[argv[0]]}{fn_ordinals[argc]}Function"
                else:
                    name = (
                        "".join(
                            ("Obj" if a == "object" else type_names[a] for a in argv)
                        )
                        + "Function"
                    )
                mthd = "apply"
            else:
                if len(args) == 1:
                    name = f"{type_names[argv[0]]}To{type_names[ret]}{fn_ordinals[argc]}Function"
                else:
                    name = (
                        "".join(
                            ("Obj" if a == "object" else type_names[a] for a in argv)
                        )
                        + f"To{type_names[ret]}Function"
                    )
                mthd = f"applyAs{type_names[ret]}"

            if name in built_ins:
                continue

            names.append(name)

            # variables for javadoc
            if ret == "void":
                operation, performs, using = (
                    "operation",
                    "performs",
                    ("using" if argc > 0 else None),
                )
            elif argc == 0:
                operation, performs, using = "operation", "supplies", None
            elif ret != "object" and {ret} == args:
                operation, performs, using = "operator", "applies", "to"
            elif ret == "boolean":
                operation, performs, using = "predicate", "evaluates", "against"
            else:
                operation, performs, using = "function", "applies", "to"
            Performs = performs.capitalize()
            perform = f"{performs[:-3]}y" if performs.endswith("ies") else performs[:-1]
            performed = performs[:-1] + ("d" if performs.endswith("es") else "ed")

            if argc == 0:
                arguments, match, those, supply = (
                    None,
                    None,
                    None,
                    (
                        "value"
                        if ret == "object"
                        else f"{{@code~{ret}}} value"
                        if ret != "void"
                        else None
                    ),
                )
            elif argc == 1 and not argv[0].endswith("[]"):
                arguments, match, those, supply = "argument", "matches", "that", None
            else:
                arguments, match, those, supply = "arguments", "match", "those", None

            # generic parameter list
            # (name, description)
            in_param_cnt = sum((1 for a in argv if a == "object"))
            elem_param_cnt = sum((1 for a in argv if a == "object[]"))
            out_param_cnt = 1 if ret == "object" else 0
            p_list = []

            for n in range(1, in_param_cnt + 1):
                p = in_params[n]
                pos = f"{pos_ordinals[n]} " if in_param_cnt > 1 else ""
                typ = "object-valued " if in_param_cnt < argc else ""
                p_list.append(
                    (p, f"The type of the {pos}{typ}argument to the {operation}.")
                )

            for n in range(1, elem_param_cnt + 1):
                p = elem_params[n]
                pos = f"{pos_ordinals[n]} " if elem_param_cnt > 1 else ""
                # typ = ""
                p_list.append(
                    (
                        p,
                        f"The type of the elements of the {pos}array argument to the {operation}.",
                    )
                )

            for n in range(1, out_param_cnt + 1):
                p = out_params[n]
                # pos = ""
                # typ = ""
                p_list.append((p, f"The type of the result of the {operation}."))

            # expanded args list
            # (type, name, abbreviated name, description)
            if argc == 0:
                a_list = []
            elif args == {"object"}:
                pos_iter = (
                    (f"{pos_ordinals[n]} " for n in itertools.count(1))
                    if argc > 1
                    else itertools.repeat("")
                )
                a_list = [
                    (
                        p,
                        p.lower(),
                        p.lower(),
                        f"The {pos}argument to the {operation}.",
                    )
                    for p, pos in zip(in_params[1 : argc + 1], pos_iter)
                ]
            elif (
                argc in (1, 2)
                and len(args) == 1
                and True not in (a.endswith("[]") for a in argv)
            ):
                if argc == 1:
                    a_list = [
                        (
                            argv[0],
                            ("operand" if {ret} == args else "value"),
                            r"x",
                            f"The argument to the {operation}.",
                        )
                    ]
                else:
                    assert argc == 2
                    a_list = [
                        (
                            argv[0],
                            r"left",
                            r"x",
                            f"The {pos_ordinals[1]} argument to the {operation}.",
                        ),
                        (
                            argv[1],
                            r"right",
                            r"y",
                            f"The {pos_ordinals[2]} argument to the {operation}.",
                        ),
                    ]
            else:
                a_list = []
                if argv[0] == "object":
                    assert argc == 2
                    assert argv[1] != "object"
                    a_list.append(
                        (
                            in_params[1],
                            r"obj",
                            r"obj",
                            f"The object-valued argument to the {operation}.",
                        )
                    )
                    a = argv[1]
                    a_iter = itertools.repeat(a, 1)
                    suf_iter = itertools.repeat("")
                    pos_iter = itertools.repeat("")
                    if a == "object[]":
                        typ_iter = itertools.repeat("array ")
                    elif a.endswith("[]"):
                        typ_iter = itertools.repeat(f"{{@code~{a[:-2]}}}-valued array ")
                    else:
                        typ_iter = itertools.repeat(f"{{@code~{a}}}-valued ")
                else:
                    assert len(args) == 1
                    (a,) = args
                    a_iter = itertools.repeat(a, argc)
                    if argc == 1:
                        suf_iter = itertools.repeat("")
                        pos_iter = itertools.repeat("")
                    else:
                        suf_iter = (str(n) for n in itertools.count(1))
                        pos_iter = (f"{pos_ordinals[n]} " for n in itertools.count(1))
                    if a.endswith("[]"):
                        typ_iter = itertools.repeat("array ")
                    else:
                        typ_iter = itertools.repeat("")

                e_iter = (f"{p}[]" for p in elem_params[1:])
                for a, suf, pos, typ in zip(a_iter, suf_iter, pos_iter, typ_iter):
                    a_name, a_abbr = (
                        (f"array{suf}", f"arr{suf}")
                        if a.endswith("[]")
                        else (f"value{suf}", f"val{suf}")
                    )

                    a_list.append(
                        (
                            (a if a != "object[]" else next(e_iter)),
                            a_name,
                            a_abbr,
                            f"The {pos}{typ}argument to the {operation}.",
                        )
                    )

                    if a.endswith("[]"):
                        a_list.append(
                            (
                                "int",
                                f"fromIndex{suf}",
                                f"from{suf}",
                                f"The start index in {{@code~array{suf}}}, inclusive.",
                            )
                        )
                        a_list.append(
                            (
                                "int",
                                f"toIndex{suf}",
                                f"to{suf}",
                                f"The end index in {{@code~array{suf}}}, exclusive.",
                            )
                        )

            # generate methods
            imports = set()
            static_imports = set()
            static_methods = {}
            instance_methods = {}

            # functional interface method
            if argc == 0:
                if ret != "void":
                    mthd_desc = f"{Performs} a {supply}."
                else:
                    mthd_desc = f"{Performs} the {operation}."
            else:
                mthd_desc = f"{Performs} the {operation} {using} the given {arguments}."

            if argc > 0 and ret == "boolean" and args != {"boolean"}:
                rslt_desc = f"A {{@code~true}}-or-{{@code~false}} value indicating whether the {arguments} {match} the {operation}."
            elif ret != "void":
                rslt_desc = f"The result of the {operation}."
            else:
                rslt_desc = None

            mthd_doc = javadoc(
                mthd_desc,
                indent=4,
                parameters=((a_name, a_desc) for _, a_name, _, a_desc in a_list),
                result=rslt_desc,
            )

            rslt = out_params[1] if ret == "object" else ret
            if argc > 0:
                instance_methods[mthd] = (
                    mthd_doc
                    + [f"    {rslt} {mthd}("]
                    + [
                        f"        final {a_type} {a_name},"
                        for a_type, a_name, _, _ in a_list[:-1]
                    ]
                    + [
                        f"        final {a_type} {a_name});"
                        for a_type, a_name, _, _ in a_list[-1:]
                    ]
                )
            else:
                instance_methods[mthd] = mthd_doc + [f"    {rslt} {mthd}();"]

            # other methods
            p_text = ("<" + ", ".join((p for p, _ in p_list)) + ">") if p_list else ""
            a_text = ", ".join((a_abbr for _, _, a_abbr, _ in a_list))
            par_a_text = a_text if len(a_list) == 1 else f"({a_text})"
            var_p_text = (
                (
                    "<"
                    + ", ".join(
                        (
                            f"? super {p}"
                            if p in in_params
                            else f"? extends {p}"
                            if p in out_params
                            else f"{p}"
                            if p in elem_params
                            else None
                            for p, _ in p_list
                        )
                    )
                    + ">"
                )
                if p_list
                else ""
            )

            # identity
            if argc == 1 and ret != "object" and args == {ret}:
                mdoc = javadoc(
                    f"Returns {aan(operation)} {operation} that always returns its input argument.",
                    indent=4,
                    result=f"{Aan(operation)} {operation} that always returns its input argument.",
                )
                lmbd = f"{par_a_text} ->${a_text}"

                static_methods["identity"] = mdoc + [
                    f"    static {name} identity()",
                    r"    {",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # negated (unary op)
            if argc == 1 and ret == "boolean" and args == {"boolean"}:
                mdoc = javadoc(
                    f"Returns {aan(operation)} {operation} that always returns the logical negation of its input argument.",
                    indent=4,
                    result=f"{Aan(operation)} {operation} that always returns the logical negation its input argument.",
                )
                lmbd = f"{par_a_text} ->$!{a_text}"

                static_methods["negated"] = mdoc + [
                    f"    static {name} negated()",
                    r"    {",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # andThen (consumer/runnable)
            if ret == "void":
                if argc == 0:
                    desc = f"Returns a compound {operation} that first {performs} this {operation} and then {performs} the given {operation}."
                else:
                    desc = f"Returns a compound {operation} that first {performs} this {operation} {using} its input {arguments} and then {performs} the given {operation} {using} {those} same {arguments}."

                mdoc = javadoc(
                    desc,
                    indent=4,
                    parameters=(
                        (
                            "after",
                            f"The {operation} to {perform} after this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that first {performs} this {operation} and then {performs} the {{@code~after}} {operation}.",
                )

                imports.add("java.util.Objects")
                instance_methods["andThen"] = mdoc + [
                    f"    default {name}{p_text} andThen(",
                    f"        final {name}{var_p_text} after)",
                    r"    {",
                    r"        Objects.requireNonNull(after);",
                    f"        return {par_a_text} ->",
                    r"        {",
                    f"            {mthd}({a_text});",
                    f"            after.{mthd}({a_text});",
                    r"        };",
                    r"    }",
                ]

            # andThen (function/supplier)
            elif ret == "object":
                o1, o2 = out_params[1], out_params[2]
                assert o1 in (p for p, _ in p_list)
                p_text2 = (
                    "<" + ", ".join((p if p != o1 else o2 for p, _ in p_list)) + ">"
                )

                if argc == 0:
                    desc = f"Returns a compound {operation} that first {performs} a {supply} and then applies the given function to produce a transformed result."
                    rslt = f"A compound {operation} that first {performs} a {supply} and then applies the {{@code~after}} function."
                else:
                    desc = f"Returns a compound {operation} that first {performs} this {operation} {using} its input {arguments} and then applies the given function to produce a transformed result."
                    rslt = f"A compound {operation} that first {performs} this {operation} and then applies the {{@code~after}} function."

                mdoc = javadoc(
                    desc,
                    indent=4,
                    parameters=(
                        (
                            f"<{o2}>",
                            f"The type of the result of the compound {operation}.",
                        ),
                        (
                            "after",
                            f"A function to apply to the result of this {operation}.",
                        ),
                    ),
                    result=rslt,
                )
                lmbd = f"{par_a_text} ->$after.apply({mthd}({a_text}))"

                imports.add("java.util.Objects")
                imports.add("java.util.function.Function")
                instance_methods["andThen"] = mdoc + [
                    f"    default <{o2}> {name}{p_text2} andThen(",
                    f"        final Function<? super {o1}, ? extends {o2}> after)",
                    r"    {",
                    r"        Objects.requireNonNull(after);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # andThen (unary op)
            elif argc == 1 and args == {ret}:
                assert ret != "object"

                mdoc = javadoc(
                    f"Returns a compound {operation} that first {performs} this {operation} {using} its input {arguments} and then {performs} the given {operation} to produce a transformed result.",
                    indent=4,
                    parameters=(
                        (
                            "after",
                            f"{Aan(operation)} {operation} to {perform} {using} the result of this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that first {performs} this {operation} and then {performs} the {{@code~after}} {operation}.",
                )
                lmbd = f"{par_a_text} ->$after.{mthd}({mthd}({a_text}))"

                imports.add("java.util.Objects")
                instance_methods["andThen"] = mdoc + [
                    f"    default {name} andThen(",
                    f"        final {name} after)",
                    r"    {",
                    r"        Objects.requireNonNull(after);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # compose (function/consumer)
            if argc == 1 and args == {"object"}:
                i1, i2 = in_params[1], in_params[2]
                assert i1 in (p for p, _ in p_list)
                p_text2 = (
                    "<" + ", ".join((p if p != i1 else i2 for p, _ in p_list)) + ">"
                )

                if ret == "void":
                    desc = f"Returns a compound {operation} that first applies the given function to its input argument and then {performs} this {operation} {using} its result."
                else:
                    desc = f"Returns a compound {operation} that first applies the given function to its input argument and then {performs} this {operation} to produce a transformed result."

                mdoc = javadoc(
                    desc,
                    indent=4,
                    parameters=(
                        (
                            f"<{i2}>",
                            f"The type of the input to the compound {operation}.",
                        ),
                        (
                            "before",
                            f"A function to apply to produce the input to this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that first applies the {{@code~before}} function and then {performs} this {operation}.",
                )
                lmbd = f"{par_a_text} ->${mthd}(before.apply({a_text}))"

                imports.add("java.util.Objects")
                imports.add("java.util.function.Function")
                instance_methods["compose"] = mdoc + [
                    f"    default <{i2}> {name}{p_text2} compose(",
                    f"        final Function<? super {i2}, ? extends {i1}> before)",
                    r"    {",
                    r"        Objects.requireNonNull(before);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # compose (unary op)
            elif argc == 1 and args == {ret}:
                assert ret != "object"

                mdoc = javadoc(
                    f"Returns a compound {operation} that first {performs} the given {operation} {using} its input argument and then {performs} this {operation} to produce a transformed result.",
                    indent=4,
                    parameters=(
                        (
                            "before",
                            f"{Aan(operation)} {operation} to {perform} to produce the input to this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that first {performs} the {{@code~before}} {operation} and then {performs} this {operation}.",
                )
                lmbd = f"{par_a_text} ->${mthd}(before.{mthd}({a_text}))"

                imports.add("java.util.Objects")
                instance_methods["compose"] = mdoc + [
                    f"    default {name} compose(",
                    f"        final {name} before)",
                    r"    {",
                    r"        Objects.requireNonNull(before);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # predicate methods
            if argc > 0 and ret == "boolean" and args != {"boolean"}:
                # and
                mdoc = javadoc(
                    f"Returns a compound {operation} that represents the logical intersection of this {operation} and the given {operation}. "
                    + f"The compound {operation} {performs} this {operation} first; the other {operation} is not {performed} if the result of this {operation} is {{@code~false}}.",
                    indent=4,
                    parameters=(
                        (
                            "other",
                            f"{Aan(operation)} {operation} to be intersected with this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that represents the logical intersection of this {operation} and the {{@code~other}} {operation}.",
                )
                lmbd = f"{par_a_text} ->${mthd}({a_text}) && other.{mthd}({a_text})"

                imports.add("java.util.Objects")
                instance_methods["and"] = mdoc + [
                    f"    default {name}{p_text} and(",
                    f"        final {name}{var_p_text} other)",
                    r"    {",
                    r"        Objects.requireNonNull(other);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

                # or
                mdoc = javadoc(
                    f"Returns a compound {operation} that represents the logical union of this {operation} and the given {operation}. "
                    + f"The compound {operation} {performs} this {operation} first; the other {operation} is not {performed} if the result of this {operation} is {{@code~true}}.",
                    indent=4,
                    parameters=(
                        (
                            "other",
                            f"{Aan(operation)} {operation} to be unioned with this {operation}.",
                        ),
                    ),
                    result=f"A compound {operation} that represents the logical union of this {operation} and the {{@code~other}} {operation}.",
                )
                lmbd = f"{par_a_text} ->${mthd}({a_text}) || other.{mthd}({a_text})"

                imports.add("java.util.Objects")
                instance_methods["or"] = mdoc + [
                    f"    default {name}{p_text} or(",
                    f"        final {name}{var_p_text} other)",
                    r"    {",
                    r"        Objects.requireNonNull(other);",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

                # negated (predicate)
                mdoc = javadoc(
                    f"Returns {aan(operation)} {operation} that represents the logical negation of this {operation}.",
                    indent=4,
                    result=f"{Aan(operation)} {operation} that represents the logical negation of this {operation}.",
                )
                lmbd = f"{par_a_text} ->$!{mthd}({a_text})"

                instance_methods["negated"] = mdoc + [
                    f"    default {name}{p_text} negated()",
                    r"    {",
                    f"        return {lmbd};".replace(
                        "$", (f"\n{' '*12}" if len(lmbd) > 64 else " ")
                    ),
                    r"    }",
                ]

            # print file
            if args.issubset({"object", "int", "long", "double"}) and ret in (
                "object",
                "int",
                "long",
                "double",
                "boolean",
                "void",
            ):
                package = base_pkg
            elif True in (a.endswith("[]") for a in argv):
                package = f"{base_pkg}.array"
            else:
                package = f"{base_pkg}.primitive"

            package_dir = os.path.join(*([base_dir] + package.split(".")))
            file_name = f"{name}.java"
            file_path = os.path.join(package_dir, file_name)

            os.makedirs(package_dir, exist_ok=True)

            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                print(
                    """/*
 * The MIT License
 *
 * Copyright 2022 David Kleszyk <dkleszyk@gmail.com>.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */""",
                    file=f,
                )

                print(f"package {package};", end="\n\n", file=f)

                if imports:
                    print(
                        *(f"import {i};" for i in sorted(imports)),
                        sep="\n",
                        end="\n\n",
                        file=f,
                    )

                if static_imports:
                    print(
                        *(f"import static {i};" for i in sorted(static_imports)),
                        sep="\n",
                        end="\n\n",
                        file=f,
                    )

                if argc == 0:
                    input = "no arguments"
                elif argc == 1:
                    if argv[0] == "object":
                        input = r"a single argument"
                    elif argv[0] == "object[]":
                        input = r"an array argument with start and end indices"
                    elif argv[0].endswith("[]"):
                        input = f"{aan(argv[0])} {{@code~{argv[0][:-2]}}}-valued array argument with start and end indices"
                    else:
                        input = f"a single {{@code~{argv[0]}}}-valued argument"
                elif len(args) == 1:
                    if argv[0] == "object":
                        input = f"{cnt_ordinals[argc]} arguments"
                    elif argv[0] == "object[]":
                        input = f"{cnt_ordinals[argc]} array arguments, each with start and end indices"
                    elif argv[0].endswith("[]"):
                        input = f"{cnt_ordinals[argc]} {{@code~{argv[0][:-2]}}}-valued array arguments, each with start and end indices"
                    else:
                        input = (
                            f"{cnt_ordinals[argc]} {{@code~{argv[0]}}}-valued arguments"
                        )
                else:
                    assert argc == 2
                    assert argv[0] == "object"
                    assert argv[1] != "object"
                    input = "an object-valued argument and "
                    if argv[1] == "object[]":
                        input += r"an array argument with start and end indices"
                    elif argv[1].endswith("[]"):
                        input += f"{aan(argv[1])} {{@code~{argv[1][:-2]}}}-valued array argument with start and end indices"
                    else:
                        input += f"{aan(argv[1])} {{@code~{argv[1]}}}-valued argument"

                if ret == "void":
                    output = "no result"
                elif ret == "object":
                    output = "a result"
                else:
                    output = f"{aan(ret)} {{@code~{ret}}}-valued result"

                print(
                    *javadoc(
                        f"Represents {aan(operation)} {operation} that takes {input} and produces {output}.",
                        parameters=((f"<{p}>", p_desc) for p, p_desc in p_list),
                        authors=("David Kleszyk <dkleszyk@gmail.com>",),
                        output_as_generator=True,
                    ),
                    sep="\n",
                    file=f,
                )

                print("@FunctionalInterface", file=f)
                print(f"public interface {name}{p_text}", file=f)
                print("{", file=f)

                all_methods = [static_methods[k] for k in sorted(static_methods)] + [
                    instance_methods[k] for k in sorted(instance_methods)
                ]

                for method in all_methods[:-1]:
                    print(*method, sep="\n", end="\n\n", file=f)
                for method in all_methods[-1:]:
                    print(*method, sep="\n", file=f)

                print("}", file=f)

print(*names, sep="\n")
print(f"Generated {len(names)} files.")
print(r"Done.")
