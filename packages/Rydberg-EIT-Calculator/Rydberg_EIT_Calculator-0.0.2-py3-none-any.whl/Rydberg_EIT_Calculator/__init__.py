from qutip import *
import numpy as np
import matplotlib.pyplot as plt
# import mpl_interactions.ipyplot as iplt
from scipy.stats import binom
from sklearn.svm import SVC
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
# from scipy.constants import *


def sum_of_binom(N1: int, p1, N2: int, p2):
    # return sum_dist: 0, 1, 2, ..., N1 + N2
    sum_dist = []
    for t in range(N1 + N2 + 1):
        pr = 0
        for x in range(t + 1):
            pr += binom.pmf(x, N1, p1) * binom.pmf(t - x, N2, p2)
        sum_dist.append(pr)
    return sum_dist  # list of probabilities


def ave_decay(N: int, p1, p2, d_rate):  # d_rate: decay probability per photon
    # d_rate = (decay prob./s) / (photon number/s)
    # the system start with distribution 1, N = N1 + N2
    dist_list = []
    for d in range(N):
        dist_list.append(sum_of_binom(d, p1, N - d, p2))
    ave_dist = np.average(dist_list, axis=0)
    # return np.array
    return ave_dist * N * d_rate + np.array([binom.pmf(x, N, p1) for x in range(N + 1)]) * (1 - N * d_rate)


def distgsh(dist0, dist1, norm=100):  # number of sample points = norm * probability[n]
    '''
    N: total photon number
    dist0: distribution under opacity
    dist1: distribution under transparency
    '''
    assert dist0.shape == dist1.shape
    # construct training data
    N = dist0.size - 1 # total photon number
    train_set = np.array([[0, 0]])
    for n in range(N + 1):  # 0, 1, 2, ..., N
        set0 = np.array([[0, n] for _ in range(int(norm * dist0[n]))])
        set1 = np.array([[1, n] for _ in range(int(norm * dist1[n]))])
        if set0.shape != (0,):
            train_set = np.concatenate((train_set, set0))
        if set1.shape != (0,):
            train_set = np.concatenate((train_set, set1))
    train_set = np.delete(train_set, obj=0, axis=0)
    y = train_set[:, 0]
    X = np.delete(train_set, obj=0, axis=1)
    clf = SVC(kernel='linear')
    clf.fit(X, y)
    return clf, clf.score(X, y)


def draw_dist(N=50, p1=0.3, p2=0.7, d_rate=0.01, select=0):  # probability per photon = decay rate / photon rate
    print('drawing distribution...')
    ave_dist = ave_decay(N, p1, p2, d_rate)
    transp_dist = np.array([binom.pmf(x, N, p2) for x in range(N + 1)])
    clf, score = distgsh(dist0=ave_dist, dist1=transp_dist)
    i = 0
    for i in range(N):
        if clf.predict([[i]])[0] < clf.predict([[i + 1]])[0]:
            break
    x = np.linspace(0, N, N + 1)
    plt.figure(figsize=(10, 8))
    plt.plot(x, ave_dist, 'bo', ms=10, label='opaque')
    plt.plot(x, transp_dist, 'ro', ms=10, label='transparent')
    plt.vlines(i, 0, max(transp_dist), colors='g', lw=5, label='decision line')
    plt.legend(fontsize=10)
    plt.ylabel('probability', fontsize=20)
    plt.xlabel('photon count', fontsize=20)
    title = rf'selected $\delta_1$={select} MHz'
    plt.title(title, fontsize=20)
    plt.show()


def Trans_4(delta_1, delta_2, R, norm, Omega_p, Omega_c, Gamma_e, Gamma_r):
    N = 4  # 4-level system
    # print(len(delta_1), type(R))
    Vex = 23.6e3 / R**3
    V = 6310e3 / R**6
    sigma_12 = basis(N, 0) * basis(N, 1).dag()
    sigma_23 = basis(N, 1) * basis(N, 2).dag()
    op_list = [np.sqrt(Gamma_e) * sigma_12, np.sqrt(Gamma_r) * sigma_23]
    trans_array = np.array([])
    for delta in delta_1:
        H = Qobj([
            [0, Omega_p / 2, 0, 0],
            [Omega_p / 2, delta, Omega_c / 2, 0],
            [0, Omega_c / 2, delta + delta_2 + V, Vex],
            [0, 0, Vex, delta + delta_2 + V]
        ])
        final_state = steadystate(H, op_list)
        trans_array = np.append(trans_array, np.exp(- norm * np.imag(final_state[0, 1])/Omega_p))
    return trans_array


def Trans_3(delta_1, delta_2, R, norm, Omega_p, Omega_c, Gamma_e, Gamma_r):  # R is here for iplt
    N = 3  # 3-level system
    sigma_12 = basis(N, 0) * basis(N, 1).dag()
    sigma_23 = basis(N, 1) * basis(N, 2).dag()
    op_list = [np.sqrt(Gamma_e) * sigma_12, np.sqrt(Gamma_r) * sigma_23]
    trans_array = np.array([])
    for delta in delta_1:
        H = Qobj([
            [0, Omega_p / 2, 0],
            [Omega_p / 2, delta, Omega_c / 2],
            [0, Omega_c / 2, delta + delta_2]
        ])
        final_state = steadystate(H, op_list)
        trans_array = np.append(trans_array, np.exp(- norm * np.imag(final_state[0, 1])/Omega_p))
    return trans_array


