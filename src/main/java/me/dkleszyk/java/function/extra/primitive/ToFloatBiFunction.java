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

/**
 * Represents a function that takes two arguments and produces a
 * {@code float}-valued result.
 *
 * @author David Kleszyk <dkleszyk@gmail.com>
 *
 * @param <T> The type of the first argument to the function.
 * @param <U> The type of the second argument to the function.
 */
@FunctionalInterface
public interface ToFloatBiFunction<T, U>
{
    /**
     * Applies the function to the given arguments.
     *
     * @param t The first argument to the function.
     * @param u The second argument to the function.
     *
     * @return The result of the function.
     */
    float applyAsFloat(
        final T t,
        final U u);
}
