/*
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
 */
package me.dkleszyk.java.function.extra.primitive;

import java.util.Objects;

/**
 * Represents an operator that takes a single {@code short}-valued argument and
 * produces a {@code short}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 */
@FunctionalInterface
public interface ShortUnaryOperator
{
    /**
     * Returns an operator that always returns its input argument.
     *
     * @return An operator that always returns its input argument.
     */
    static ShortUnaryOperator identity()
    {
        return x -> x;
    }

    /**
     * Returns a compound operator that first applies this operator to its input
     * argument and then applies the given operator to produce a transformed
     * result.
     *
     * @param after An operator to apply to the result of this operator.
     *
     * @return A compound operator that first applies this operator and then
     *         applies the {@code after} operator.
     */
    default ShortUnaryOperator andThen(
        final ShortUnaryOperator after)
    {
        Objects.requireNonNull(after);
        return x -> after.applyAsShort(applyAsShort(x));
    }

    /**
     * Applies the operator to the given argument.
     *
     * @param operand The argument to the operator.
     *
     * @return The result of the operator.
     */
    short applyAsShort(
        final short operand);

    /**
     * Returns a compound operator that first applies the given operator to its
     * input argument and then applies this operator to produce a transformed
     * result.
     *
     * @param before An operator to apply to produce the input to this operator.
     *
     * @return A compound operator that first applies the {@code before}
     *         operator and then applies this operator.
     */
    default ShortUnaryOperator compose(
        final ShortUnaryOperator before)
    {
        Objects.requireNonNull(before);
        return x -> applyAsShort(before.applyAsShort(x));
    }
}