def onclick(event):  # call draw_dist
    x = event.xdata
    print('delta_1=', x)
    p1 = Trans_4([x], delta_2_, R_, norm_, Omega_p_, Omega_c_, Gamma_e_, Gamma_r_)[0]
    p2 = Trans_3([x], delta_2_, R_, norm_, Omega_p_, Omega_c_, Gamma_e_, Gamma_r_)[0]
    draw_dist(p1=p1, p2=p2, select=x)


def start():
    root = tk.Tk()
    root.geometry("1000x800")
    diagram_frame = tk.Frame(root)
    panel_frame = tk.Frame(root)
    image_frame = tk.Frame(root)
    para_frame_1 = tk.Frame(panel_frame, width=2000)
    para_frame_2 = tk.Frame(panel_frame, width=2000)
    para_frame_3 = tk.Frame(panel_frame, width=2000)
    button_frame = tk.Frame(panel_frame, width=2000)

    image = Image.open('diagram.png')
    k = 0.3
    width = int(2192 * k)
    height = int(830 * k)
    img = image.resize((width, height))
    img = ImageTk.PhotoImage(img)
    label = tk.Label(image_frame, image=img)
    label.pack()
    
    delta_1 = np.linspace(-150, 150, 500)  # MHz
    # scale of parameters
    Omega_p = tk.DoubleVar()
    Omega_c = tk.DoubleVar()
    delta_2 = tk.DoubleVar()
    norm = tk.DoubleVar()
    Gamma_e = tk.DoubleVar()
    Gamma_r = tk.DoubleVar()
    R = tk.DoubleVar()

    def draw_trans():
        global Omega_p_, Omega_c_, delta_2_, norm_, Gamma_e_, Gamma_r_, R_
        Omega_p_ = Omega_p.get()
        Omega_c_ = Omega_c.get()
        delta_2_ = delta_2.get()
        norm_ = norm.get()
        Gamma_e_ = Gamma_e.get()
        Gamma_r_ = Gamma_r.get()
        R_ = R.get()

        trans_4 = Trans_4(delta_1, delta_2_, R_, norm_, Omega_p_, Omega_c_, Gamma_e_, Gamma_r_)
        trans_3 = Trans_3(delta_1, delta_2_, R_, norm_, Omega_p_, Omega_c_, Gamma_e_, Gamma_r_)

        ax.cla()
        ax.plot(delta_1, trans_3, label='3-level')
        ax.plot(delta_1, trans_4, label='4-level')
        ax.set_xlabel(r'$\delta_1$ [MHz]')
        ax.set_ylabel('Transparency')
        ax.legend()

        canvas.draw()
        canvas.mpl_connect('button_press_event', onclick)

    # scale widget
    slider_length = 10
    s_Omega_p = tk.Scale(para_frame_1, variable=Omega_p, from_=0.1, to=10., orient=tk.HORIZONTAL, label='Omega_p [MHz]', sliderlength=slider_length)
    s_Omega_c = tk.Scale(para_frame_1, variable=Omega_c, from_=1., to=50., orient=tk.HORIZONTAL, label='Omega_c [MHz]', sliderlength=slider_length)
    s_delta_2 = tk.Scale(para_frame_1, variable=delta_2, from_=0., to=10., orient=tk.HORIZONTAL, label='delta_2 [MHz]', sliderlength=slider_length)
    s_norm = tk.Scale(para_frame_2, variable=norm, from_=1., to=50., orient=tk.HORIZONTAL, label='Optical_Deepth', sliderlength=slider_length)
    s_Gamma_e = tk.Scale(para_frame_2, variable=Gamma_e, from_=1., to=10., orient=tk.HORIZONTAL, label='Gamma_e [/s]', sliderlength=slider_length)
    s_Gamma_r = tk.Scale(para_frame_2, variable=Gamma_r, from_=1., to=10., orient=tk.HORIZONTAL, label='Gamma_r [/s]', sliderlength=slider_length)
    s_R = tk.Scale(para_frame_3, variable=R, from_=1., to=10., orient=tk.HORIZONTAL, label='R [um]', sliderlength=slider_length)
    # button to get parameters
    b_set_para = tk.Button(button_frame, text='Set Parameters', command=draw_trans)
    # button to quit
    b_quit = tk.Button(button_frame, text='QUIT', command=root.destroy)
    # canvas
    fig = Figure(figsize=(16, 5))
    ax = fig.add_subplot()
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk Drawing Area.

    # placement
    b_quit.pack(side=tk.RIGHT)
    b_set_para.pack(side=tk.LEFT)
    s_R.pack(side=tk.LEFT)
    s_Gamma_r.pack(side=tk.RIGHT)
    s_Gamma_e.pack(side=tk.LEFT)
    s_norm.pack(side=tk.LEFT)
    s_delta_2.pack(side=tk.RIGHT)
    s_Omega_c.pack(side=tk.LEFT)
    s_Omega_p.pack(side=tk.LEFT)

    para_frame_1.pack(side=tk.BOTTOM)
    para_frame_2.pack(side=tk.BOTTOM)
    para_frame_3.pack(side=tk.BOTTOM)
    button_frame.pack(side=tk.BOTTOM)

    canvas.get_tk_widget().pack(side=tk.TOP, expand=False)

    panel_frame.pack(side=tk.RIGHT)

    image_frame.pack(side=tk.LEFT)

    tk.mainloop()
