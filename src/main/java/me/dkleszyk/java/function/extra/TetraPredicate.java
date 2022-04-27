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
package me.dkleszyk.java.function.extra;

import java.util.Objects;

/**
 * Represents a predicate that takes four arguments and produces a
 * {@code boolean}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 *
 * @param <T> The type of the first argument to the predicate.
 * @param <U> The type of the second argument to the predicate.
 * @param <V> The type of the third argument to the predicate.
 * @param <W> The type of the fourth argument to the predicate.
 */
@FunctionalInterface
public interface TetraPredicate<T, U, V, W>
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
    default TetraPredicate<T, U, V, W> and(
        final TetraPredicate<? super T, ? super U, ? super V, ? super W> other)
    {
        Objects.requireNonNull(other);
        return (t, u, v, w) -> test(t, u, v, w) && other.test(t, u, v, w);
    }

    /**
     * Returns a predicate that represents the logical negation of this
     * predicate.
     *
     * @return A predicate that represents the logical negation of this
     *         predicate.
     */
    default TetraPredicate<T, U, V, W> negated()
    {
        return (t, u, v, w) -> !test(t, u, v, w);
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
    default TetraPredicate<T, U, V, W> or(
        final TetraPredicate<? super T, ? super U, ? super V, ? super W> other)
    {
        Objects.requireNonNull(other);
        return (t, u, v, w) -> test(t, u, v, w) || other.test(t, u, v, w);
    }

    /**
     * Evaluates the predicate against the given arguments.
     *
     * @param t The first argument to the predicate.
     * @param u The second argument to the predicate.
     * @param v The third argument to the predicate.
     * @param w The fourth argument to the predicate.
     *
     * @return A {@code true}-or-{@code false} value indicating whether the
     *         arguments match the predicate.
     */
    boolean test(
        final T t,
        final U u,
        final V v,
        final W w);
}
