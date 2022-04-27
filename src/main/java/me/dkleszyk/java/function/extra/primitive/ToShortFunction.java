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
import java.util.function.Function;

/**
 * Represents a function that takes a single argument and produces a
 * {@code short}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 *
 * @param <T> The type of the argument to the function.
 */
@FunctionalInterface
public interface ToShortFunction<T>
{
    /**
     * Applies the function to the given argument.
     *
     * @param t The argument to the function.
     *
     * @return The result of the function.
     */
    short applyAsShort(
        final T t);

    /**
     * Returns a compound function that first applies the given function to its
     * input argument and then applies this function to produce a transformed
     * result.
     *
     * @param <U>    The type of the input to the compound function.
     * @param before A function to apply to produce the input to this function.
     *
     * @return A compound function that first applies the {@code before}
     *         function and then applies this function.
     */
    default <U> ToShortFunction<U> compose(
        final Function<? super U, ? extends T> before)
    {
        Objects.requireNonNull(before);
        return t -> applyAsShort(before.apply(t));
    }
}
