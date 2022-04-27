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
 * Represents a predicate that takes two {@code float}-valued arguments and
 * produces a {@code boolean}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 */
@FunctionalInterface
public interface FloatBiPredicate
{
    /**
     * Returns a compound predicate that represents the logical intersection of
     * this predicate and the given predicate. The compound predicate evaluates
     * this predicate first; the other predicate is not evaluated if the result
     * of this predicate is {@code false}.
     *
     * @param other A predicate to be intersected with this predicate.
     *
     * @return A compound predicate that represents the logical intersection of
     *         this predicate and the {@code other} predicate.
     */
    default FloatBiPredicate and(
        final FloatBiPredicate other)
    {
        Objects.requireNonNull(other);
        return (x, y) -> test(x, y) && other.test(x, y);
    }

    /**
     * Returns a predicate that represents the logical negation of this
     * predicate.
     *
     * @return A predicate that represents the logical negation of this
     *         predicate.
     */
    default FloatBiPredicate negated()
    {
        return (x, y) -> !test(x, y);
    }

    /**
     * Returns a compound predicate that represents the logical union of this
     * predicate and the given predicate. The compound predicate evaluates this
     * predicate first; the other predicate is not evaluated if the result of
     * this predicate is {@code true}.
     *
     * @param other A predicate to be unioned with this predicate.
     *
     * @return A compound predicate that represents the logical union of this
     *         predicate and the {@code other} predicate.
     */
    default FloatBiPredicate or(
        final FloatBiPredicate other)
    {
        Objects.requireNonNull(other);
        return (x, y) -> test(x, y) || other.test(x, y);
    }

    /**
     * Evaluates the predicate against the given arguments.
     *
     * @param left  The first argument to the predicate.
     * @param right The second argument to the predicate.
     *
     * @return A {@code true}-or-{@code false} value indicating whether the
     *         arguments match the predicate.
     */
    boolean test(
        final float left,
        final float right);
}
