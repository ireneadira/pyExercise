var maxDigits, ZERO_ARRAY, bigZero, bigOne, biRadixBase = 2,
    biRadixBits = 16,
    bitsPerDigit = biRadixBits,
    biRadix = 65536,
    biHalfRadix = biRadix >>> 1,
    biRadixSquared = biRadix * biRadix,
    maxDigitVal = biRadix - 1,
    maxInteger = 9999999999999998;

function setMaxDigits(e) {
    ZERO_ARRAY = new Array(maxDigits = e);
    for (var i = 0; i < ZERO_ARRAY.length; i++)
        ZERO_ARRAY[i] = 0;
    bigZero = new BigInt, (bigOne = new BigInt).digits[0] = 1
}
setMaxDigits(20);
var dpl10 = 15,
    lr10 = biFromNumber(1e15);

function BigInt(e) {
    this.digits = "boolean" == typeof e && 1 == e ? null : ZERO_ARRAY.slice(0),
        this.isNeg = !1
}

function biFromDecimal(e) {
    for (var i, t = "-" == e.charAt(0), r = t ? 1 : 0; r < e.length && "0" == e.charAt(r);)
    ++r;
    if (r == e.length)
        i = new BigInt;
    else {
        var a = (e.length - r) % dpl10;
        for (0 == a && (a = dpl10),
            i = biFromNumber(Number(e.substr(r, a))),
            r += a; r < e.length;)
            i = biAdd(biMultiply(i, lr10), biFromNumber(Number(e.substr(r, dpl10)))),
            r += dpl10;
        i.isNeg = t
    }
    return i
}

function biCopy(e) {
    var i = new BigInt(!0);
    return i.digits = e.digits.slice(0),
        i.isNeg = e.isNeg,
        i
}

function biFromNumber(e) {
    var i = new BigInt;
    i.isNeg = e < 0,
        e = Math.abs(e);
    for (var t = 0; 0 < e;)
        i.digits[t++] = e & maxDigitVal,
        e = Math.floor(e / biRadix);
    return i
}

function reverseStr(e) {
    for (var i = "", t = e.length - 1; - 1 < t; --t)
        i += e.charAt(t);
    return i
}
var hexatrigesimalToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z");

function biToString(e, i) {
    var t = new BigInt;
    t.digits[0] = i;
    for (var r = biDivideModulo(e, t), a = hexatrigesimalToChar[r[1].digits[0]]; 1 == biCompare(r[0], bigZero);)
        r = biDivideModulo(r[0], t),
        digit = r[1].digits[0],
        a += hexatrigesimalToChar[r[1].digits[0]];
    return (e.isNeg ? "-" : "") + reverseStr(a)
}

function biToDecimal(e) {
    var i = new BigInt;
    i.digits[0] = 10;
    for (var t = biDivideModulo(e, i), r = String(t[1].digits[0]); 1 == biCompare(t[0], bigZero);)
        t = biDivideModulo(t[0], i),
        r += String(t[1].digits[0]);
    return (e.isNeg ? "-" : "") + reverseStr(r)
}
var hexToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f");

function digitToHex(e) {
    var t = "";
    for (i = 0; i < 4; ++i)
        t += hexToChar[15 & e],
        e >>>= 4;
    return reverseStr(t)
}

function biToHex(e) {
    for (var i = "", t = (biHighIndex(e),
        biHighIndex(e)); - 1 < t; --t)
        i += digitToHex(e.digits[t]);
    return i
}

function charToHex(e) {
    return e = 48 <= e && e <= 57 ? e - 48 : 65 <= e && e <= 90 ? 10 + e - 65 : 97 <= e && e <= 122 ? 10 + e - 97 : 0
}

function hexToDigit(e) {
    for (var i = 0, t = Math.min(e.length, 4), r = 0; r < t; ++r)
        i <<= 4,
        i |= charToHex(e.charCodeAt(r));
    return i
}

function biFromHex(e) {
    for (var i = new BigInt, t = e.length, r = 0; 0 < t; t -= 4,
        ++r)
        i.digits[r] = hexToDigit(e.substr(Math.max(t - 4, 0), Math.min(t, 4)));
    return i
}

