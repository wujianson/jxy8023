# precompute.py
from fxmath import *  # 包含原始未优化的函数

# 计算100位精度的e和π（只需运行一次）
if __name__ == "__main__":
    print("计算中...请耐心等待（约1-5分钟）")
    high_precision_e = e()  # 调用原始泰勒展开
    high_precision_pi = pi()
    
    with open("constants.py", "w") as f:
        f.write(f"# 预计算常数（精度1e-100）\n")
        f.write(f"e = {high_precision_e}\n")
        f.write(f"pi = {high_precision_pi}\n")
    print("预计算完成！结果已保存到constants.py")
