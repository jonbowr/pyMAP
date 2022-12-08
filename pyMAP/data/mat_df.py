import numpy as np
import pandas as pd

class mat_df:
    # Array/Matrix Hybrid data frame for easy interaction

    def __init__(self,dat = [] ,minor_lables = [],major_lables= [],
                                     dependent_data = 0,major_ax = None):
        if type(dat)==list:
            maj_tot = []
            for m_labs,maj_lab in zip(minor_lables,major_lables):
                maj_tot += [maj_lab]*len(m_labs) 
            h = pd.MultiIndex.from_arrays([maj_tot,list(np.concatenate(minor_lables))],
                                                    names = ['type','val'])
            self.df = pd.DataFrame(np.concatenate(dat,axis = 1),columns = h)
            self.dependent_df = major_lables[dependent_data]


            if not major_ax:
                major_ax = [0,0]
            if type(major_ax[0]) == int:
                self.major_ax = (major_lables[major_ax[0]],minor_lables[major_ax[0]][major_ax[1]])        
            elif type(major_ax[0]) == str:
                self.major_ax = major_ax
        elif type(dat)==pd.DataFrame:
            self.df = dat
            if not major_ax:
                self.major_ax = dat.keys().values[0]
                self.dependent_df = dat.keys().values[0][0]
            elif type(major_ax) == int:
                self.major_ax =  dat.keys().values[major_ax]
                self.dependent_df = dat.keys().values[major_ax,0]
            elif type(major_ax) == tuple and type(major_ax[0]) == str:
                self.major_ax = major_ax
                self.dependent_df = major_ax[0]
        self.supp_data = []


    def __getitem__(self,item):
        if item in self.df:
            return(self.df[item])
        elif item in self.df[self.dependent_df]:
            return(self.df[self.dependent_df][item])

    def __setitem__(self,item,value):
        self.df[item] = value

    def __str__(self):
        return(str(self.df))

    def __call__(self):
        return(self.df)

    def __iter__(self):
        mkeys = np.stack(self.df.keys())[:,0]
        ind = np.sort(np.unique(mkeys,return_index = True)[1])
        return(iter(mkeys[ind]))
        # mkeys = self.keys()

    def __repr__(self):
        return(self.df.__repr__())

    def loc(self,locr):
        return(mat_df(self.df.loc[locr],major_ax = self.major_ax))

    def get_axes(self):
        return({lab:[self.df[self.major_ax].values,
                        self.labels()[lab].astype(float)] for lab in self\
                        if lab != self.dependent_df and lab not in self.supp_data})

    def get_bins(self):
        hbins = {}
        for lab,ax in self.get_axes().items():
            bins = []
            for a in ax:
                d = np.nanmedian(np.diff(a))
                bins.append(np.insert(a+d/2,0,a[0]-d/2))
            hbins[lab] = bins
        return(hbins)

    def get_base_ax(self):
        return(self.df[self.major_ax].values)

    def get_base_bins(self):
        a = self.get_base_ax()
        # d = np.nanmedian(np.diff(a))
        d = np.diff(a)
        d = np.append(d,d[-1])
        # return(np.insert(a+d/2,0,a[0]-d/2))
        return(np.insert(a+d/2,0,a[0]-d[0]/2))

    def add(self,x,values,statistic = 'mean',inplace = True,
                                label = '',ax = None,dat_type = 'mat',combine = False):
        from scipy.stats import binned_statistic as bs
        bins = self.get_base_bins()
        withit = np.logical_and(x>np.nanmin(bins),x<np.nanmax(bins))
        thing = bs(x[withit],
                    values[withit].T,
                    bins= self.get_base_bins(),
                    # range = (min(bins),max(bins))
                    statistic = statistic,
                    )[0]
        if combine == False or label not in self.df[self.dependent_df].keys():
            if ax is None:
                self.df[(self.dependent_df,label)] = thing
            else: 
                for val,acc in zip(ax,thing):
                    self.df[(label,val)] = acc
                if dat_type != 'mat':
                    if label not in self.supp_data:
                        self.supp_data.append(label)
        elif combine == True:
            if label in self.df[self.dependent_df]:
                self.df[(self.dependent_df,label)].loc[~np.isnan(thing)] = thing[~np.isnan(thing)]

    def labels(self):
        return({lab:self.df[lab].keys().values for lab in self})

    def get_mats(self):
        return({thing: self.df[thing] for thing in self if thing != self.dependent_df \
                        and thing not in self.supp_data})

    def keys(self):
        return({lab:[(lab,k) for k in self.df[lab].keys().values] for lab in self})

    def reduce(self,reduce_type = 'sum'):
        reduce_df = self.df[[nam for nam in self.labels() \
                         if nam != self.dependent_df]].sum(axis = 1,skipna = True,level = 0)

        return(pd.concat([reduce_df],
                  keys =[reduce_type.upper()],
                  names = list(self.df.keys().names),
                  axis = 1,
                  ))
    
    def mask(self,log,inplace = True,keep_shape = True):
        ndf = self.df.copy()
        for k,keys in self.keys().items():
            if keep_shape:
                ndf.loc[log,keys] = np.nan
        ndf.loc[:,self.major_ax] = self.df[self.major_ax]

        if inplace:
            self.df = ndf
            return(self)
        else:
            return(mat_df(ndf))
    def drop_mat(self,lab):
        self.df.drop([val for val in self.keys()[lab]],inplace = True,axis = 1)
        return(self)

    def _repr_pretty_(self, p, cycle):
        from IPython.display import display
        # display(self.reduce())
        display_cols = []
        for labs,vals in self.keys().items(): 
            if labs == self.dependent_df:
                display_cols += vals
            else:
                display_cols += [vals[i] for i in [0,-1]]
        display(pd.concat([self.df[display_cols],self.reduce()],axis = 1))

    def accum_bins(self,binnum = 1,reduce_f ={},bin_split = None,mat_reduce = np.nansum):

        if bin_split:
            dat_l = [x for _, x in self.df.groupby((self.dependent_df,bin_split))]
        else: 
            dat_l = [self.df]

        d_split = []
        for d in dat_l:
            n_dat = []
            m_labs = []
            maj_labs = []
            rem = d[self.dependent_df].shape[0]%binnum
            tf = np.zeros(d.shape[0]).astype(bool)
            tf[:-rem] = True
            df = d.loc[tf]

            # df = self.df.loc[-rem,:]
            for mtype,vals in self.labels().items():
                if mtype == self.dependent_df:
                    dep_dat = []
                    if reduce_f:
                        for lab in df[mtype]:
                            # print(lab)
                            if lab in reduce_f:
                                dep_dat.append(reduce_f[lab](df[mtype][lab].values.reshape(-1,binnum),
                                                          axis = 1))
                            else:
                                dep_dat.append(np.nanmean(df[mtype][lab].values.reshape(-1,binnum),
                                                          axis = 1))
                        n_dat.append(np.stack(dep_dat).T)
                    else:
                        n_dat.append(np.nanmean(df[mtype].values.reshape(-1,binnum,
                                                        df[mtype].shape[1]),axis = 1))
                if mtype != self.dependent_df:
                    n_dat.append(mat_reduce(df[mtype].values.reshape(-1,binnum,
                                                        df[mtype].shape[1]),axis = 1))
                m_labs.append(list(self.df[mtype].keys().values))
                maj_labs.append(mtype)
            d_split.append(mat_df(n_dat,m_labs,maj_labs).df)
        d_out =mat_df(pd.concat(d_split,ignore_index = True))
        d_out.dependent_df = self.dependent_df
        d_out.supp_data = self.supp_data 
        return(d_out)

    def group_bins(self,binnum  = 2, reduce_f = {},mat_reduce = {}):
        # total_f = {}
        keys = self.keys()
        for lab,func in mat_reduce.items():

            for k in keys[lab]:
                reduce_f[k] = func

        # total_f = {}
        # for lab,func in reduce_f:
        #     for key in self.get_keys()[self.dependent_df]:
        #         if lab in key:
        #             total_f[key] = lab

        # for lab,key in self.get_


        g_df = self.df.groupby(self.df.index // binnum).agg(reduce_f)
        d_out = mat_df(g_df)
        # d_out =mat_df(pd.concat(d_split,ignore_index = True))
        d_out.dependent_df = self.dependent_df
        d_out.supp_data = self.supp_data 
        d_out.major_ax = self.major_ax
        return(d_out)


    def accum_bins2(self,binnum = 1,reduce_f ={},bin_split = None):
        from scipy.stats import binned_statistic as bs
        def digi_round(value,bin_edges,binm):
            # general binning utility function, rounds phase_angle to nearest binm
            t_loc = np.digitize(value,bin_edges[:-1].flatten()).flatten()-1
            return(binm[t_loc])


        if bin_split:
            dat_l = [mat_df(x) for _, x in self.df.groupby((self.dependent_df,bin_split))]
        else: 
            dat_l = [self]

        d_split = []
        thing = {
                ('eph','t_mean'):np.mean,
                ('eph','time'):np.mean,
                ('eph','start_time'):np.min,
                ('eph','end_time'):np.max,
                ('eph','dt'):np.sum,
                }
        dep_stuff= {}
        for th in self.df:
            if th not in thing:
                thing[th] = np.sum

        for d in dat_l:
            rem = d[self.dependent_df].shape[0]%binnum
            bins = d.get_base_bins()[::binnum]
            mids = (bins[1:]+bins[:-1])/2
            # return(bins,mids)
            t_rnd = digi_round(d['t_mean'],bins,mids)
            # return(t_rnd)
            d_split.append(d.df.groupby(t_rnd).agg(thing))

        return(mat_df(pd.concat(d_split,ignore_index = True)))

    def mat_print(self,loc='',mat_formatter = '%d',
                                splitby = None,split_folders = False,
                                        reduce_func = np.floor,print_type = int):
        import os
        if not os.path.exists(loc):
            os.makedirs(loc)
        for lab in self.get_mats().keys():
            sup = [k for supp in self.supp_data if supp in self.keys() for k in self.keys()[supp] if lab in k]
            eph_cols = list(self.keys()['eph'])
            mat_cols = list(self.keys()[lab])
            cols = eph_cols+sup+mat_cols
            # headder = ''
            # for col in [eph_cols,sup,mat_cols]:
            #     for c in col:
            #         if lab not in c:
            #             headder += 'c[1]headderf

            fmts = {
                    'sep':'\t',
                    'na_rep':'NAN',
                    # 'float_format':'%.6f'
                    }
            if splitby != None:
                splitter = (self.dependent_df,splitby)

                def print_func(x):
                    if split_folders:
                        split_val = reduce_func(x[splitter][0]).astype(print_type)
                        split_loc = loc+'/%s/'%str(split_val)
                        if not os.path.exists(split_loc):
                            os.makedirs(split_loc)
                    else:
                        split_loc = loc
                    x.to_csv(split_loc+'ISN_hist_%s_%s_%s.txt'%(splitby,
                                                str(split_val),
                                                  lab),**fmts)
                self.df[cols].groupby(
                        reduce_func(self.df[splitter])).apply(print_func)
            else:
                self.df[cols].to_csv(loc+'ISN_hist_%s.txt'%lab,**fmts)