import collections

def pow_mod(x, n, m):
    '''xのn乗 mod m を求める
    '''
    _x = 1
    for i in range(1, n+1):
        _x = (x*_x)% m
    return _x

def gyakusu(x, m):
    '''
    mを法としたときのx^(-1)を求める
    x x^(-1) ≡ 1 (mod m)
    '''
    right=1
    while(True):
        if right % x == 0:
            break
        else:
            right+=m
    return int(right/x)

def pohlig(p, g, y, q, bb):
    '''log_g y (mod p)'''
    n = int((p-1) / q)
    mods = []
    q_gyaku = gyakusu(g, p)
    i=0
    x=0
    for i in range(q):
        mods.append(pow_mod(g, n*i, p))
    for j in range(bb):
        pow_y = pow_mod(y*(q_gyaku**x),int(n/(q**j)), p)
        for k in range(q):
            if pow_y == mods[k]:
                x+=k*(q**j)
    return x

def euler(num):
    ''' オイラー関数
    return: φ(num)
    '''
    cnt=0
    for i in range (1,num):
        if gcd(num,i)==1:
            cnt+=1
    return cnt

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def china(mods, rems):
    M = 1
    mod = 0
    eulers = []

    # オイラー関数の配列
    for m in mods:
        eulers.append(euler(m))
    for i in range(len(mods)):
        M *= mods[i]
    for j in range(len(mods)):
        mod += rems[j] * pow_mod((M/mods[j]), eulers[j], M)
    mod = int(mod % M)
    return mod

def prime_factorize(n):
    a = []
    while n % 2 == 0:
        a.append(2)
        n //= 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            a.append(f)
            n //= f
        else:
            f += 2
    if n != 1:
        a.append(n)
    return a

def pohlig_hellman(p, g, y):
    '''log_g y (mod p) を求める'''
    c = collections.Counter(prime_factorize(p-1))
    q = []
    r = []
    mods = []
    rems = []
    for _c in c.items():
        q.append(_c[0])
        r.append(_c[1])
        mods.append(_c[0]**_c[1])
    for i in range(len(q)):
        rem = pohlig(p, g, y, q[i], r[i])
        rems.append(rem)

    return china(mods, rems)

if __name__ == "__main__":
    p = 101
    g = 2
    y = 26
    print(pohlig_hellman(p, g, y))