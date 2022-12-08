import numpy as np
import pandas as pd


def get_headder(fil):
    hct = 0
    head = []
    with open(fil) as l:
        for ll in l.readlines():

            if ll.strip():
                if '#' in ll:    
                    hs = ll.strip().strip('#').strip(':')
                    if hs:
                        head = []
                        if 'met' in hs.lower():
                            for h in hs.split(' '):
                                if h:head.append(h)
                else:
                    break
                
                hct+=1
    if head and 'met' in head[0].lower():
        head[0]= 'time'
    return(head)

def get_line_loc(fil,end_str,count_blanks = True):
    with open(fil,'r') as f:
        i = -1
        l = ''
        while end_str not in l:
            l = f.readline()
            # print(l)
            if count_blanks or l.strip():
                i+=1
    return(i)


def import_good_times(fil):
    lines = []
    if fil =='LoGoodTimes.txt':
        header = ['orbit','Start Time','Stop Time',
                    'NEP Start','NEP End','Hi/Lo']+list('E%d'%n for n in range(1,9))
    else:
        header = open(fil,'r').read().split('#')[-1].split('\n')[0].split('\t')
    arr = pd.read_csv(fil,delim_whitespace = True,
                      comment = '#',header = None)

    head_out = []
    for h in header:
        head_out.append(h.replace('begin_GPS','Start Time').replace('end_GPS','Stop Time').strip().strip('/arc'))
    arr.columns = head_out
    if type(arr['orbit'].values[0])==str:
        int_orb = arr['orbit'].str.strip('a').str.strip('b').astype(int)
        arr.drop('orbit',axis = 1,inplace = True)
        arr['orbit'] = int_orb

    if 'NEP Start' not in arr: 
        arr['NEP Start'] = np.zeros(len(arr.values))
        print("Auto Generated NEP Start Range")
    if 'NEP End' not in arr: 
        arr['NEP End'] = np.ones(len(arr.values))*60
        print("Auto Generated NEP Stop Range")
    return(arr)



def load_me_show(f):
    cols = get_headder(f)

    return(pd.read_csv(f,delim_whitespace = True,header = None,
                    comment = '#',names = (cols if cols else None)))