function biFromString(e, i) {
    var t = "-" == e.charAt(0),
        r = t ? 1 : 0,
        a = new BigInt;
    (n = new BigInt).digits[0] = 1;
    for (var o = e.length - 1; r <= o; o--)
        var a = biAdd(a, biMultiplyDigit(n, charToHex(e.charCodeAt(o)))),
            n = biMultiplyDigit(n, i);
    return a.isNeg = t,
        a
}

function biDump(e) {
    return (e.isNeg ? "-" : "") + e.digits.join(" ")
}

function biAdd(e, i) {
    if (e.isNeg != i.isNeg)
        i.isNeg = !i.isNeg,
        r = biSubtract(e, i),
        i.isNeg = !i.isNeg;
    else {
        for (var t, r = new BigInt, a = 0, o = 0; o < e.digits.length; ++o)
            t = e.digits[o] + i.digits[o] + a,
            r.digits[o] = t % biRadix,
            a = Number(biRadix <= t);
        r.isNeg = e.isNeg
    }
    return r
}

function biSubtract(e, i) {
    if (e.isNeg != i.isNeg)
        i.isNeg = !i.isNeg,
        r = biAdd(e, i),
        i.isNeg = !i.isNeg;
    else {
        for (var t, r = new BigInt, a = o = 0; a < e.digits.length; ++a)
            t = e.digits[a] - i.digits[a] + o,
            r.digits[a] = t % biRadix,
            r.digits[a] < 0 && (r.digits[a] += biRadix),
            o = 0 - Number(t < 0);
        if (-1 == o) {
            for (var o = 0, a = 0; a < e.digits.length; ++a)
                t = 0 - r.digits[a] + o,
                r.digits[a] = t % biRadix,
                r.digits[a] < 0 && (r.digits[a] += biRadix),
                o = 0 - Number(t < 0);
            r.isNeg = !e.isNeg
        } else
            r.isNeg = e.isNeg
    }
    return r
}

function biHighIndex(e) {
    for (var i = e.digits.length - 1; 0 < i && 0 == e.digits[i];)
    --i;
    return i
}

function biNumBits(e) {
    for (var i = biHighIndex(e), t = e.digits[i], r = (i + 1) * bitsPerDigit, a = r; r - bitsPerDigit < a && 0 == (32768 & t); --a)
        t <<= 1;
    return a
}

function biMultiply(e, i) {
    for (var t, r, a, o = new BigInt, n = biHighIndex(e), s = biHighIndex(i), d = 0; d <= s; ++d) {
        for (a = d,
            j = t = 0; j <= n; ++j,
            ++a)
            r = o.digits[a] + e.digits[j] * i.digits[d] + t,
            o.digits[a] = r & maxDigitVal,
            t = r >>> biRadixBits;
        o.digits[d + n + 1] = t
    }
    return o.isNeg = e.isNeg != i.isNeg,
        o
}

function biMultiplyDigit(e, i) {
    var t;
    result = new BigInt;
    for (var r = biHighIndex(e), a = 0, o = 0; o <= r; ++o)
        t = result.digits[o] + e.digits[o] * i + a,
        result.digits[o] = t & maxDigitVal,
        a = t >>> biRadixBits;
    return result.digits[1 + r] = a,
        result
}

function arrayCopy(e, i, t, r, a) {
    for (var o = Math.min(i + a, e.length), n = i, s = r; n < o; ++n,
        ++s)
        t[s] = e[n]
}
var highBitMasks = new Array(0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535);

function biShiftLeft(e, i) {
    var t = Math.floor(i / bitsPerDigit),
        r = new BigInt;
    arrayCopy(e.digits, 0, r.digits, t, r.digits.length - t);
    for (var a = i % bitsPerDigit, o = bitsPerDigit - a, n = r.digits.length - 1, s = n - 1; 0 < n; --n,
        --s)
        r.digits[n] = r.digits[n] << a & maxDigitVal | (r.digits[s] & highBitMasks[a]) >>> o;
    return r.digits[0] = r.digits[n] << a & maxDigitVal,
        r.isNeg = e.isNeg,
        r
}
var lowBitMasks = new Array(0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535);

