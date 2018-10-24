import E6BCore
import PySimpleGUI as sg
import sys
import math

# intialize the e6b calculator
e6b = E6BCore.E6BCore()

# frame for the aircraft type setting
frame_ty = sg.Frame(layout = [[sg.Text('Aircraft type:', size = (20, 1)), sg.InputCombo(('C172R'), key = 'aircraft_type', size = (40, 1))],
                              [sg.ReadButton('Load', key = 'load', size = (15, 1))]], 
                    title = 'Aircraft', relief = sg.RELIEF_SUNKEN)
frame_alt = sg.Frame(layout = [[sg.Text('Indicated alt.:', size = (10, 1)), sg.InputText('0', key = 'altitude_ind', size = (10, 1), do_not_clear = True), 
                                sg.Text('Alt. setting :', size = (15, 1), justification = 'right'), sg.InputText('29.92', key = 'altimeter', size = (10, 1), do_not_clear = True),
                                sg.Text('Temperature (C):', size = (20, 1), justification = 'right'), sg.InputText('15', key = 'temperature', size = (10, 1), do_not_clear = True),
                                sg.Text('KIAS:', size = (12, 1), justification = 'right'), sg.InputText('100', key = 'kias', size = (10, 1), do_not_clear = True)],
                               [sg.Text('Pressure alt.:', size = (10, 1)), sg.Text('1000', key = 'altitude_pressure', size = (10, 1)), 
                                sg.Text('Density  alt.:', size = (14, 1), justification = 'right'), sg.Text('1000', key = 'altitude_density', size = (10, 1)),
                                sg.Text('KTAS:', size = (19, 1), justification = 'right'), sg.Text('1000', key = 'ktas_out', size = (10, 1))],
                               [sg.ReadButton('Calculate', key = 'calcAltitude', size = (15, 1))]],
                     title = 'Altitude', relief = sg.RELIEF_SUNKEN)
frame_wind = sg.Frame(layout = [[sg.Text('Wind dir.:', size = (10, 1)), sg.InputText('0', key = 'wind_direction', size = (10, 1), do_not_clear = True), 
                                 sg.Text('Wind spd:', size = (15, 1), justification = 'right'), sg.InputText('0', key = 'wind_speed', size = (10, 1), do_not_clear = True),
                                 sg.Text('KTAS:', size = (20, 1), justification = 'right'), sg.InputText('0', key = 'ktas_in', size = (10, 1), do_not_clear = True),
                                 sg.Text('True course:', size = (12, 1), justification = 'right'), sg.InputText('0', key = 'true_course', size = (10, 1), do_not_clear = True)],
                                [sg.Text('WCA:', size = (10, 1)), sg.Text('0', key = 'wca', size = (10, 1)), 
                                 sg.Text('True HDG:', size = (14, 1), justification = 'right'), sg.Text('1000', key = 'true_heading', size = (10, 1)),
                                 sg.Text('Ground spd:', size = (19, 1), justification = 'right'), sg.Text('1000', key = 'ground_speed', size = (10, 1))],
                                [sg.ReadButton('Calculate', key = 'calcWindCorr', size = (15, 1))]],
                      title = 'Wind correction', relief = sg.RELIEF_SUNKEN)
frame_flt = sg.Frame(layout = [[sg.Text('Distance:', size = (10, 1)), sg.InputText('0', key = 'distance', size = (10, 1), do_not_clear = True),
                                sg.Text('Fuel rate (GPH):', size = (15, 1), justification = 'right'), sg.InputText('7.8', key = 'fuel_rate', size = (10, 1), do_not_clear = True)],
                               [sg.Text('Time:', size = (10, 1)), sg.Text('0', key = 'time', size = (10, 1)), 
                                sg.Text('Fuel:', size = (14, 1), justification = 'right'), sg.Text('0', key = 'fuel', size = (10, 1))],
                               [sg.ReadButton('Calculate', key = 'calcFlight', size = (15, 1))]],
                     title = 'Flight planning', relief = sg.RELIEF_SUNKEN)

# Window layout
layout = [[frame_ty], [frame_alt], [frame_wind], [frame_flt], [sg.ReadButton('Calculate All', key = 'calcAll', size = (30, 1)), sg.ReadButton('Exit', key = 'exit', size = (30, 1))]]
window = sg.Window('MyE6B Calculator').Layout(layout)

# run forever
while True:
    # wait for a event
    button, values = window.Read()

    if button == 'exit':
        break
    elif button == 'load':
        e6b.aircraft = values['aircraft_type']
    elif button == 'calcAltitude':
        e6b.alt_abs   = float(values['altitude_ind'])
        e6b.temp      = float(values['temperature'])
        e6b.altimeter = float(values['altimeter'])
        e6b.KIAS      = float(values['kias'])

        e6b.calcPressureAltitude()
        e6b.calcDensityAltitude()
        e6b.calcTAS()

        window.FindElement('altitude_pressure').Update(round(e6b.alt_pre))
        window.FindElement('altitude_density').Update(round(e6b.alt_den))
        window.FindElement('ktas_out').Update(round(e6b.KTAS))

        window.FindElement('ktas_in').Update(round(e6b.KTAS))
    elif button == 'calcWindCorr':
        e6b.windDir = float(values['wind_direction'])
        e6b.windStr = float(values['wind_speed'])
        e6b.KTAS    = float(values['ktas_in'])
        e6b.trueCourse = float(values['true_course'])

        e6b.calcWindCorr()

        window.FindElement('wca').Update(round(e6b.WCA))
        window.FindElement('true_heading').Update(round(e6b.trueHeading))
        window.FindElement('ground_speed').Update(round(e6b.groundSpeed))
    elif button == 'calcFlight':
        e6b.fuelRate = float(values['fuel_rate'])
        distance     = float(values['distance'])

        time, fuel = e6b.fltPlanning(distance)
        hour = math.floor(time/60.)
        minute = round(time - hour*60.)

        window.FindElement('time').Update('%02d : %02d' % (hour, minute))
        window.FindElement('fuel').Update(round(fuel))
    else:
        print(button)
        print(values)
