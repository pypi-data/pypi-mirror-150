from pykingas import KineticGas, suppress_stdout, bcolors
import numpy as np
import sys

# Exit codes 1***
# Second digit identifies potential mode
# Third digit identifies test loop, fourth digit identifies loop iteration

FLT_EPS = 1e-12

def run_test(do_plot=False, do_print=False):
    control_value_dict = {'HS' : {'No_BH' : [[-0.5161629180776952 , 0.5161629180776952],
                                           4.645041206823456e-05, -5.034955850200782e-06,
                                            0.02598758965504002],
                                  'BH' : [[-0.5298208409698769 , 0.5298208409698769 ],
                                          5.86506545292918e-05, -6.525611212290054e-06,
                                          0.03174164264057401]},
                          'mie' : {'No_BH' : [[-0.33300911952977325, 0.33300911952977325],
                                              6.108716788890306e-05 , -4.271942638582721e-06 ,
                                              0.030399198798366923],
                                   'BH' :  [[-0.3401923180799464, 0.3401923180799464],
                                            7.701799287938923e-05, -5.502195201615889e-06,
                                            0.03711818358242925]}}

    comps = 'HE,AR'
    T = 300
    x = [0.3, 0.7]
    Vm = 24e-3

    potentials = ['HS', 'mie']
    N_list = [4, 1]
    r = 0
    for potential_idx, potential in enumerate(potentials):
        kingas = KineticGas(comps, BH=False, potential=potential)
        # Compute some values
        with suppress_stdout('-silent' in sys.argv):
            alpha_T0 = kingas.alpha_T0(T, Vm, x, N=N_list[potential_idx])
            D12 = kingas.interdiffusion(T, Vm, x, N=N_list[potential_idx])
            DT = kingas.thermal_diffusion(T, Vm, x, N=N_list[potential_idx])
            thermal_cond = kingas.thermal_conductivity(T, Vm, x, N=N_list[potential_idx])

        vals = [alpha_T0, D12, DT, thermal_cond]
        vals_control =  control_value_dict[potential]['No_BH'] # Precomputed values to check that output has not changed
        for i, (val, valc) in enumerate(zip(vals, vals_control)):
            if r != 0:
                break
            if any(abs(np.array([val]).flatten() - np.array([valc]).flatten()) > FLT_EPS):
                r, v = 100 * potential_idx + i + 1, tuple(np.array([val]) - np.array([valc]))

        # Compute values without saving to variables, with different BH-setting
        with suppress_stdout('-silent' in sys.argv):
            alpha_T0_BH = kingas.alpha_T0(T, Vm, x, BH=True, N=N_list[potential_idx])
            D12_BH = kingas.interdiffusion(T, Vm, x, BH=True, N=N_list[potential_idx])
            DT_BH = kingas.thermal_diffusion(T, Vm, x, BH=True, N=N_list[potential_idx])
            thermal_cond_BH = kingas.thermal_conductivity(T, Vm, x, BH=True, N=N_list[potential_idx])

        vals = [alpha_T0_BH, D12_BH, DT_BH, thermal_cond_BH]
        vals_control = control_value_dict[potential]['BH']
        for i, (val, valc) in enumerate(zip(vals, vals_control)):
            if r != 0:
                break
            if any(abs(np.array([val]).flatten() - np.array([valc]).flatten()) > FLT_EPS):
                r, v = 100 * potential_idx + 10 + i + 1, tuple(np.array([val]) - np.array([valc]))

        if do_print is True:
            print('\n\nMixture is :', comps)
            print('T =', T, 'K')
            print('rho =', 1e-3 / Vm, 'kmol/m3')
            print('x =', x)
            print()
            print('alpha_T =', alpha_T0[0], alpha_T0[1])
            print('D12 =', D12, 'mol / m s')
            print('D_T = ', DT, 'mol / m s')
            print('k =', thermal_cond, 'W / m K')
            print()
            print('alpha_T_BH =', alpha_T0_BH[0], alpha_T0_BH[1])
            print('D12_BH =', D12_BH, 'mol / m s')
            print('D_T_BH = ', DT_BH, 'mol / m s')
            print('k_BH =', thermal_cond_BH, 'W / m K')

        # Recompute the first values, check that they are the same as before.
        with suppress_stdout('-silent' in sys.argv):
            if any(abs(alpha_T0 - kingas.alpha_T0(T, Vm, x, N=N_list[potential_idx])) > FLT_EPS) and r == 0:
                r = 100 * potential_idx + 21
            elif abs(D12 - kingas.interdiffusion(T, Vm, x, N=N_list[potential_idx])) > FLT_EPS and r == 0:
                r = 100 * potential_idx + 22
            elif abs(DT - kingas.thermal_diffusion(T, Vm, x, N=N_list[potential_idx])) > FLT_EPS and r == 0:
                r = 100 * potential_idx + 23
            elif abs(thermal_cond - kingas.thermal_conductivity(T, Vm, x, N=N_list[potential_idx])) > FLT_EPS and r == 0:
                r = 100 * potential_idx + 24

    if r != 0:
        r += 1000
        print(f'{bcolors.FAIL}Python test failed with exit code :', r, f'{bcolors.ENDC}')
    else:
        print(f'{bcolors.OKGREEN}Python test was successful!{bcolors.ENDC}')
    if '-debug' in sys.argv or '-d' in sys.argv:
        return 0 # For some reason, the output computed by the debug build is slightly different from release build (error is after 8th decimal place)

    return r