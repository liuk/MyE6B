import math

class E6BCore:

    # definition of constants
    lapseRate = 0.0019812   # degree C per foot
    tempZero  = 273.15      # C to K
    tempStdSea = 15. + tempZero  # standard temperature at sea level
    pressureStdSea = 29.92  # standard pressure at sea level

    def __init__(self):
        # definition of all variables involved
        self.aircraft = 'C172R'       # default for C-172 R (N3504P)
        self.fuelRate = 7.8           # fuel usage, unit is gal/h
        self.KIAS = 100               # indicated airspeed, unit is knot
        self.KTAS = 100               # true airspeed, unit is knot
        self.alt_abs = 7300           # absolute altitude, unit is feet
        self.alt_pre = 7300           # pressure altitude, unit is feet
        self.alt_den = 7300           # density altitude, unit is feet
        self.temp = 15                # outside temperature, unit is celcius
        self.altimeter = 29.92        # altimeter setting, unit is inch Hg
        self.windDir = 0              # wind true direction, unit is degree
        self.windStr = 10             # wind speed, unit is knot
        self.trueCourse = 0           # true course, unit is degree
        self.WCA = 0                  # wind correction angle, unit is degree
        self.trueHeading = 0          # true heading, unit is degree
        self.groundSpeed = 100        # ground speed, unit is knot

    def calcPressureAltitude(self):
        """from the indicated altitude to pressure altitude"""
        self.alt_pre = self.alt_abs + 145442.2*(1. - math.pow(self.altimeter/E6BCore.pressureStdSea, 0.190261))
    
    def calcDensityAltitude(self):
        """from pressure altitude to density altitude"""
        tempStd = E6BCore.tempStdSea - self.alt_pre*E6BCore.lapseRate  # standard temperature at current pressure altitude
        self.alt_den = self.alt_pre + tempStd/E6BCore.lapseRate*(1. - math.pow(tempStd/(self.temp + E6BCore.tempZero), 0.234969))

    def calcTAS(self):
        """calculate the true airspeed based on density altitude and indicated airspeed"""
        self.KTAS = self.KIAS/math.sqrt(math.pow((E6BCore.tempStdSea - self.alt_den*E6BCore.lapseRate)/E6BCore.tempStdSea, 1./0.234969))

    def calcWindCorr(self):
        """calculate the wind correction angle, true heading and ground speed"""
        headWind, crossWind = self.windDecompose()
        self.WCA = self.rad2deg(math.asin(crossWind/self.KTAS))
        self.trueHeading = self.trueCourse + self.WCA
        self.groundSpeed = self.KTAS*math.cos(self.deg2rad(self.WCA)) - headWind

    def fltPlanning(self, distance): # unit of distance should be naunical miles
        """calculate the time and fuel consumption"""
        #self.calcPressureAltitude()
        #self.calcDensityAltitude()
        #self.calcTAS()
        #self.calcWindCorr()

        time = distance/self.groundSpeed*60.
        fuelUse = self.fuelRate*time/60.

        return (time, fuelUse)
    
    def windDecompose(self):
        """get the head and cross wind component"""
        angle = self.deg2rad(self.windDir - self.trueCourse)
        headWind = self.windStr*math.cos(angle)
        crossWind = self.windStr*math.sin(angle)

        return (headWind, crossWind)

    def rad2deg(self, rad):
        return rad/math.pi*180.
    
    def deg2rad(self, deg):
        return deg/180.*math.pi

    def inhg2mbar(self, inhg):
        return inhg*33.8639

    def interpolate(self, xval, xlo, ylo, xhi, yhi):
        """simple interpolation tool to get the number between 2 points in POH"""
        return ylo + (yhi - ylo)/(xhi - xlo)*(xval - xlo)
