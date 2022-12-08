import numpy as np
import pandas as pd
from ipywidgets import *


FILTERZ = {
           'Equal To':lambda x,y: np.equal(x,y),
           'Not Equal':lambda x,y:np.not_equal(x,y),
           'Greater Than': lambda x,y:np.greater_equal(x,y),
            'Less Than':lambda x,y:np.less_equal(x,y),
           'Contains (str)':lambda x,y: x.str.contains(y,na = False)
          }

def button_gen(label,button_func,button_inputs = []):
    button = widgets.Button(description=label)
    output = widgets.Output()

    display(button, output)
    button.f_out = []

    def on_button_clicked(b):
        with output:
            button.f_out.append(button_func(*button_inputs))

    button.on_click(on_button_clicked)
    return(button)

def filter_selector(df_in,group_keys = None):
    df  = df_in.reset_index()
    if not group_keys: 
        group_keys = df.keys()
    def int_call(f,append_menu = [],
                         manual = False,
                         append_func = None,
                        finp = {}):
        thing = interactive(f,{'manual': manual},**finp)
        display(thing)
        append_menu.append(append_func(thing) if append_func != None else thing)
        return(thing)
    
    def nfunc_button(selector,menu):
        p_button = button_gen('+',int_call,[selector])
        menu.append(list(p_button.f_out)[:-1])
        return(p_button)
    
    def add_filter_button(famly,group_keys):
        # Function to generate logical filter for pandas df using gui interacts
        
        fam = {}
        def log_red(Selector = { 'and':np.logical_and.reduce,
                                'or':np.logical_or.reduce,
                               'nor':np.logical_xor.reduce,
                               'not':np.logical_not.reduce},
                       fam = fixed(fam),Pick_Value = True):

            def plus_menu_button(Selector,group_keys,children,Pick_Value):
                siblings = {'menu':{}}
                
                def selector(Group = group_keys,
                                 Filter = FILTERZ,
                                 siblings = fixed(siblings),
                                 reducer = fixed(Selector),
                                 Pick_Value = fixed(Pick_Value)):
                    
                    if Pick_Value:
                        val = df[Group].dropna().unique()
                    else:
                        if np.issubdtype(df[Group].dtype, np.number):
                            val = FloatText()
                        else:
                            val = ''
                        
                    def val_pick(Value = val,
                                     Filter = fixed(Filter),
                                     siblings = fixed(siblings),
                                         group = fixed(Group)):
                        siblings['bool'] = Filter(df[group],Value)
                    menu = int_call(val_pick)
                    siblings['menu'][menu.children[0].description] = menu.children[0]
                    return(menu)

                menu = interactive(selector)
                display(menu)

                for thing in menu.children[:-1]:
                    siblings['menu'][thing.description] = thing
                children.append(siblings)
                return(menu)
            
            fam['children'] = []
            plus_button = button_gen('+',plus_menu_button,
                            [Selector,group_keys,fam['children'],Pick_Value])
            return(plus_button.f_out)
        filt_top = int_call(log_red)
        fam['parents'] = filt_top.children[0]
        famly.append(fam)
        return(filt_top)
    famly = []
    filts = []
    
    filt_button = button_gen('Add Filter',add_filter_button,
                                     [famly,group_keys])
    
    def apply_button(fams,close_stuff = [],filts = [],des = ''):

        for fam in fams:
            parent = fam['parents']
            des += '\n%s  \n{'%parent._options_labels[parent.index]
            fam_filt = []
            for sib in fam['children']:
                fam_filt.append(sib['bool'])
                labs = {}
                for l,s in sib['menu'].items():
                    if type(s) == Dropdown:
                        labs[l] = s._options_labels[s.index]
                    else:
                        labs[l] = s.value
#                     labs[l] = s.value
                des += '\n   %s %s %s(%s),'%(
                                            labs['Group'],labs['Filter'],
                                             type(labs['Value']).__name__,
                                             str(labs['Value'])
                                            )
            des+='\n  }'
            filts.append(parent.value(fam_filt))
            
        descriptor_display.value = des.replace('\n','<br>')
        
        fams = []
        for c in close_stuff:c.close()
    
    descriptor_display = HTML()
    descriptor_txt = 'Filters Generated:'
    apply_button = button_gen('Apply',
                                apply_button,
                              [famly,filt_button.f_out,filts,
                               descriptor_txt])
    display(descriptor_display)
    
    def clear_button(famly,filt,display_descript,descriptor):
        famly.clear()
        filt.clear()
        descriptor = 'Filters Generated:'
        display_descript.value = descriptor
        
    clear_button = button_gen('Clear Filters',
                                  clear_button,
                                  [famly,filts,descriptor_display,descriptor_txt])

    return(filts,descriptor_display)
    