function biShiftRight(e, i) {
    var t = Math.floor(i / bitsPerDigit),
        r = new BigInt;
    arrayCopy(e.digits, t, r.digits, 0, e.digits.length - t);
    for (var a = i % bitsPerDigit, o = bitsPerDigit - a, n = 0, s = n + 1; n < r.digits.length - 1; ++n,
        ++s)
        r.digits[n] = r.digits[n] >>> a | (r.digits[s] & lowBitMasks[a]) << o;
    return r.digits[r.digits.length - 1] >>>= a,
        r.isNeg = e.isNeg,
        r
}

function biMultiplyByRadixPower(e, i) {
    var t = new BigInt;
    return arrayCopy(e.digits, 0, t.digits, i, t.digits.length - i),
        t
}

function biDivideByRadixPower(e, i) {
    var t = new BigInt;
    return arrayCopy(e.digits, i, t.digits, 0, t.digits.length - i),
        t
}

function biModuloByRadixPower(e, i) {
    var t = new BigInt;
    return arrayCopy(e.digits, 0, t.digits, 0, i),
        t
}

function biCompare(e, i) {
    if (e.isNeg != i.isNeg)
        return 1 - 2 * Number(e.isNeg);
    for (var t = e.digits.length - 1; 0 <= t; --t)
        if (e.digits[t] != i.digits[t])
            return e.isNeg ? 1 - 2 * Number(e.digits[t] > i.digits[t]) : 1 - 2 * Number(e.digits[t] < i.digits[t]);
    return 0
}

function biDivideModulo(e, i) {
    var t = biNumBits(e),
        r = biNumBits(i),
        a = i.isNeg;
    if (t < r)
        return e.isNeg ? ((o = biCopy(bigOne)).isNeg = !i.isNeg,
                e.isNeg = !1,
                i.isNeg = !1,
                n = biSubtract(i, e),
                e.isNeg = !0,
                i.isNeg = a) : (o = new BigInt,
                n = biCopy(e)),
            new Array(o, n);
    for (var o = new BigInt, n = e, s = Math.ceil(r / bitsPerDigit) - 1, d = 0; i.digits[s] < biHalfRadix;)
        i = biShiftLeft(i, 1),
        ++d,
        ++r,
        s = Math.ceil(r / bitsPerDigit) - 1;
    n = biShiftLeft(n, d),
        t += d;
    for (var l = Math.ceil(t / bitsPerDigit) - 1, m = biMultiplyByRadixPower(i, l - s); - 1 != biCompare(n, m);)
    ++o.digits[l - s],
        n = biSubtract(n, m);
    for (var c = l; s < c; --c) {
        var u = c >= n.digits.length ? 0 : n.digits[c],
            g = c - 1 >= n.digits.length ? 0 : n.digits[c - 1],
            h = c - 2 >= n.digits.length ? 0 : n.digits[c - 2],
            p = s >= i.digits.length ? 0 : i.digits[s],
            b = s - 1 >= i.digits.length ? 0 : i.digits[s - 1];
        o.digits[c - s - 1] = u == p ? maxDigitVal : Math.floor((u * biRadix + g) / p);
        for (var f = o.digits[c - s - 1] * (p * biRadix + b), N = u * biRadixSquared + (g * biRadix + h); N < f;)
        --o.digits[c - s - 1],
            f = o.digits[c - s - 1] * (p * biRadix | b),
            N = u * biRadix * biRadix + (g * biRadix + h);
        (n = biSubtract(n, biMultiplyDigit(m = biMultiplyByRadixPower(i, c - s - 1), o.digits[c - s - 1]))).isNeg && (n = biAdd(n, m),
            --o.digits[c - s - 1])
    }
    return n = biShiftRight(n, d),
        o.isNeg = e.isNeg != a,
        e.isNeg && (o = (a ? biAdd : biSubtract)(o, bigOne),
            n = biSubtract(i = biShiftRight(i, d), n)),
        0 == n.digits[0] && 0 == biHighIndex(n) && (n.isNeg = !1),
        new Array(o, n)
}

function biDivide(e, i) {
    return biDivideModulo(e, i)[0]
}

function biModulo(e, i) {
    return biDivideModulo(e, i)[1]
}

