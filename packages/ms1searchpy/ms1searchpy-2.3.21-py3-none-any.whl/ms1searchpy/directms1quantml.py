from __future__ import division
import argparse
import pandas as pd
import numpy as np
from scipy.stats import binom, ttest_ind
import logging
from pyteomics import fasta
from collections import Counter
import random
import csv
import lightgbm as lgb
from sklearn import metrics
import ast


SEED = 42


def get_X_array(df, feature_columns):
    return df.loc[:, feature_columns].values

def get_Y_array_pfms(df):
    return df.loc[:, 'decoy2'].values

def get_features_pfms(dataframe):
    feature_columns = dataframe.columns
    columns_to_remove = []
    usefull_features = {
        'nummissing',
        'S2_mean',
        'S1_mean',
        'FC',
        'intensity_median',
        'p-value',
    }

    for feature in feature_columns:
        if feature not in usefull_features:
            columns_to_remove.append(feature)
    feature_columns = feature_columns.drop(columns_to_remove)
    return feature_columns

def objective_pfms(df, hyperparameters, iteration, threshold=0):
    """Objective function for grid and random search. Returns
    the cross validation score from a set of hyperparameters."""

    all_res = []


    # groups = df['peptide']
    # ix = df.index.values
    # unique = np.unique(groups)
    # np.random.RandomState(SEED).shuffle(unique)
    # for split in np.array_split(unique, 3):
    #     mask = groups.isin(split)
    #     train, test = ix[~mask], ix[mask]
    #     train_df = df.iloc[train]
    #     test_df = df.iloc[test]

    for group_val in range(3):
        
        mask = df['G'] == group_val
        test_df = df[mask]
        test_ids = set(test_df['peptide'])
        train_df = df[(~mask) & (df['peptide'].apply(lambda x: x not in test_ids))]



        feature_columns = get_features_pfms(df)
        ### 1
        # model = get_cat_model_pfms(df[~df['decoy2']], hyperparameters, feature_columns, train_df[~train_df['decoy2']], test_df[~test_df['decoy2']])
        # all_iters.append(model.best_iteration)
        model = get_cat_model_final_pfms(train_df, hyperparameters, feature_columns)
        # model = get_cat_model_final_pfms(train_df, hyperparameters, feature_columns)

        df.loc[mask, 'preds'] = model.predict(get_X_array(df.loc[mask, :], feature_columns))

        # train_df = df.iloc[train]
        # test_df = df.iloc[test]
        test_df = df[mask]

        ### 1
        fpr, tpr, thresholds = metrics.roc_curve(get_Y_array_pfms(test_df), test_df['preds'])
        # fpr, tpr, thresholds = metrics.roc_curve(get_Y_array_pfms(test_df), test_df['preds'])
        shr_v = metrics.auc(fpr, tpr)
        # shr_v = len(aux.filter(test_df, fdr=0.25, key='preds', is_decoy='decoy'))

        all_res.append(shr_v)

        if shr_v < threshold:
            all_res = [0, ]
            break

    shr_v = np.mean(all_res)
    # hyperparameters['n_estimators'] = int(np.max(all_iters))# * 1.5)

    return np.array([shr_v, hyperparameters, iteration, all_res], dtype=object)

def random_search_pfms(df, param_grid, out_file, max_evals):
    """Random search for hyperparameter optimization.
    Writes result of search to csv file every search iteration."""

    threshold = 0

    

    # Dataframe for results
    results = pd.DataFrame(columns = ['sharpe', 'params', 'iteration', 'all_res'],
                                index = list(range(max_evals)))
    for i in range(max_evals):

        # Choose random hyperparameters
        random_params = {k: random.sample(v, 1)[0] for k, v in param_grid.items()}

        # Evaluate randomly selected hyperparameters
        eval_results = objective_pfms(df, random_params, i, threshold)
        results.loc[i, :] = eval_results

        threshold = max(threshold, np.mean(eval_results[3]) - 3 * np.std(eval_results[3]))

        # open connection (append option) and write results
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow(eval_results)

        # make sure to close connection
        of_connection.close()

    # Sort with best score on top
    results.sort_values('sharpe', ascending = False, inplace = True)
    results.reset_index(inplace = True)

    return results

