import time, scipy.io as sio, csv, numpy as np, matplotlib.pyplot as plt, os
from statistics import mean
from datetime import datetime

np.set_printoptions(suppress=True)

# Timer functions
def tic():
    start = time.time()
    return start
def toc(start, label='This program'):
    end = time.time(); t_sec = end-start; mins = t_sec//60; secs = t_sec-mins*60
    print(f"{label} took {mins} minutes and {secs} seconds")
    return end

def now(seperator=''):
    spr = seperator
    now = datetime.now().strftime(f'%Y{spr}%m{spr}%d{spr}%H{spr}%M{spr}%S')
    return now

def softmax_proportional(x):
    y = []
    min_x = min(x)
    x = [i+abs(min_x)+100 for i in x]
    sum_x = sum(x)
    for x_i in x:
        y.append(x_i/sum_x)
    return y

def softmax_to_integers(max_val: int, lista, lower_bound=1) -> list: 
    l_len = len(lista)

    if lower_bound*l_len > max_val: raise ValueError(f'You cannot have {l_len} elements witch its having at least {lower_bound} value and they add up to {max_val}')
    if not isinstance(max_val, int): raise TypeError('Max_val needs to be int')

    integer_softmax = np.ones((1,l_len))*lower_bound
    lista = [item*(max_val-l_len) for item in lista]
    rnd_lista = np.round(lista)
    given = rnd_lista-lista
    left_overs = max_val - np.sum(rnd_lista) - l_len*lower_bound
    left_overs_sign = np.sign(left_overs)
    given *= left_overs_sign
    gived = np.zeros((l_len,))

    left_overs = int(abs(left_overs))
    for i in range(left_overs):
        idx = np.argmin(given)
        given[idx] += 1
        gived[idx] += 1
    gived *= left_overs_sign

    integer_softmax += gived + rnd_lista
    integer_softmax = integer_softmax[0].tolist()
    integer_softmax = [int(i) for i in integer_softmax]
    
    return integer_softmax
    

# def polyak_update(
#     params: Iterable[th.Tensor],
#     target_params: Iterable[th.Tensor],
#     tau: float,
# ) -> None:
#     with th.no_grad():
#         # zip does not raise an exception if length of parameters does not match.
#         for param, target_param in zip_strict(params, target_params):
#             target_param.data.mul_(1 - tau)
#             th.add(target_param.data, param.data, alpha=tau, out=target_param.data)

# def zip_strict(*iterables: Iterable) -> Iterable:
#     r"""
#     ``zip()`` function but enforces that iterables are of equal length.
#     Raises ``ValueError`` if iterables not of equal length.
#     Code inspired by Stackoverflow answer for question #32954486.

#     :param \*iterables: iterables to ``zip()``
#     """
#     # As in Stackoverflow #32954486, use
#     # new object for "empty" in case we have
#     # Nones in iterable.
#     sentinel = object()
#     for combo in zip_longest(*iterables, fillvalue=sentinel):
#         if sentinel in combo:
#             raise ValueError("Iterables have different lengths")
#         yield combo

def csv_to_dict(dir):
    with open(dir, 'r') as file:
        reader = csv.reader(file)

        header = next(reader)
        data = {}
        for i in range(len(header)):
            data[header[i]] = []
        for row in reader:
            for i in range(len(header)):
                data[header[i]].append(row[i])
    return data

def csv_to_mat(csv_path, save_path, newfile_name):
    data = csv_to_dict(csv_path)
    # del data['Wall time']
    sio.savemat(save_path + '/' + newfile_name +'.mat', data)