def load_df(path,estep=None,dtype = '.txt',
                            head = None,
                            usecols = None,
                            use_labs = None,
                            calc_nep = False,
                            orbit_range = [0,np.inf],
                            True_square = False,
                            w = 'auto',
                            accum_duplicates = 'integrate',
                            dt_multiplier = 8,use_steps = 'all'):

    import glob

    # Get the database file 

    if type(estep) == list:
        fils = []
        for e in estep:
            ftype = "*e%s%s"%(str(e),dtype)
            fils+=glob.glob(path +ftype)
    elif type(estep) == int:
        ftype = "*e%d%s"%(estep,dtype)
        fils = glob.glob(path + ftype)
    else:
        ftype = "*%s%s"%(str(estep),dtype)
        fils = glob.glob(path + ftype)
    # return(fils)

    # check the files over to see if the orbitsa are split or not
    from pathlib import Path
    import re
    orbit_fils = {'orbit':[],
                  'orbit_arc':[],
                  'arc': [],
                  'estep':[],
                  'fils':[],
                  'fsize':[],
                  }
    for f in fils:
        if '-' not in f:
            orbit_arc = f.split('\\')[-1].split('o')[1].split('_')[0]
            orbit = float(orbit_arc.strip('a').strip('b'))
            arc = re.sub('[0-9]+', '', orbit_arc)
            # if orbit not in orbit_fils:
            #     orbit_fils[orbit] = {'arc':[orbit_arc],
            #                         'fils':[f],

            #                         'fsize':[Path(f).stat().st_size]}
            # else:
            #     orbit_fils[orbit]['arc'].append(orbit_arc)
            #     orbit_fils[orbit]['fils'].append(f)
            #     orbit_fils[orbit]['fsize'].append(Path(f).stat().st_size)
            # head = np.array(get_headder(f))
            # if 'ch' in head:
            estep = f.split('_')[-1].split('.')[0]
            # estep = np.loadtxt(f,dtype = str,comments = '#',
            #                    max_rows = 1,usecols = 3)
            orbit_fils['estep'].append(estep)
            orbit_fils['orbit'].append(orbit)
            orbit_fils['orbit_arc'].append(orbit+(.5 if 'b' in orbit_arc else 0))
            orbit_fils['arc'].append(arc)
            orbit_fils['fils'].append(f)
            orbit_fils['fsize'].append(Path(f).stat().st_size)
    # return(pd.DataFrame(orbit_fils))
    orbit_fils = pd.DataFrame(orbit_fils)
                 
    

    # Remove orbits with out arc separation for file splitting
    def orb_selector(df):
        arc_fils = np.logical_or.reduce([df['arc'].str.contains(val) for val in ['a','b']])
        if np.any(arc_fils):
            return(df.loc[arc_fils])
        else:
            return(df)
    orbit_fils = orbit_fils.groupby(['orbit'],as_index = False).apply(orb_selector)
    # return(orbit_fils)

    if use_steps =='all':
        g_fils = orbit_fils['fils'].values
    elif use_steps == 'unique_times':
        def fil_select(df):
            fil_pick = ~df['estep'].str.strip('e').str.isnumeric()
            fil_pick[np.argmax(df['fsize'].values)] = True
            return(df.loc[fil_pick])
        # g_fils = orbit_fils.groupby(['orbit_arc'],as_index = False).apply(lambda x:x.loc[x['fsize'].idxmax()])['fils'].values
        g_fils = orbit_fils.groupby(['orbit_arc'],as_index = False).apply(fil_select)['fils'].values
    # return(g_fils)
            # arc_fils = []
            # arc_size = []
            # for arcs,fil,size in zip(orb_fils['arc'],orb_fils['fils'],orb_fils['size']):
            #     if 'a' in arcs or 'b' in arcs:
            #         arc_fils.append(fil)
            #         arc_size.append(size)
            #     elif not split:
            #         arc_fils.append(fil)
            #         arc_size.append(size)

            # arcs = np.array(orb_fils['arc'])

            # for large_fil in 
            # g_fils.append()

    # return(g_fils)

    from ipywidgets import IntProgress,Output
    from IPython.display import display

    out = Output()
    lb = IntProgress(min=0, max=len(g_fils)) # instantiate the bar
    display(lb) # display the bar
    display(out)
    lb.value = 0
        
    li = []
    orb = []
    orbit_fails = ''
    fail = 0
    for f in g_fils:
        if '-' not in f:
            orbit_arc = f.split('\\')[-1].split('o')[1].split('_')[0]
            orbit_int = float(orbit_arc.strip('a').strip('b'))+(.5 if 'b' in orbit_arc else 0)
            if orbit_int >orbit_range[0] and orbit_int<orbit_range[1]:
                # print(orbit_arc)
                try:
                    if head == 'auto' and not usecols:
                        cols = get_headder(f)
                    elif head=='auto' and usecols:
                        cols = list(get_headder(f)[c] for c in usecols)
                    elif type(head)==list and usecols:
                        cols = list(head[c] for c in usecols)
                    elif head:
                        cols = head
                    else: cols = None

                    l = pd.read_csv(f,delim_whitespace = True,header = None,
                                    comment = '#',names = (cols if cols else None),
                                        usecols = usecols)
                    if use_labs != None:
                        l = l[use_labs]

                    # Define exception to convert 'en' column to 'ch'
                    if 'en' in l:
                        l['en']  = l['en'].astype(str)

                    orb=[orbit_int]*l.shape[0]
                    arc=[orbit_arc[-1]]*l.shape[0]

                    for nam,val in zip(['arc','orbit'],[arc,orb]):
                        l.insert(1,nam,val)
                    if not l.empty:


                        if calc_nep == True:
                            l.insert(4,'nep',phase_to_nep(l['phase'].values))
                        if accum_duplicates=='integrate':
                            l = accum_duplicate_times(l,dt_multiplier = dt_multiplier)
                        elif accum_duplicates == 'drop':
                            l = l.groupby(['time','phase']).head(1)


                        if True_square:
                            dif_p = np.diff(l['phase'].values)
                            dif_m = np.median(dif_p[dif_p>0])
                            loc = dif_p>2*dif_m
                            tloc = np.logical_or.reduce([np.append(loc,loc[-1]),np.insert(loc,0,loc[0])])
                            l = l[~tloc]

                        if not True_square or len(l)%(len(np.unique(l['phase'])) if w == 'auto' else w) ==0:
                            li.append(l)
                        else:
                            print('Orbit: %s,: Not Square!'%orbit_arc)
                        del(l)

                    else:
                        print(cols)
                        print(head)
                except(pd.errors.EmptyDataError,IndexError):
                    if fail == 0:
                        out.append_stdout('E%s Import Failed [EmptyDataError] on Orbits: \n'%f.split('.')[0][-1])
                    out.append_stdout('%s,'%orbit_arc)
                    fail+=1

                    orbit_fails+='%s, '%orbit_arc
        lb.value +=1

    lb.close()
    # return((pd.concat(li) if len(li)>= 1 else pd.DataFrame()).sort_values(['time']))

    return((pd.concat(li) if len(li)>= 1 else pd.DataFrame()))


def accum_duplicate_times(df_hist,dt_multiplier = 8,
                                        phase_steps = 60,
                                        spin_av = 14.37126):
    # inputs pandas df, accumulates counts in redundant time bins,
    # calculates dt

    df_acc = df_hist.copy()

    # define parameter to calculate individual bin exposure time
    df_acc['dt'] = np.ones(df_acc.shape[0])
    
    # accumulate counts and exposure time of duplicate timesteps
    df_acc[['count','dt']] = df_acc.groupby(['time','phase'])['count','dt'].transform('sum')

    # drop redundant duplicates
    df_acc.drop_duplicates('time',inplace = True)

    delt = np.diff(df_acc['time'])/np.diff(df_acc['phase'])/phase_steps
    tbin = np.nanmedian(delt[np.diff(df_acc['phase'])>0])
    dt_av = pd.Series(np.append(delt,tbin),
                        ).rolling(window = 31,center = True).median().values
    dt_av[np.isnan(dt_av)] = tbin
    dt_av[abs(dt_av-spin_av/phase_steps)>spin_av/phase_steps*.05] = spin_av/phase_steps
    # if tbin>10:
        # print(tbin)
    # dif_down = np.insert(np.diff(df_acc['time']),0,tbin)


    # dt_av = np.median(np.diff(df_acc['time']))
    df_acc['dt'] = (df_acc['dt']*dt_av*dt_multiplier)#.round(8)
    
    # Define the orbit number as a float to differentiate arc
    # Need to move else where in analysis 
    # orb = df_acc['orbit'].values.astype(float)
    # orb[df_acc['arc']=='b'] += .5
    # df_acc['orbit'] = orb
    return(df_acc)



def phase_to_nep(phase,instrument = 'lo'):
    nep = 360*(phase+(.5 if instrument == 'lo' else 0))-3
    nep[nep>=357] = nep[nep>=357]-360
    return(nep.astype(float).round())



