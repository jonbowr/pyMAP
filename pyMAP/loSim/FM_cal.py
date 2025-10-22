
import simPyon as sp

def sim_h2_dispersion(n,mean = 100,fwhm = 50):
    
    def e_diss(E0,Ed = 4.52,pm = 1,alpha = 0):
        return(E0/2+Ed/2+pm*np.sqrt(E0*Ed)*np.cos(alpha))

    E0 = sp.particles.source('gaussian',{'fwhm': fwhm,'mean': mean})(n)
    alpha = sp.particles.source('cos')(n)*np.pi/180
    pm = np.round(np.random.rand(n))*2-1
    return(e_diss(E0,Ed = 4.52,pm = pm,alpha = alpha))


def set_simulator_cal(sim, result = 'fin_cal_H_2'):
    '''
    Function to setup instrument scattering simulator to calibrated values from FinalCal

    Options:
        result:
            'fin_cal_H_1': 
            'fin_cal_H_2': 
            'fin_cal_H_3': 
    '''


    def fin_cal_H_1(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal, 12/16/2024
        - model regression performed primarily against final cal results, 20241212-FMv3_T105_PSPL_FinalCal_DER.csv
        - model checked against IBEX-lo H final cal results and precal2 results
        - see 20241204_FinalCal_DER1 H Model Comparison.ipynb for exact definition
        '''
          
        sim[1].part['surf_binding'] = .25
        sim[1].part['sputtering'] = .2
        sim.params['cs_scatter']['ke']['pdf']['b'] = .3
        sim[1].effic.p0 =sim[1].cal_fits['effic']['He'].p0*.0968*.68

        sim[1].scatter_type = 'inelastic'
        sim[1].ke['modulator_f'] = make_f_eloss()[1]
        return(sim)


    def fin_cal_H_2(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        - model regression performed primarily against final cal results, 20241219-FMv3_T105_PSPL_FinalCal_DER.csv
            - also possibly agains 20241220
        - model checked against IBEX-lo H final cal results and precal2 results
        - see 20241204_FinalCal_DER1 H Model Comparison.ipynb for exact definition
        '''
        from numpy import array
        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .2
        sim.params['cs_scatter']['ke']['pdf']['b'] = .3
        sim[1].effic.p0 =array([0.00721197/.8, 0.19172372*.8])*.9

        sim[1].scatter_type = 'inelastic'
        sim[1].ke['modulator_f'] = make_f_eloss()[1]
        
        sim[1].theta['modulator_f'].p0 = array([0.92923537, 2.        , 0.1530386 ])
        sim[1].phi['modulator_f'].p0 = array([ 1.16825037, 36.99865872,  0.22471439])
        return(sim)

    def fin_cal_H_3(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        - model regression performed primarily against final cal results, 20250324-FMv3_T105_PSPL_FinalCal_DER.csv
            - regression performed against parameter: 'eDE_SILVER_H_CS_H2fix'
        - model checked against IBEX-lo H final cal results and precal2 results
        - see 20241204_FinalCal_DER1 H Model Comparison.ipynb for exact definition
        '''
        from numpy import array
        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .2
        sim.params['cs_scatter']['ke']['pdf']['b'] = .3
        sim[1].effic.p0 =array([0.00721197/.8, 0.19172372*.8])*.9*.438*.84716

        sim[1].scatter_type = 'inelastic'
        sim[1].ke['modulator_f'] = make_f_eloss()[1]
        

        sim[1].theta['modulator_f'].p0 = array([0.92923537, 2.        , 0.1530386 ])
        sim[1].phi['modulator_f'].p0 = array([ 1.16825037, 36.99865872,  0.22471439])
        return(sim)


    def spot_cal_H_4(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        '''
        from numpy import array
        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .2
        sim.params['cs_scatter']['ke']['pdf']['b'] = .3
        sim[1].effic.p0 =sim[1].cal_fits['effic']['H'].p0

        sim[1].scatter_type = 'inelastic'
        sim[1].ke['modulator_f'] = make_f_eloss()[1]
        
        sim[1].theta['modulator_f'].p0 = sim[1].cal_fits['theta']['O'].p0#array([ 1.16825037, 36.99865872,  0.22471439])*1.2
        sim[1].phi['modulator_f'].p0 = sim[1].cal_fits['phi']['O'].p0#array([ 1.16825037, 36.99865872,  0.22471439])*1.2
        return(sim)


    def fin_cal_O_0(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        - model regression performed primarily against final cal results, 20250331-FMv3_T105_PSPL_FinalCal_DER.csv
            - regression performed against parameter: 'eDE_SILVER_O_ESA_CS'
        - Fit regresssion can be seen in '20250331_FinalCal_DER1 O Model Regression.ipynb'
            - results are stored in 
        '''
        from numpy import array
        from bowPy import Jonda
        sim.source['mass'] = 16
        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .3
        sim.params['cs_scatter']['ke']['pdf']['b'] = .45
        
        sim[1].effic = Jonda(xy_data = sim[1].effic.xy,func = 'power_law')

        H_off = 211.12*.55
        sim[1].effic.p0 = [1.67664469e-05*H_off*2, 1.58156040e+00, 5.11102927e-05*H_off, 3.59291274e+00]
        sim[1].effic.f = sim[1].effic.func
        # sim[1].effic.p0 =array([ 0.0002274 , -0.00335699])*400*1.23

        sim[1].scatter_type = 'inelastic'

        sim[1].ke['modulator_f'].p0 = [-0.0019832,0.76422464*.9]
        
        # sim[1].theta['modulator_f'].p0 = array([0.92923537, 2.        , 0.1530386 ])
        # sim[1].phi['modulator_f'].p0 = array([ 1.16825037, 36.99865872,  0.22471439])
        return(sim)

    def fin_cal_O_1(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        - model regression performed primarily against final cal results, 20250331-FMv3_T105_PSPL_FinalCal_DER.csv
            - regression performed against parameter: 'eDE_SILVER_O_ESA_CS'
        - Fit regresssion can be seen in '20250331_FinalCal_DER1 O Model Regression.ipynb'
            - results are stored in 
        '''
        from numpy import array
        from bowPy import Jonda
        sim.source['mass'] = 16
        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .3/5 # for sake of energy response sputtered H wont show up, so we should
        sim.params['cs_scatter']['ke']['pdf']['b'] = .3
        
        sim[1].effic = Jonda(xy_data = sim[1].effic.xy,func = 'power_law')

        H_off = 211.12*.55
        sim[1].effic.p0 = [ 2.91021338e-07*H_off*2,  2.75855908e+00,  5.00000000e-05*H_off, -1.00000000e-01]
        sim[1].effic.f = sim[1].effic.func
        # sim[1].effic.p0 =array([ 0.0002274 , -0.00335699])*400*1.23

        # sim[1].scatter_type = 'inelastic'

        sim[1].ke['modulator_f'].p0 = [-0.0019832,0.76422464*.95]
        return(sim)

    def fin_cal_O_2(sim):
        '''
        Simulator settings defined following IMAP-Lo FM cal
        - model regression performed primarily against final cal results, 20250331-FMv3_T105_PSPL_FinalCal_DER.csv
            - regression performed against parameter: 'eDE_SILVER_O_ESA_CS'
        - Fit regresssion can be seen in '20250331_FinalCal_DER1 O Model Regression.ipynb'
            - results are stored in
        - same as fin-cal01, but now I'm not assuming that the energy dispsersion is being caused by  beam and background 
        '''
        from numpy import array
        from bowPy import Jonda
        sim.source['mass'] = 16
        sim[0].source['mass'] = 16
        sim[2].source['mass'] = 16

        sim[1].part['surf_binding'] = .1
        sim[1].part['sputtering'] = .3/4.4 # for sake of energy response sputtered H wont show up, so we should
        # sim.params['cs_scatter']['ke']['pdf']['b'] = .2
        sim[1].ke['pdf'].kwargs = {'c':-.075,'b':.405*2**1.6,'k':3}
        
        sim[1].effic = Jonda(xy_data = sim[1].effic.xy,func = 'power_law')

        H_off = 211.12*.55
        # sim[1].effic.p0 = [ 2.91021338e-07*H_off*2,  2.75855908e+00,  5.00000000e-05*H_off, -1.00000000e-01]
        sim[1].effic.p0 = [ 1.23873235e-05*H_off*2,  1.59737600e+00,  1.68663966e-05*H_off, 1.00000000e-01]
        sim[1].effic.f = sim[1].effic.func
        
        # sim[1].effic.p0 =array([ 0.0002274 , -0.00335699])*400*1.23

        # sim[1].scatter_type = 'inelastic'
        sim[1].ke['modulator_f'].p0 = [-0.0019832*.82,0.76422464*.82]
        return(sim)

    dict_cals = {
                'fin_cal_H_1': fin_cal_H_1,
                'fin_cal_H_2': fin_cal_H_2,
                'fin_cal_H_3': fin_cal_H_3,
                'fin_cal_O_0': fin_cal_O_0,
                'fin_cal_O_1': fin_cal_O_1,
                'fin_cal_O_2': fin_cal_O_2,
                'spot_cal_H_4':spot_cal_H_4,
                }

    return(dict_cals[result](sim))


def make_f_eloss():
    '''
     energy loss funciton defined following final cal 12/16/2024
     energy loss here defined in addition to inellastic scattering loss processes
    '''
    import pandas as pd
    from .cs_cal import get_vperp
    eloss_vals = pd.DataFrame([0.82809887]*7 ,index = range(1,8),columns = ['Eloss'])

    from .esa_cs_const import cent_eng

    eloss_vals['ke'] = cent_eng
    eloss_vals['v_perp'] = get_vperp(1,eloss_vals['ke'],15)
    # Eloss defined 12/11/2024
    eloss_run0 = pd.Series({3 : 0.866685,
                            4 :  0.946218,
                            5 :  0.977120,
                            6 :  1.029214,
                            7:  0.950984})
    eloss_vals['eloss_1']=eloss_run0*eloss_vals['Eloss']
    #second run using polyfit of eloss values
    eloss_vals['eloss_2'] = pd.Series({3 :   0.698561,
                                        4:    0.786205,
                                        5:    0.784077,
                                        6:    0.886756,
                                        7:    0.777787})
    from pyMAP.bowPy import Jonda
    f_eloss_new =Jonda(xy_data = eloss_vals[['v_perp','eloss_2']].dropna().values.T)
    f_eloss_new.interp_xy('cubic',sigma = .9,bounds_error = False,interp_input = {'fill_value':'extrapolate'})
    
    return(eloss_vals,f_eloss_new)

def grids_n_spokes(instrument_config = 'IMAP_flight'):
    '''
    Function to get dict of grid/spoke trans
    Options:
        'IMAP_flight': 
        'IMAP_finCal':
        'IMAP_preCal2':
        'IBEX_finCal':
        'IBEX_flight':
    '''
    from pandas import Series
    g_spokes = {
            'IMAP_flight':{
                            'coll_trans':1,
                            'p10_trans':.85,
                            'tof_trans': .68,
                            'p2_trans': .9363,
                            },
            'IMAP_finCal':{
                            'coll_grid':.694,
                            'p10_trans':.85,
                            'tof_trans': .68,
                            'p2_grid': 1,
                            },
            'IMAP_preCal2':{
                            'coll_grid':1,
                            'p10_trans':.85,
                            'tof_trans': .68,
                            'p2_grid': 1,
                            },
            'IBEX_finCal':{
                            'coll_grid':.67,
                            'coll_grnd_grid':.9,
                            'p2_grid': .855,
                            'p10_Trans':.83,
                            'tof_trans':.5504,
                            },
            'IBEX_flight':{
                            'coll_grnd_grid':.9,
                            'p2_grid': .855,
                            'p10_Trans':.83,
                            'tof_trans':.5504
                            }
                
                }
    return(Series(g_spokes[instrument_config]))

def get_mcp_gain(species = 'H2'):
    '''
    import silver triple mcp gain curve function for a given species. 
    - MCP gain curves loaded from 20241218_T105_FinalCal_MCP_Gain.pkl. 
    - Gian curves generated from final cal data in 20241218_T105_FinalCal_MCP_Gain.ipynb
    
    Input:
        species [str]: calibration species for gain curve
        Options:
            'D/H2'
            'H2'
            'He'
            'O'
    Output:
        Jonda: cubic interpolation of averaged and smoothed gain curve measurements
    '''

    from pandas import read_pickle
    from os.path import dirname,join
    lpath = dirname(__file__)
    for up in range(2):
        lpath = dirname(lpath+'..')

    f_data = join(lpath,"cal/cal_results/20241218_T105_FinalCal_MCP_Gain.pkl")
    return(read_pickle(f_data)[species])


def get_inst_response(species = 'H'):
    '''
    import instrument energy response funciton calibcated from final cal. 
    - Response functions loaded from fin_cal1_H_KE_Response.pkl. 
    
    Input:
        species [str]: calibration species for gain curve
        Options:
            'D/H2'
            'H2'
            'He'
            'O'
    Output:
    '''

    # from pandas import read_pickle
    from pandas import read_csv
    from os.path import dirname,join
    lpath = dirname(__file__)
    for up in range(2):
        lpath = dirname(lpath+'..')

    if species == 'H':
        f_data = join(lpath,"cal/cal_results/20250326-FMv3_T105_PSPL_FinalCal_DERH_Response.csv")
        from pandas import read_pickle
        return(read_pickle(f_data.replace('.csv','.pkl')))
    elif species == 'O':
        f_data = join(lpath,"cal/cal_results/20250331-FMv3_T105_PSPL_FinalCal_DERO_Response.csv")
    # return(read_pickle(f_data))
    return(read_csv(f_data))