function biMultiplyMod(e, i, t) {
    return biModulo(biMultiply(e, i), t)
}

function biPow(e, i) {
    for (var t = bigOne, r = e; 0 != (1 & i) && (t = biMultiply(t, r)),
        0 != (i >>= 1);)
        r = biMultiply(r, r);
    return t
}

function biPowMod(e, i, t) {
    for (var r = bigOne, a = e, o = i; 0 != (1 & o.digits[0]) && (r = biMultiplyMod(r, a, t)),
        0 != (o = biShiftRight(o, 1)).digits[0] || 0 != biHighIndex(o);)
        a = biMultiplyMod(a, a, t);
    return r
}

function BarrettMu(e) {
    this.modulus = biCopy(e),
        this.k = biHighIndex(this.modulus) + 1, (e = new BigInt).digits[2 * this.k] = 1,
        this.mu = biDivide(e, this.modulus),
        this.bkplus1 = new BigInt,
        this.bkplus1.digits[this.k + 1] = 1,
        this.modulo = BarrettMu_modulo,
        this.multiplyMod = BarrettMu_multiplyMod,
        this.powMod = BarrettMu_powMod
}

function BarrettMu_modulo(e) {
    for (var i = biDivideByRadixPower(e, this.k - 1), i = biDivideByRadixPower(biMultiply(i, this.mu), this.k + 1), t = biSubtract(biModuloByRadixPower(e, this.k + 1), biModuloByRadixPower(biMultiply(i, this.modulus), this.k + 1)), r = 0 <= biCompare(t = t.isNeg ? biAdd(t, this.bkplus1) : t, this.modulus); r;)
        r = 0 <= biCompare(t = biSubtract(t, this.modulus), this.modulus);
    return t
}

function BarrettMu_multiplyMod(e, i) {
    return i = biMultiply(e, i),
        this.modulo(i)
}

function BarrettMu_powMod(e, i) {
    var t = new BigInt;
    t.digits[0] = 1;
    for (var r = e, a = i; 0 != (1 & a.digits[0]) && (t = this.multiplyMod(t, r)),
        0 != (a = biShiftRight(a, 1)).digits[0] || 0 != biHighIndex(a);)
        r = this.multiplyMod(r, r);
    return t
}

function RSAKeyPair(e, i, t) {
    this.e = biFromHex(e),
        this.d = biFromHex(i),
        this.m = biFromHex(t),
        this.chunkSize = 2 * biHighIndex(this.m),
        this.radix = 16,
        this.barrett = new BarrettMu(this.m)
}

function twoDigit(e) {
    return (e < 10 ? "0" : "") + String(e)
}

function encryptedString(e, i) {
    for (var t = new Array, r = i.length, a = 0; a < r;)
        t[a] = i.charCodeAt(a),
        a++;
    for (; t.length % e.chunkSize != 0;)
        t[a++] = 0;
    for (var o, n, s, d = t.length, l = "", a = 0; a < d; a += e.chunkSize) {
        for (s = new BigInt,
            o = 0,
            n = a; n < a + e.chunkSize; ++o)
            s.digits[o] = t[n++],
            s.digits[o] += t[n++] << 8;
        var m = e.barrett.powMod(s, e.e);
        l += (16 == e.radix ? biToHex(m) : biToString(m, e.radix)) + " "
    }
    return l.substring(0, l.length - 1)
}

function decryptedString(e, i) {
    for (var t = i.split(" "), r = "", a = 0; a < t.length; ++a)
        for (var o = 16 == e.radix ? biFromHex(t[a]) : biFromString(t[a], e.radix), n = e.barrett.powMod(o, e.d), s = 0; s <= biHighIndex(n); ++s)
            r += String.fromCharCode(255 & n.digits[s], n.digits[s] >> 8);
    return 0 == r.charCodeAt(r.length - 1) ? r.substring(0, r.length - 1) : r
}

function encryptpassword(e) {
    return setMaxDigits(130),
        key = new RSAKeyPair("10001", "", "b1ce915a21d373a31640728c7a1f00badfeb4f0884299e05a8f5c921e627c59bcedd94743a231182f387183aaa961943701ae1af732d7792156e89707d27b06b"),
        encryptedString(key, e)
}