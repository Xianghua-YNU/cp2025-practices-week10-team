import numpy as np
import matplotlib.pyplot as plt

def q3a(T):
    """
    计算 3-alpha 反应速率中与温度相关的部分 q / (rho^2 Y^3)
    输入: T - 温度 (K)
    返回: 速率因子 (erg * cm^6 / (g^3 * s))
    """
    T8 = T / 1.0e8  # 以 10^8 K 为单位
    # 避免 T8 过小导致除0或溢出错误
    if T8 <= 0:
        return 0.0
    rate_factor = 5.09e11 * T8**(-3.0) * np.exp(-44.027 / T8)
    return rate_factor

def plot_rate(filename="rate_vs_temp.png"):
    """绘制速率因子随温度变化的对数图"""
    T_values = np.logspace(np.log10(3.0e8), np.log10(5.0e9), 100) 
    q_values = [q3a(T) for T in T_values]

    fig, ax = plt.subplots()
    ax.loglog(T_values, q_values)
    ax.set_xlabel("Temperature T (K)")
    ax.set_ylabel(r"$q_{3\alpha}/(\rho^2 Y^3)$  (erg cm$^6$ g$^{-3}$ s$^{-1}$)")
    ax.set_title("3-α Reaction Rate Factor vs Temperature")
    ax.grid(True, which="both", ls=":") # show both major and minor grid lines
    #plt.savefig(filename)
    #print(f"图表已存至 {filename}")
    plt.show() 

if __name__ == "__main__":
    # 计算并输出nu值
    print("   温度 T (K)    :   ν (敏感性指数)")
    print("--------------------------------------")

    temperatures_K = [1.0e8, 2.5e8, 5.0e8, 1.0e9, 2.5e9, 5.0e9]
    h = 1.0e-8 # 加入微扰，差分微元

    for T0 in temperatures_K:
        q_T0 = q3a(T0)
        if q_T0 == 0: # 避免除以0
            nu = np.nan # Not a Number
        else:
            delta_T = h * T0
            q_T0_plus_deltaT = q3a(T0 + delta_T)
            
            # 使用前向差分计算 dq/dT近似值
            dq_dT_approx = (q_T0_plus_deltaT - q_T0) / delta_T
            
            # 计算 nu
            nu = (T0 / q_T0) * dq_dT_approx
            
        # 格式化输出
        print(f"  {T0:10.3e} K : {nu:8.3f}")

    plot_rate()
