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
import java.util.function.Function;

/**
 * Represents a function that takes a {@code byte}-valued array argument with
 * start and end indices and produces a result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 *
 * @param <R> The type of the result of the function.
 */
@FunctionalInterface
public interface ByteArraySegmentFunction<R>
{
    /**
     * Returns a compound function that first applies this function to its input
     * arguments and then applies the given function to produce a transformed
     * result.
     *
     * @param <S>   The type of the result of the compound function.
     * @param after A function to apply to the result of this function.
     *
     * @return A compound function that first applies this function and then
     *         applies the {@code after} function.
     */
    default <S> ByteArraySegmentFunction<S> andThen(
        final Function<? super R, ? extends S> after)
    {
        Objects.requireNonNull(after);
        return (arr, from, to) -> after.apply(apply(arr, from, to));
    }

    /**
     * Applies the function to the given arguments.
     *
     * @param array     The array argument to the function.
     * @param fromIndex The start index in {@code array}, inclusive.
     * @param toIndex   The end index in {@code array}, exclusive.
     *
     * @return The result of the function.
     */
    R apply(
        final byte[] array,
        final int fromIndex,
        final int toIndex);
}
