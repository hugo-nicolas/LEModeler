import sys


def foil_parameters(filename='..\\input_parameters.txt'):
    try:
        f = open(filename, 'r+')
    except IOError as e:
        print('Unable to open de file\n', e)
        sys.exit()
    L_values, L_sections, L_extension, L_isSymmetric, L_closeRhino = [], [], [], [], []
    for el in f.readlines():
        el_split = el.split('=')
        if len(el_split) == 2:
            try:
                float(el_split[1])
                L_values.append(float(el_split[1]))
            except:
                if str(el_split[0]).strip(' ') == 'extension':
                    L_extension.append(str(el_split[1]).strip('\n '))
                elif str(el_split[0]).strip(' ') == 'symmetric':
                    L_isSymmetric.append(str(el_split[1]).strip('\n '))
                elif str(el_split[0]).strip(' ') == 'close':
                    L_closeRhino.append(str(el_split[1]).strip('\n '))
                else:
                    if str(el_split[0]).strip(' ') not in ['wing','stab','mast','fuselage']:
                        L_sections.append(str(el_split[1]).strip('\n '))
    return L_values, L_sections, L_extension, L_isSymmetric, L_closeRhino