def plot_person_progress(dir, run_dir, what_to_plot='rollout/ep_rew_mean', save=False, show=True, clf=True):
    # dir = f'/home/athanasiospetsanis/Documents/Work/XCAO/XCAO_NN_Final/Measurements/{env_name}/' + dir 
    data_mat = sio.loadmat(dir)
    data = data_mat[what_to_plot]
    steps_till_eval = data_mat['time/total_timesteps']

    data = np.char.strip(data)
    steps_till_eval = np.char.strip(steps_till_eval)
    data2 = []; steps_till_eval2 = []
    
    for idx, el in enumerate(data.tolist()):
        el = el.strip()
        if el!='': 
            data2.append(float(el))
            steps_till_eval2.append(float(steps_till_eval[idx]))

    # data2 = float(data2)
    # steps_till_eval2 = steps_till_eval2.astype(np.float)

    plt.plot(steps_till_eval2, data2, label=run_dir)
    plt.ylabel(what_to_plot)
    if save: plt.savefig(f'{dir}')
    if show: plt.show()
    if clf: plt.clf()
    return data2, steps_till_eval2

def plot_epoch_progress(env_name, algo, log, what_to_plot='rollout/ep_rew_mean', show=True, save=True, seperate=False, avg=False, maxx=False):
    log = f'Measurements/{env_name}/{algo}/{log}'
    runs_data = []; mean_data = []
    dirs = os.listdir(log)

    for run_dir in dirs:
        if os.path.isdir(f'{log}/{run_dir}'):
            full_path = log + '/' + run_dir + '/progress.mat'
            plt.figure(1) 
            data, steps_till_eval = plot_person_progress(full_path, run_dir, what_to_plot, show=False, clf=False)

            max_data = []; max_val = -1e20
            for sample in data:
                if max_val < sample: max_val = sample
                max_data.append(max_val)
            
            runs_data.append(max_data)

            if maxx: plt.figure(2); plt.plot(steps_till_eval, max_data, label=run_dir)

    for i in range(len(steps_till_eval)):
        runs_val = []
        for run_data in runs_data:
            runs_val.append(run_data[i])
        mean_data.append(mean(runs_val))
    if avg: plt.figure(3); plt.plot(steps_till_eval, mean_data)

    plt.figure(1).set_size_inches(18, 10); plt.title(f'{algo} Evals', wrap=True); plt.ylabel(what_to_plot); plt.xlabel('nof Interactions'); plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    if maxx: plt.figure(2).set_size_inches(18, 10); plt.title(f'{algo} Evals', wrap=True); plt.ylabel(f'Max of {what_to_plot}'); plt.xlabel('nof Interactions'); plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    if avg: plt.figure(3); plt.title(f'{algo} Evals', wrap=True); plt.ylabel(f'Mean of {what_to_plot}'); plt.xlabel('nof Interactions')
    if save: 
        plt.figure(1); plt.savefig(f'{log}/Runs')
        if maxx: plt.figure(2); plt.savefig(f'{log}/Runs_max_value')
        if avg:plt.figure(3); plt.savefig(f'{log}/Runs, mean of max value')
    if seperate:
        plt.figure(1); plt.savefig(f'{log}/{what_to_plot.replace("/", "")}')
    if show: plt.show()
    else: plt.clf()

def plot_total_progress(save_path, epoch_train_steps, name='GeNN', what_to_plot='rollout/ep_rew_mean', show=True, save=True):
    epochs = next(os.walk(save_path))[1]
    nof_epochs = len(epochs)
    sof_population  = len(next(os.walk(save_path + '/' + epochs[0]))[1])
    data = [[] for _ in range(sof_population)]

    for i, epoch in enumerate(epochs):
        people_path = save_path + '/' + epoch
        people = next(os.walk(people_path))[1]
        for j, person in enumerate(people):
            person_path = people_path + '/'  + person
            data_mat = sio.loadmat(person_path + '/progress.mat')
            for d in data_mat[what_to_plot]:
                data[j].append(float(d))

    plt.figure().set_size_inches(18, 10); plt.title(f'Evolution', wrap=True); plt.ylabel(what_to_plot); plt.xlabel(f'nof Interactions (*{epoch_train_steps})'); plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    for i in range(sof_population):
        plt.plot(data[i])
    data_len = np.shape(data_mat[what_to_plot])[0]
    for i in range(nof_epochs):
        plt.axvline(x = i*data_len, color = 'b', linestyle='dashed', label = 'New Epoch')
    if save: plt.savefig(save_path + '/' + name)
    if show: plt.show()