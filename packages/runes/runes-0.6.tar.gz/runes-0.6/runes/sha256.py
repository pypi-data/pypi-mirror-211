#!/usr/bin/python
# Copied from https://github.com/thomdixon/pysha2/blob/master/sha2/sha256.py
# Modified for modern python3
# MIT license

__author__ = 'Thomas Dixon'
__license__ = 'MIT'

import copy
import sys

class sha256(object):
    _k = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
          0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
          0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
          0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
          0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
          0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
          0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
          0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
          0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
          0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
          0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
          0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
          0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
          0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
          0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
          0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)
    _output_size = 8
    
    blocksize = 1
    block_size = 64
    digest_size = 32
    
    def __init__(self, m=None):        
        self._buffer = bytes(0)
        self._counter = 0
        self._h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                   0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

        if m is not None:
            if type(m) is not bytes:
                raise TypeError('__init__ argument 1 must be bytes, not {}'.format(type(m)))
            self.update(m)
        
    def _rotr(self, x, y):
        return ((x >> y) | (x << (32-y))) & 0xFFFFFFFF
                    
    def _sha256_process(self, c):
        w = [0]*64
        # Initialize the first 16 words to the buffer.
        w[0:16] = [int.from_bytes(c[i*4:(i+1)*4], 'big') for i in range(16)]
        
        for i in range(16, 64):
            s0 = self._rotr(w[i-15], 7) ^ self._rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = self._rotr(w[i-2], 17) ^ self._rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF
        
        a,b,c,d,e,f,g,h = self._h
        
        for i in range(64):
            s0 = self._rotr(a, 2) ^ self._rotr(a, 13) ^ self._rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = s0 + maj
            s1 = self._rotr(e, 6) ^ self._rotr(e, 11) ^ self._rotr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            t1 = h + s1 + ch + self._k[i] + w[i]
            
            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF
            
        self._h = [(x+y) & 0xFFFFFFFF for x,y in zip(self._h, [a,b,c,d,e,f,g,h])]
        
    def update(self, m):
        if not m:
            return
        if type(m) is not bytes:
            raise TypeError('update argument 1 must be bytes, not {}'.format(type(m)))
        
        self._buffer += m
        self._counter += len(m)
        
        while len(self._buffer) >= 64:
            self._sha256_process(self._buffer[:64])
            self._buffer = self._buffer[64:]

    def set_midstate(self, midstate: bytes):
        if len(midstate) != 32:
            raise ValueError("midstate must be 32 bytes")
        self._h = [int.from_bytes(midstate[i:i+4], 'big') for i in range(0, 32, 4)]

    def midstate(self):
        return b''.join([i.to_bytes(4, 'big') for i in self._h])

    def digest(self):
        mdi = self._counter & 0x3F
        length = (self._counter << 3).to_bytes(8, 'big')
        
        if mdi < 56:
            padlen = 55-mdi
        else:
            padlen = 119-mdi
        
        r = self.copy()
        r.update(bytes([0x80]) + bytes(padlen) +length)
        return r.midstate()

    def hexdigest(self):
        return self.digest().encode('hex')
        
    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if isinstance(other, sha256):
            return (self._h == other._h and 
                    self._counter == other._counter and 
                    self._buffer == other._buffer)
        return False        
