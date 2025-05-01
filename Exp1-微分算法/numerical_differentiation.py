import numpy as np
import matplotlib.pyplot as plt
from sympy import tanh, symbols, diff, lambdify

def f(x):
    """计算函数值 f(x) = 1 + 0.5*tanh(2x)
    
    参数：
        x: 标量或numpy数组，输入值
    
    返回：
        标量或numpy数组，函数值
    """
    # TODO: 实现函数 f(x) = 1 + 0.5*tanh(2x)
    return 1 + 0.5 * np.tanh(2 * x)

def get_analytical_derivative():
    """使用sympy获取解析导数函数
    
    返回：
        可调用函数，用于计算导数值
    """
    # TODO: 使用sympy计算解析导数并返回可调用的函数
    x = symbols('x')
    return lambdify(x, diff(1 + 0.5 * tanh(2 * x), x))

def calculate_central_difference(x, f):
    """使用中心差分法计算数值导数
    
    参数：
        x: numpy数组，要计算导数的点
        f: 可调用函数，要求导的函数
    
    返回：
        numpy数组，x[1:-1]处的导数值
    """
    # TODO: 实现中心差分法计算导数
    h = x[1] - x[0]  # 假设均匀步长
    return (f(x[2:]) - f(x[:-2])) / (2 * h)

def richardson_derivative_all_orders(x, f, h, max_order=3):
    """使用Richardson外推法计算不同阶数的导数值
    
    参数：
        x: 标量，要计算导数的点
        f: 可调用函数，要求导的函数
        h: 浮点数，初始步长
        max_order: 整数，最大外推阶数
    
    返回：
        列表，不同阶数计算的导数值
    """
    # TODO: 实现Richardson外推法计算不同阶数的导数值
    R = np.zeros((max_order + 1, max_order + 1))
    
    for i in range(max_order + 1):
        hi = h / (2**i)
        R[i, 0] = (f(x + hi) - f(x - hi)) / (2 * hi)
    
    for j in range(1, max_order + 1):
        R[:-j, j] = (4**j * R[1:max_order-j+2, j-1] - R[:-j, j-1]) / (4**j - 1)
    
    return R[0, 1:max_order+1]

def create_comparison_plot(x, x_central, dy_central, dy_richardson, df_analytical):
    """创建对比图，展示导数计算结果和误差分析
    
    参数：
        x: numpy数组，所有x坐标点
        x_central: numpy数组，中心差分法使用的x坐标点
        dy_central: numpy数组，中心差分法计算的导数值
        dy_richardson: numpy数组，Richardson方法计算的导数值
        df_analytical: 可调用函数，解析导数函数
    """
    # 创建四个子图
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    analytical = df_analytical(x)
    analytical_central = df_analytical(x_central)
    
    # Plot 1: Derivative comparison
    axs[0,0].plot(x, analytical, 'b-', label='Analytical')
    axs[0,0].plot(x_central, dy_central, 'ro', ms=4, label='Central Difference')
    axs[0,0].plot(x, dy_richardson[:,1], 'g^', ms=4, label='Richardson (2nd)')
    axs[0,0].set(xlabel='x', ylabel='dy/dx', title='Derivative Comparison')
    axs[0,0].legend()
    
    # Plot 2: Error comparison
    errors = [
        np.abs(dy_central - analytical_central),
        np.abs(dy_richardson[:,1] - analytical)
    ]
    axs[0,1].plot(x_central, errors[0], 'ro', ms=4, label='Central Error')
    axs[0,1].plot(x, errors[1], 'g^', ms=4, label='Richardson Error')
    axs[0,1].set(yscale='log', xlabel='x', ylabel='Error', title='Error Analysis')
    axs[0,1].legend()

    for i, order in enumerate(['1st', '2nd', '3rd']):
        error = np.abs(dy_richardson[:,i] - analytical)
        axs[1,0].plot(x, error, marker='^', ms=4, label=f'Richardson {order}')
    axs[1,0].set(yscale='log', xlabel='x', ylabel='Error', title='Richardson Errors')
    axs[1,0].legend()
    
    # Plot 4: Step size sensitivity
    h_values = np.logspace(-6, -1, 20)
    x_test = 0.0
    expected = df_analytical(x_test)

def main():
    """运行数值微分实验的主函数"""
    h_initial = 0.1
    x = np.linspace(-2, 2, 200)
    df_analytical = get_analytical_derivative()
    
    dy_central = calculate_central_difference(x, f)
    x_central = x[1:-1]
    
    dy_richardson = np.array([richardson_derivative(xi, f, h_initial) for xi in x])
    
    plot_results(x, x_central, dy_central, dy_richardson, df_analytical)

if __name__ == '__main__':
    main()
