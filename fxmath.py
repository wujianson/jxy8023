# 全局常量
dx = 1e-12

# 1. 四舍五入函数
def fofi(f, n):
    if n >= 0:
        shift = 10 ** n
        temp = f * shift
        if temp >= 0:
            rounded = int(temp + 0.5)
        else:
            rounded = int(temp - 0.5)
        return rounded / shift
    else:
        shift = 10 ** (-n)
        temp = f / shift
        if temp >= 0:
            rounded = int(temp + 0.5)
        else:
            rounded = int(temp - 0.5)
        return rounded * shift

# 2. 阶乘函数
def rd(maxnum):
    if maxnum < 0:
        return None
    result = 1
    for i in range(1, maxnum + 1):
        result *= i
    return result

# 3. 幂函数
def nfx(x, n):
    if n == 0:
        return 1
    if x == 0:
        return 0
    if n < 0:
        return 1 / nfx(x, -n)
    result = 1
    for _ in range(n):
        result *= x
    return result

# 4. 平方根函数（二分法）
def sqr(x=2, n=2):
    if x < 0 or n <= 0:
        return None
    low, high = 0, max(1, x)
    while high - low > dx:
        mid = (low + high) / 2
        mid_val = nfx(mid, n)
        if mid_val < x:
            low = mid
        else:
            high = mid
    return (low + high) / 2

# 5. 自然对数底e（泰勒展开）
def e():
    result = 1
    term = 1
    n = 1
    while term > dx:
        term /= n
        result += term
        n += 1
    return result

# 6. 圆周率pi（反正切级数）
def pi():
    pi_val = 0
    k = 0
    term = 1
    while abs(term) > dx:
        term = 4 * (-1)**k / (2*k + 1)
        pi_val += term
        k += 1
    return pi_val

# 7. 表达式生成函数
def rofofi(f):
    return f"√{f}"

# 8. 三角函数辅助函数（角度转弧度）
def to_radians(x, typ):
    if typ == 'd':  # 角度
        return x * pi() / 180
    elif typ == 'g':  # 百分度
        return x * pi() / 200
    else:  # 弧度
        return x

# 9. 正弦函数
def sinf(x, typ='r'):
    x_rad = to_radians(x, typ)
    result = 0
    term = x_rad
    n = 1
    while abs(term) > dx:
        result += term
        term = term * (-x_rad * x_rad) / ((2 * n) * (2 * n + 1))
        n += 1
    return result

# 10. 余弦函数
def cosf(x, typ='r'):
    x_rad = to_radians(x, typ)
    result = 0
    term = 1
    n = 1
    while abs(term) > dx:
        result += term
        term = term * (-x_rad * x_rad) / ((2 * n - 1) * (2 * n))
        n += 1
    return result

# 11. 正切函数
def tanf(x, typ='r'):
    s = sinf(x, typ)
    c = cosf(x, typ)
    if abs(c) < dx:
        return None
    return s / c

# 12. 指数函数
def ex(x, a=None):
    if a is None:
        a = e()
    result = 1
    term = 1
    n = 1
    while abs(term) > dx:
        term *= x * nfx(a, -1)
        result += term
        n += 1
    return result

# 13. 反函数辅助函数（二分法）
def inverse(func, y, typ='r', a=-1e308, b=1e308):
    while b - a > dx:
        mid = (a + b) / 2
        mid_val = func(mid, typ)
        if mid_val < y:
            a = mid
        else:
            b = mid
    return (a + b) / 2

# 14. 反正弦函数
def asinf(y, typ='r'):
    return inverse(sinf, y, typ, -pi()/2, pi()/2)

# 15. 反余弦函数
def acosf(y, typ='r'):
    return pi()/2 - asinf(y, typ)

# 16. 反正切函数
def atanf(y, typ='r'):
    return inverse(tanf, y, typ, -pi()/2, pi()/2)

# 17. 自然对数函数
def lnf(x):
    return inverse(ex, x, 'r', 0, 1e308)

# 18. 微分函数
def df(fx, limx, h=dx):
    return (fx(limx + h) - fx(limx - h)) / (2 * h)

# 19. 积分函数
def sf(fx, min_val, max_val, h=dx):
    total = 0
    x = min_val
    while x < max_val:
        total += fx(x) * h
        x += h
    return total

# 20. 多阶微积分函数
def nds(typ, fx, t=1, limx=None, min_val=None, max_val=None, h=dx):
    if typ == 'df':
        if t == 1:
            return df(fx, limx, h)
        else:
            def dfx(x):
                return nds('df', fx, t-1, limx=x, h=h)
            return df(dfx, limx, h)
    elif typ == 'sf':
        if t == 1:
            return sf(fx, min_val, max_val, h)
        else:
            def sfx(x):
                return nds('sf', fx, t-1, min_val=min_val, max_val=x, h=h)
            return sf(sfx, min_val, max_val, h)
    return None

# 21. 求和函数
def ad(lis=[], func=None, max_val=None, min_val=None, h=1):
    if lis:
        return sum(lis)
    total = 0
    x = min_val
    while x <= max_val:
        total += func(x)
        x += h
    return total

# 22. 求积函数
def xd(lis=[], func=None, max_val=None, min_val=None, h=1):
    if lis:
        result = 1
        for num in lis:
            result *= num
        return result
    result = 1
    x = min_val
    while x <= max_val:
        result *= func(x)
        x += h
    return result

# 23. 方程求解（二分法）
def ffx(fx, fy, a=-1e308, b=1e308):
    def F(x):
        return fx(x) - fy(x)
    
    while b - a > dx:
        mid = (a + b) / 2
        if F(mid) == 0:
            return mid
        if F(a) * F(mid) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

# 24. 常微分方程求解（欧拉法）
def dfx(fx, fy, min_val, max_val, h=dx):
    result = []
    y = 0  # 初始值
    x = min_val
    while x <= max_val:
        result.append((x, y))
        dydx = fx(x, y)  # dy/dx = f(x,y)
        y += dydx * h
        x += h
    return result

# 25. 参数估计函数
def dfc(fx, fy, min_val, max_val, h=dx):
    # 简化的参数估计实现
    best_c = None
    min_error = float('inf')
    for c in range(-100, 101):  # 假设参数范围
        error = 0
        x = min_val
        while x <= max_val:
            error += abs(fx(x, c) - fy(x))
            x += h
        if error < min_error:
            min_error = error
            best_c = c
    return best_c

# 定义常数
e = e()
pi = pi()

