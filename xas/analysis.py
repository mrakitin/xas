import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xas.file_io import load_binned_df_from_file, save_binned_df_as_file
import os

def filenames_from_dir(path, base='', ext=''):
    filenames = []
    if type(base) == str:
        (_, _, all_filenames) = next(os.walk(path))
        for f in all_filenames:
            if f.startswith(base) and f.endswith(ext) and ('merge' not in f):
                filenames.append(os.path.join(path, f))
    elif type(base) == list:
        for f in base:
            filenames.append(os.path.join(path, f))
    else:
        print('Invalid file type. Return None')
        return None
    return np.sort(filenames)





def average_scans(path, base, ext=''):
    filenames = filenames_from_dir(path, base=base, ext=ext)
    header_av = '# merge\n'
    path_av =os.path.join(path, base + ' merged' + ext)
    # define energy grid and read the data to merge
    n = len(filenames)
    energy_lo = np.zeros(n)
    energy_hi = np.zeros(n)
    df_list = []
    for i, f in enumerate(filenames):
        df, header = load_binned_df_from_file(f)
        df_list.append(df)
        energy_lo[i] = df.iloc[:, 0].min()
        energy_hi[i] = df.iloc[:, 0].max()
        _, new_line = os.path.split(f)
        header_av += '# ' + new_line + '\n'

    energy_lo = energy_lo.max()
    energy_hi = energy_hi.min()
    E = np.array(df_list[0].iloc[:, 0])
    E = E[(E >= energy_lo) & (E <= energy_hi)]

    # create new df
    idx = pd.Index(np.arange(E.size))
    columns = df_list[0].columns
    df_av = pd.DataFrame( index=idx, columns=columns)
    df_av.iloc[:, 0] = E
    df_av.iloc[:, 1:] = 0


    # average
    for each_df in df_list:
        data = np.array(each_df.iloc[:, 1:])
        n_cols = data[0, :].size
        E_cur = np.array(each_df.iloc[:, 0])
        data_int = np.array([np.interp(E, E_cur, data[:, i]) for i in range(n_cols)]).T
        df_av.iloc[:, 1:] += data_int
    df_av.iloc[:, 1:] /= n

    columns_str = '  '.join(columns)
    fmt = '%12.6f ' + (' '.join(['%12.6e' for i in range(len(columns) - 1)]))
    np.savetxt(path_av,
               df_av.values,
               delimiter=" ",
               fmt=fmt,
               header=f'# {columns_str}',
               comments=header_av)
    # dfgd
    # save_binned_df_as_file(path_av, df_av, header_av)


    # plt.figure(1)
    # plt.clf()
    # for each_df in df_list:
    #     plt.plot(each_df['energy'], each_df['iff'])
    # plt.plot(df_av['energy'], df_av['iff'], 'r-')
    # dfgef





# def test_interpolation(fpath):


