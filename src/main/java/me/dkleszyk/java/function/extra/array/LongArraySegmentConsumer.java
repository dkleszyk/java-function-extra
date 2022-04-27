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
 * Represents an operation that takes a {@code long}-valued array argument with
 * start and end indices and produces no result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 */
@FunctionalInterface
public interface LongArraySegmentConsumer
{
    /**
     * Performs the operation using the given arguments.
     *
     * @param array     The array argument to the operation.
     * @param fromIndex The start index in {@code array}, inclusive.
     * @param toIndex   The end index in {@code array}, exclusive.
     */
    void accept(
        final long[] array,
        final int fromIndex,
        final int toIndex);

    /**
     * Returns a compound operation that first performs this operation using its
     * input arguments and then performs the given operation using those same
     * arguments.
     *
     * @param after The operation to perform after this operation.
     *
     * @return A compound operation that first performs this operation and then
     *         performs the {@code after} operation.
     */
    default LongArraySegmentConsumer andThen(
        final LongArraySegmentConsumer after)
    {
        Objects.requireNonNull(after);
        return (arr, from, to) ->
        {
            accept(arr, from, to);
            after.accept(arr, from, to);
        };
    }
}