def get_cat_model_pfms(df, hyperparameters, feature_columns, train, test):
    feature_columns = list(feature_columns)
    dtrain = lgb.Dataset(get_X_array(train, feature_columns), get_Y_array_pfms(train), feature_name=feature_columns, free_raw_data=False)
    dvalid = lgb.Dataset(get_X_array(test, feature_columns), get_Y_array_pfms(test), feature_name=feature_columns, free_raw_data=False)
    np.random.seed(SEED)
    evals_result = {}
    model = lgb.train(hyperparameters, dtrain, num_boost_round=500, valid_sets=(dvalid,), valid_names=('valid',), verbose_eval=False,
                early_stopping_rounds=10, evals_result=evals_result)
    return model

def get_cat_model_final_pfms(df, hyperparameters, feature_columns):
    feature_columns = list(feature_columns)
    train = df
    dtrain = lgb.Dataset(get_X_array(train, feature_columns), get_Y_array_pfms(train), feature_name=feature_columns, free_raw_data=False)
    np.random.seed(SEED)
    model = lgb.train(hyperparameters, dtrain, num_boost_round=100)
    return model


def calc_sf_all(v, n, p):
    sf_values = -np.log10(binom.sf(v-1, n, p))
    sf_values[v <= 1] = 0
    sf_values[np.isinf(sf_values)] = 20
    sf_values[n == 0] = 0
    return sf_values

