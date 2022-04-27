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
package me.dkleszyk.java.function.extra.array;

import java.util.Objects;

/**
 * Represents a predicate that takes an object-valued argument and a
 * {@code char}-valued array argument with start and end indices and produces a
 * {@code boolean}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 *
 * @param <T> The type of the object-valued argument to the predicate.
 */
@FunctionalInterface
public interface ObjCharArraySegmentPredicate<T>
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
    default ObjCharArraySegmentPredicate<T> and(
        final ObjCharArraySegmentPredicate<? super T> other)
    {
        Objects.requireNonNull(other);
        return (obj, arr, from, to) ->
            test(obj, arr, from, to) && other.test(obj, arr, from, to);
    }

    /**
     * Returns a predicate that represents the logical negation of this
     * predicate.
     *
     * @return A predicate that represents the logical negation of this
     *         predicate.
     */
    default ObjCharArraySegmentPredicate<T> negated()
    {
        return (obj, arr, from, to) -> !test(obj, arr, from, to);
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
    default ObjCharArraySegmentPredicate<T> or(
        final ObjCharArraySegmentPredicate<? super T> other)
    {
        Objects.requireNonNull(other);
        return (obj, arr, from, to) ->
            test(obj, arr, from, to) || other.test(obj, arr, from, to);
    }

    /**
     * Evaluates the predicate against the given arguments.
     *
     * @param obj       The object-valued argument to the predicate.
     * @param array     The {@code char}-valued array argument to the predicate.
     * @param fromIndex The start index in {@code array}, inclusive.
     * @param toIndex   The end index in {@code array}, exclusive.
     *
     * @return A {@code true}-or-{@code false} value indicating whether the
     *         arguments match the predicate.
     */
    boolean test(
        final T obj,
        final char[] array,
        final int fromIndex,
        final int toIndex);
}