def run():
    parser = argparse.ArgumentParser(
        description='run DirectMS1quantML for ms1searchpy results',
        epilog='''

    Example usage
    -------------
    $ directms1quantml -S1 sample1_1_proteins_full.tsv sample1_n_proteins_full.tsv -S2 sample2_1_proteins_full.tsv sample2_n_proteins_full.tsv
    -------------
    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-S1', nargs='+', help='input files for S1 sample', required=True)
    parser.add_argument('-S2', nargs='+', help='input files for S2 sample', required=True)
    parser.add_argument('-out', help='name of DirectMS1quant output file', default='directms1quant_out')
    parser.add_argument('-min_samples', help='minimum number of samples for peptide usage. 0 means 50%% of input files', default=0)
    parser.add_argument('-fold_change', help='FC threshold standard deviations', default=3.0, type=float)
    parser.add_argument('-fold_change_abs', help='Use absolute log2 scale FC threshold instead of standard deviations', action='store_true')
    parser.add_argument('-qval', help='qvalue threshold', default=0.05, type=float)
    parser.add_argument('-intensity_norm', help='Intensity normalization: 0-none, 1-median', default=1, type=int)
    parser.add_argument('-all_proteins', help='use all proteins instead of FDR controlled', action='store_true')
    parser.add_argument('-all_pfms', help='use all PFMs instead of ML controlled', action='store_true')
    parser.add_argument('-output_peptides', help='Add output table with peptides', action='store_true')
    parser.add_argument('-allowed_peptides', help='path to allowed peptides')
    parser.add_argument('-allowed_proteins', help='path to allowed proteins')
    parser.add_argument('-d', '-db', help='path to uniprot fasta file for gene annotation')
    parser.add_argument('-prefix', help='Decoy prefix. Default DECOY_', default='DECOY_', type=str)
    args = vars(parser.parse_args())
    logging.basicConfig(format='%(levelname)9s: %(asctime)s %(message)s',
            datefmt='[%H:%M:%S]', level=logging.INFO)
    logger = logging.getLogger(__name__)


    replace_label = '_proteins_full.tsv'
    decoy_prefix = args['prefix']

    fold_change = float(args['fold_change'])

    df_final = False

    all_s_lbls = {}


    allowed_prots = set()
    allowed_prots_all = set()
    allowed_peptides = set()

    cnt0 = Counter()

    for i in range(1, 3, 1):
        sample_num = 'S%d' % (i, )
        if args[sample_num]:
            for z in args[sample_num]:
                if not args['allowed_proteins']:
                    if not args['all_proteins']:
                        df0 = pd.read_table(z.replace('_proteins_full.tsv', '_proteins.tsv'), usecols=['dbname', ])
                        allowed_prots.update(df0['dbname'])
                        allowed_prots.update([decoy_prefix + z for z in df0['dbname'].values])
                    else:
                        df0 = pd.read_table(z, usecols=['dbname', ])
                        allowed_prots.update(df0['dbname'])

                if not args['allowed_peptides']:
                    df0 = pd.read_table(z.replace('_proteins_full.tsv', '_PFMs_ML.tsv'), usecols=['seqs', 'qpreds', 'ch', 'im'])

                    if not args['all_pfms']:

                        df0 = df0[df0['qpreds'] <= 10]

                    df0['seqs'] = df0['seqs'] + df0['ch'].astype(str) + df0['im'].astype(str)
                    allowed_peptides.update(df0['seqs'])
                    cnt0.update(allowed_peptides)

    if args['allowed_proteins']:
        allowed_prots = set(z.strip() for z in open(args['allowed_proteins'], 'r').readlines())
        allowed_prots.update([decoy_prefix + z for z in allowed_prots])

    if args['allowed_peptides']:
        allowed_peptides = set(z.strip() for z in open(args['allowed_peptides'], 'r').readlines())
    else:

        custom_min_samples = int(args['min_samples'])
        if custom_min_samples == 0:
            custom_min_samples = int((len(args['S1']) + len(args['S2']))/2)
        print('MIN SAMPLES: %d' % (custom_min_samples, ))

        allowed_peptides = set()
        for k, v in cnt0.items():
            if v >= custom_min_samples:
                allowed_peptides.add(k)


    logger.info('Total number of TARGET protein GROUPS: %d', len(allowed_prots) / 2)

    for i in range(1, 3, 1):
        sample_num = 'S%d' % (i, )
        if args.get(sample_num, 0):
            for z in args[sample_num]:
                df3 = pd.read_table(z.replace(replace_label, '_PFMs.tsv'), usecols=['sequence', 'proteins', 'charge', 'ion_mobility'])
                # df3 = df3[df3['sequence'].apply(lambda x: x in allowed_peptides)]

                if not args['allowed_peptides']:
                    df3['tmpseq'] = df3['sequence'] + df3['charge'].astype(str) + df3['ion_mobility'].astype(str)
                    df3 = df3[df3['tmpseq'].apply(lambda x: x in allowed_peptides)]
                else:
                    df3 = df3[df3['sequence'].apply(lambda x: x in allowed_peptides)]

                df3_tmp = df3[df3['proteins'].apply(lambda x: any(z in allowed_prots for z in x.split(';')))]
                for dbnames in set(df3_tmp['proteins'].values):
                    for dbname in dbnames.split(';'):
                        allowed_prots_all.add(dbname)



    for i in range(1, 3, 1):
        sample_num = 'S%d' % (i, )
        if args.get(sample_num, 0):
            all_s_lbls[sample_num] = []
            for z in args[sample_num]:
                print('Stage 2: ', z)
                label = sample_num + '_' + z.replace(replace_label, '')
                all_s_lbls[sample_num].append(label)
                df3 = pd.read_table(z.replace(replace_label, '_PFMs.tsv'), usecols=['sequence', 'proteins', 'charge', 'ion_mobility', 'Intensity'])
                # df3 = df3[df3['sequence'].apply(lambda x: x in allowed_peptides)]

                if not args['allowed_peptides']:
                    df3['tmpseq'] = df3['sequence'] + df3['charge'].astype(str) + df3['ion_mobility'].astype(str)
                    df3 = df3[df3['tmpseq'].apply(lambda x: x in allowed_peptides)]
                else:
                    df3 = df3[df3['sequence'].apply(lambda x: x in allowed_peptides)]

                # allowed_prots2 = set()
                # df3_tmp = df3[df3['proteins'].apply(lambda x: any(z in allowed_prots for z in x.split(';')))]
                # for dbnames in set(df3_tmp['proteins'].values):
                #     for dbname in dbnames.split(';'):
                #         allowed_prots2.add(dbname)
                # print('!', len(allowed_prots), len(allowed_prots2))

                # df3 = df3[df3['proteins'].apply(lambda x: any(z in allowed_prots for z in x.split(';')))]

                df3 = df3[df3['proteins'].apply(lambda x: any(z in allowed_prots_all for z in x.split(';')))]
                df3['proteins'] = df3['proteins'].apply(lambda x: ';'.join([z for z in x.split(';') if z in allowed_prots_all]))
                ### df3['proteins'] = df3['proteins'].apply(lambda x: ';'.join([z for z in x.split(';') if z in allowed_prots]))

                df3['origseq'] = df3['sequence']
                df3['sequence'] = df3['sequence'] + df3['charge'].astype(int).astype(str) + df3['ion_mobility'].astype(str)




                df3 = df3.sort_values(by='Intensity', ascending=False)

                df3 = df3.drop_duplicates(subset='sequence')

                df3[label] = df3['Intensity']
                # df3[label+'_faims'] = df3['ion_mobility']
                # df3[label+'_scanApex'] = df3['scanApex'].astype(int)
                df3['protein'] = df3['proteins']
                df3['peptide'] = df3['sequence']
                df3 = df3[['origseq', 'peptide', 'protein', label]]

                if df_final is False:
                    df_final = df3.reset_index(drop=True)
                else:
                    df_final = df_final.reset_index(drop=True).merge(df3.reset_index(drop=True), on='peptide', how='outer')
                    df_final.protein_x.fillna(value=df_final.protein_y, inplace=True)
                    df_final.origseq_x.fillna(value=df_final.origseq_y, inplace=True)
                    df_final['protein'] = df_final['protein_x']
                    df_final['origseq'] = df_final['origseq_x']

                    df_final = df_final.drop(columns=['protein_x', 'protein_y'])
                    df_final = df_final.drop(columns=['origseq_x', 'origseq_y'])


    logger.info('Total number of peptide sequences used in quantitation: %d', len(set(df_final['origseq'])))
    # print('Total number of proteins used in quantitation %d' % (len(allowed_prots_all), ))


    df_final = df_final.assign(protein=df_final['protein'].str.split(';')).explode('protein').reset_index(drop=True)

    df_final = df_final.set_index('peptide')
    df_final['peptide'] = df_final.index
    df_final['proteins'] = df_final['protein']
    df_final = df_final.drop(columns=['protein'])
    # cols = df_final.columns.tolist()
    cols = [z for z in df_final.columns.tolist() if not z.startswith('mz_')]
    cols.remove('proteins')
    cols.insert(0, 'proteins')
    df_final = df_final[cols]

    all_lbls = all_s_lbls['S1'] + all_s_lbls['S2']

    df_final_copy = df_final.copy()

    custom_min_samples = int(args['min_samples'])
    if custom_min_samples == 0:
        custom_min_samples = int(len(all_lbls)/2)

    df_final = df_final_copy.copy()

    max_missing = len(all_lbls) - custom_min_samples

    logger.info('Allowed max number of missing values: %d', max_missing)

    df_final['nummissing'] = df_final.isna().sum(axis=1)
    df_final['nonmissing'] = df_final['nummissing'] <= max_missing

    df_final = df_final[df_final['nonmissing']]
    logger.info('Total number of PFMs passed missing values threshold: %d', len(df_final))

    

    df_final['S2_mean'] = df_final[all_s_lbls['S2']].mean(axis=1)
    df_final['S1_mean'] = df_final[all_s_lbls['S1']].mean(axis=1)
    df_final['FC_raw'] = np.log2(df_final['S2_mean']/df_final['S1_mean'])

    FC_max = df_final['FC_raw'].max()
    FC_min = df_final['FC_raw'].min()

    df_final.loc[(pd.isna(df_final['S2_mean'])) & (~pd.isna(df_final['S1_mean'])), 'FC_raw'] = FC_min
    df_final.loc[(~pd.isna(df_final['S2_mean'])) & (pd.isna(df_final['S1_mean'])), 'FC_raw'] = FC_max


    if args['intensity_norm'] == 1:
        for cc in all_lbls:
            # print(cc, df_final[cc].median())
            df_final[cc] = df_final[cc] / df_final[cc].median()


    df_final['S2_mean'] = df_final[all_s_lbls['S2']].median(axis=1)
    df_final['S1_mean'] = df_final[all_s_lbls['S1']].median(axis=1)

    for cc in all_lbls:
        df_final[cc] = df_final[cc].fillna(df_final[cc].min())

    df_final['p-value'] = list(ttest_ind(df_final[all_s_lbls['S1']].values.astype(float), df_final[all_s_lbls['S2']].values.astype(float), axis=1, nan_policy='omit', equal_var=True)[1])
    df_final['p-value'] = df_final['p-value'].astype(float)
    df_final['p-value'] = df_final['p-value'].fillna(1.0)

    p_val_threshold = 0.05

    df_final['sign'] = df_final['p-value'] <= p_val_threshold

    df_final['intensity_median'] = df_final[all_s_lbls['S1'] + all_s_lbls['S2']].median(axis=1)

    df_final['FC'] = np.log2(df_final['S2_mean']/df_final['S1_mean'])

    df_final_for_calib = df_final.copy()
    df_final_for_calib = df_final_for_calib[~pd.isna(df_final_for_calib['S1_mean'])]
    df_final_for_calib = df_final_for_calib[~pd.isna(df_final_for_calib['S2_mean'])]
    df_final_for_calib = df_final_for_calib[~df_final_for_calib['sign']]

    FC_max = df_final['FC'].max()
    FC_min = df_final['FC'].min()

    df_final.loc[(pd.isna(df_final['S2_mean'])) & (~pd.isna(df_final['S1_mean'])), 'FC'] = FC_min
    df_final.loc[(~pd.isna(df_final['S2_mean'])) & (pd.isna(df_final['S1_mean'])), 'FC'] = FC_max

    df_final['decoy'] = df_final['proteins'].apply(lambda x: all(z.startswith(decoy_prefix) for z in x.split(';')))






    param_grid = {
        'boosting_type': ['gbdt', ],
        'num_leaves': list(range(10, 1000)),
        'learning_rate': list(np.logspace(np.log10(0.001), np.log10(0.3), base = 10, num = 1000)),
    #     'learning_rate': list(np.logspace(np.log10(0.1), np.log10(0.3), base = 10, num = 1000)),
        # 'subsample_for_bin': list(range(1, 10000, 10)),
        'min_child_samples': list(range(1, 1000, 5)),
        'reg_alpha': list(np.linspace(0, 1)),
        'reg_lambda': list(np.linspace(0, 1)),
        'colsample_bytree': list(np.linspace(0.01, 1, 100)),
        'subsample': list(np.linspace(0.01, 1, 100)),
        'is_unbalance': [True, False],
        'metric': ['rmse', ],
        'verbose': [-1, ],
        'num_threads': [6, ],
    }



    def is_decoy_2(proteins, decoy_set):
        return all(z in decoy_set for z in proteins.split(';'))
    all_decoys = set()
    for proteins in df_final.loc[df_final.decoy, 'proteins'].values:
        all_decoys.update(proteins.split(';'))
    all_decoys_2 = set(random.sample(all_decoys, int(len(all_decoys) / 2)))
    df_final['decoy2'] = df_final['proteins'].apply(is_decoy_2, decoy_set=all_decoys_2)

    print('!', sum(df_final['decoy']), sum(df_final['decoy2']))

    print(df_final.columns)

    print(get_features_pfms(df_final))




#    if args['ml'] and not skip_ml:

    print('Start Machine Learning on PFMs...')

    MAX_EVALS = 25

    out_file = '/home/mark/testMLQuant.tsv'#os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    of_connection = open(out_file, 'w')
    writer = csv.writer(of_connection)

    # Write column names
    headers = ['auc', 'params', 'iteration', 'all_res']
    writer.writerow(headers)
    of_connection.close()



    all_id_list = list(set(df_final[df_final['decoy']]['peptide']))
    all_id_list = random.sample(all_id_list, len(all_id_list))
    seq_gmap = {}
    for idx, split in enumerate(np.array_split(all_id_list, 3)):
        for id_ftr in split:
            seq_gmap[id_ftr] = idx
            
    all_id_list = list(set(df_final[~df_final['decoy']]['peptide']))
    all_id_list = random.sample(all_id_list, len(all_id_list))
    for idx, split in enumerate(np.array_split(all_id_list, 3)):
        for id_ftr in split:
            seq_gmap[id_ftr] = idx



    df_final['G'] = df_final['peptide'].apply(lambda x: seq_gmap[x])



    random_results = random_search_pfms(df_final, param_grid, out_file, MAX_EVALS)

    random_results = pd.read_csv(out_file)
    random_results = random_results[random_results['auc'] != 'auc']
    random_results['params'] = random_results['params'].apply(lambda x: ast.literal_eval(x))
    convert_dict = {'auc': float,
                }
    random_results = random_results.astype(convert_dict)


    bestparams = random_results.sort_values(by='auc',ascending=False)['params'].values[0]

    # bestparams['num_threads'] = args['nproc']



    for group_val in range(3):
        
        mask = df_final['G'] == group_val
        test_df = df_final[mask]
        test_ids = set(test_df['peptide'])
        train_df = df_final[(~mask) & (df_final['peptide'].apply(lambda x: x not in test_ids))]


        feature_columns = list(get_features_pfms(train_df))
        model = get_cat_model_final_pfms(train_df, bestparams, feature_columns)

        df_final.loc[mask, 'preds'] = model.predict(get_X_array(test_df, feature_columns))










    from scipy.stats import scoreatpercentile
    from scipy.optimize import curve_fit
    from scipy import exp
    def noisygaus(x, a, x0, sigma, b):
        return a * exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + b

    def calibrate_mass(bwidth, mass_left, mass_right, true_md):

        bbins = np.arange(-mass_left, mass_right, bwidth)
        H1, b1 = np.histogram(true_md, bins=bbins)
        b1 = b1 + bwidth
        b1 = b1[:-1]


        popt, pcov = curve_fit(noisygaus, b1, H1, p0=[1, np.median(true_md), 1, 1])
        mass_shift, mass_sigma = popt[1], abs(popt[2])
        return mass_shift, mass_sigma, pcov[0][0]

    try:
        FC_mean, FC_std, covvalue_cor = calibrate_mass(0.05, -df_final_for_calib['FC'].min(), df_final_for_calib['FC'].max(), df_final_for_calib['FC'])
    except:
        FC_mean, FC_std, covvalue_cor = calibrate_mass(0.1, -df_final_for_calib['FC'].min(), df_final_for_calib['FC'].max(), df_final_for_calib['FC'])
    # print('df_final_FC', FC_mean, FC_std)

    # FC_l = FC_mean-fold_change
    # FC_r = FC_mean+fold_change

    if not args['fold_change_abs']:
        fold_change = FC_std * fold_change
    logger.info('Absolute FC threshold = %.2f', fold_change)
    FC_l = -fold_change
    FC_r = fold_change


    df_final_copy = df_final.copy()


    df_final['up'] = df_final['sign'] * (df_final['FC'] >= FC_r)
    df_final['down'] = df_final['sign'] * (df_final['FC'] <= FC_l)

    if args['output_peptides']:
        df_final['peptide'] = df_final.index
        df_final.to_csv(path_or_buf=args['out']+'_quant_peptides.tsv', sep='\t', index=False)

    df_final = df_final.sort_values(by=['nummissing', 'intensity_median'], ascending=(True, False))
    df_final = df_final.drop_duplicates(subset=('origseq', 'proteins'))

    up_dict = df_final.groupby('proteins')['up'].sum().to_dict()
    down_dict = df_final.groupby('proteins')['down'].sum().to_dict()

    ####### !!!!!!! #######
    df_final['up'] = df_final.apply(lambda x: x['up'] if up_dict.get(x['proteins'], 0) >= down_dict.get(x['proteins'], 0) else x['down'], axis=1)
    protsN = df_final.groupby('proteins')['up'].count().to_dict()

    prots_up = df_final.groupby('proteins')['up'].sum()

    N_decoy_total = df_final['decoy'].sum()

    upreg_decoy_total = df_final[df_final['decoy']]['up'].sum()

    p_up = upreg_decoy_total / N_decoy_total

    names_arr = np.array(list(protsN.keys()))

    logger.info('Total number of proteins used in quantitation: %d', sum(not z.startswith(decoy_prefix) for z in names_arr))
    logger.info('Total number of peptides: %d', len(df_final))
    logger.info('Total number of decoy peptides: %d', N_decoy_total)
    logger.info('Total number of significantly changed decoy peptides: %d', upreg_decoy_total)
    logger.info('Probability of random peptide to be significantly changed: %.3f', p_up)
    # print(N_decoy_total, upreg_decoy_total, p_up)






    df_final = df_final_copy.copy()
    df_final = df_final.sort_values(by='preds')
    df_final['sign'] = df_final['decoy'].cumsum() <= upreg_decoy_total


    df_final['up'] = df_final['sign'] * (df_final['FC'] >= 0)
    df_final['down'] = df_final['sign'] * (df_final['FC'] < 0)

    if args['output_peptides']:
        df_final['peptide'] = df_final.index
        df_final.to_csv(path_or_buf=args['out']+'_quant_peptidesML.tsv', sep='\t', index=False)

    df_final = df_final.sort_values(by=['nummissing', 'intensity_median'], ascending=(True, False))
    df_final = df_final.drop_duplicates(subset=('origseq', 'proteins'))

    up_dict = df_final.groupby('proteins')['up'].sum().to_dict()
    down_dict = df_final.groupby('proteins')['down'].sum().to_dict()

    ####### !!!!!!! #######
    df_final['up'] = df_final.apply(lambda x: x['up'] if up_dict.get(x['proteins'], 0) >= down_dict.get(x['proteins'], 0) else x['down'], axis=1)
    protsN = df_final.groupby('proteins')['up'].count().to_dict()

    prots_up = df_final.groupby('proteins')['up'].sum()

    N_decoy_total = df_final['decoy'].sum()

    upreg_decoy_total = df_final[df_final['decoy']]['up'].sum()

    p_up = upreg_decoy_total / N_decoy_total

    names_arr = np.array(list(protsN.keys()))

    logger.info('Total number of proteins used in quantitation: %d', sum(not z.startswith(decoy_prefix) for z in names_arr))
    logger.info('Total number of peptides: %d', len(df_final))
    logger.info('Total number of decoy peptides: %d', N_decoy_total)
    logger.info('Total number of significantly changed decoy peptides: %d', upreg_decoy_total)
    logger.info('Probability of random peptide to be significantly changed: %.3f', p_up)









    v_arr = np.array(list(prots_up.get(k, 0) for k in names_arr))
    n_arr = np.array(list(protsN.get(k, 0) for k in names_arr))

    all_pvals = calc_sf_all(v_arr, n_arr, p_up)

    total_set = set()
    total_set_genes = set()

    FC_up_dict_basic = df_final.groupby('proteins')['FC'].median().to_dict()
    FC_up_dict_raw_basic = df_final.groupby('proteins')['FC_raw'].median().to_dict()

    df_final = df_final[df_final['up']>0]

    df_final['bestmissing'] = df_final.groupby('proteins')['nummissing'].transform('min')

    FC_up_dict2 = df_final.groupby('proteins')['FC'].median().to_dict()
    FC_up_dict_raw2 = df_final.groupby('proteins')['FC_raw'].median().to_dict()

    FC_up_dict = df_final[df_final['bestmissing']==df_final['nummissing']].groupby('proteins')['FC'].median().to_dict()
    FC_up_dict_raw = df_final[df_final['bestmissing']==df_final['nummissing']].groupby('proteins')['FC_raw'].median().to_dict()

    # FC_up_dict = df_final.groupby('proteins')['FC'].median().to_dict()


    df_out = pd.DataFrame()
    df_out['score'] = all_pvals
    df_out['dbname'] = names_arr

    df_out['FC'] = df_out['dbname'].apply(lambda x: FC_up_dict.get(x))
    df_out['FC_raw'] = df_out['dbname'].apply(lambda x: FC_up_dict_raw.get(x))

    df_out.loc[pd.isna(df_out['FC']), 'FC'] = df_out.loc[pd.isna(df_out['FC']), 'dbname'].apply(lambda x: FC_up_dict_basic.get(x))
    df_out.loc[pd.isna(df_out['FC_raw']), 'FC_raw'] = df_out.loc[pd.isna(df_out['FC_raw']), 'dbname'].apply(lambda x: FC_up_dict_raw_basic.get(x))


    df_out['FC2'] = df_out['dbname'].apply(lambda x: FC_up_dict2.get(x))
    df_out['FC2_raw'] = df_out['dbname'].apply(lambda x: FC_up_dict_raw2.get(x))

    df_out.loc[pd.isna(df_out['FC2']), 'FC2'] = df_out.loc[pd.isna(df_out['FC2']), 'dbname'].apply(lambda x: FC_up_dict_basic.get(x))
    df_out.loc[pd.isna(df_out['FC2_raw']), 'FC2_raw'] = df_out.loc[pd.isna(df_out['FC2_raw']), 'dbname'].apply(lambda x: FC_up_dict_raw_basic.get(x))


    df_out.loc[:, 'FC_basic'] = df_out.loc[:, 'dbname'].apply(lambda x: FC_up_dict_basic.get(x))
    df_out.loc[:, 'FC_basic_raw'] = df_out.loc[:, 'dbname'].apply(lambda x: FC_up_dict_raw_basic.get(x))

    df_out['v_arr'] = v_arr
    df_out['n_arr'] = n_arr

    df_out['decoy'] = df_out['dbname'].str.startswith(decoy_prefix)

    df_out = df_out[~df_out['decoy']]

    # df_out['FC_pass'] = (df_out['FC'].abs() >= fold_change) & (df_out['v_arr'] > 0)
    df_out['FC_pass'] = (df_out['FC'].abs() >= 0) & (df_out['v_arr'] > 0)


    df_out['protname'] = df_out['dbname'].apply(lambda x: x.split('|')[1] if '|' in x else x)

    genes_map = {}
    if args['d']:
        for prot, protseq in fasta.read(args['d']):
            try:
                prot_name = prot.split('|')[1]
            except:
                prot_name = prot
            try:
                gene_name = prot.split('GN=')[1].split(' ')[0]
            except:
                gene_name = prot
            genes_map[prot_name] = gene_name

        df_out['gene'] = df_out['protname'].apply(lambda x: genes_map[x])

    else:
        df_out['gene'] = df_out['protname']

    df_out_BH_multiplier = df_out['FC_pass'].sum()

    qval_threshold = args['qval']

    df_out['p-value'] = 1.0
    df_out['BH_pass'] = False

    df_out = df_out.sort_values(by='score', ascending=False)

    df_out.loc[df_out['FC_pass'], 'BH_threshold'] = -np.log10(df_out.loc[df_out['FC_pass'], 'score'].rank(ascending=False, method='max') * qval_threshold / df_out_BH_multiplier)

    current_rank = 0
    BH_threshold_array = []
    added_genes = set()
    for z in df_out[df_out['FC_pass']]['gene'].values:
        if z not in added_genes:
            added_genes.add(z)
            current_rank += 1
        BH_threshold_array.append(-np.log10(current_rank * qval_threshold / df_out_BH_multiplier))
    df_out.loc[df_out['FC_pass'], 'BH_threshold'] = BH_threshold_array


    # df_out.loc[df_out['FC_pass'], 'BH_threshold'] = -np.log10(df_out.loc[df_out['FC_pass'], 'score'].rank(ascending=False, method='max') * qval_threshold / df_out_BH_multiplier)
    df_out.loc[df_out['FC_pass'], 'BH_pass'] = df_out.loc[df_out['FC_pass'], 'score'] > df_out.loc[df_out['FC_pass'], 'BH_threshold']
    df_out.loc[df_out['FC_pass'], 'p-value'] = 10**(-df_out.loc[df_out['FC_pass'], 'score'])
    score_threshold = df_out[df_out['BH_pass']]['score'].min()
    df_out.loc[df_out['FC_pass'], 'BH_pass'] = df_out.loc[df_out['FC_pass'], 'score'] >= score_threshold

    df_out.to_csv(path_or_buf=args['out']+'_quant_full.tsv', sep='\t', index=False)

    df_out_f = df_out[(df_out['BH_pass']) & (df_out['FC_pass'])]

    df_out_f.to_csv(path_or_buf=args['out']+'.tsv', sep='\t', index=False)

    for z in set(df_out_f['dbname']):
        try:
            prot_name = z.split('|')[1]
        except:
            prot_name = z

        gene_name = genes_map.get(prot_name, prot_name)

        total_set.add(prot_name)
        total_set_genes.add(gene_name)

    logger.info('Total number of significantly changed proteins: %d', len(total_set))
    logger.info('Total number of significantly changed genes: %d', len(total_set_genes))

    f1 = open(args['out'] + '_proteins_for_stringdb.txt', 'w')
    for z in total_set:
        f1.write(z + '\n')
    f1.close()

    f1 = open(args['out'] + '_genes_for_stringdb.txt', 'w')
    for z in total_set_genes:
        f1.write(z + '\n')
    f1.close()

if __name__ == '__main__':
    run()
