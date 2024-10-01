# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
# Converts ECEF coordinates to ECI coordinates based on the provided date and time.
#
# Parameters:
# year: Integer
# month: Integer, 1-12
# day: Integer 1-31
# hour: Integer 0-23
# minute: Integer 0-59
# second: Decimal
# ecef_x_km: ECEF x-coordinate in km
# ecef_y_km: ECEF y-coordinate in km
# ecef_z_km: ECEF z-coordinate in km
#
# Output:
# eci_x_km: ECI x-coordinate in km
# eci_y_km: ECI y-coordinate in km
# eci_z_km: ECI z-coordinate in km
#
# Written by Michael Hoffman
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

import sys #argv
import math #math module

# Helper function to calculate fractional Julian Date
def ymdhms_to_jd(year, month, day, hour, minute, second):
    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    C = math.floor(365.25 * (year + 4716))
    D = math.floor(30.6001 * (month + 1))

    jd = C + D + day + B - 1524.5
    day_fraction = (hour + minute / 60 + second / 3600) / 24
    jd_frac = jd + day_fraction

    return jd_frac

# Helper function to calculate GMST
def jd_to_gmst(jd):
    T = (jd - 2451545.0) / 36525.0  
    GMST_sec = 67310.54841 + (876600.0 * 3600.0 + 8640184.812866) * T + 0.093104 * T**2 - 6.2e-6 * T**3
    GMST_deg = (GMST_sec / 240.0) % 360.0  
    if GMST_deg < 0:
        GMST_deg += 360.0
    return GMST_deg

# Convert degrees to radians
def degrees_to_radians(degrees):
    return degrees * math.pi / 180.0

# Convert ECEF coordinates to ECI coordinates
def ecef_to_eci(jd, ecef_x, ecef_y, ecef_z):
    gmst = jd_to_gmst(jd)
    gmst_rad = degrees_to_radians(gmst)

    # Rotation matrix for GMST around the z-axis 
    cos_gmst = math.cos(gmst_rad)
    sin_gmst = math.sin(gmst_rad)

    eci_x = cos_gmst * ecef_x - sin_gmst * ecef_y
    eci_y = sin_gmst * ecef_x + cos_gmst * ecef_y
    eci_z = ecef_z  

    return eci_x, eci_y, eci_z

# Initialize script arguments
year = 0
month = 0
day = 0
hour = 0
minute = 0
second = 0.0
ecef_x_km = 0.0
ecef_y_km = 0.0
ecef_z_km = 0.0

# Parse script arguments
if len(sys.argv) == 10:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    ecef_x_km = float(sys.argv[7])
    ecef_y_km = float(sys.argv[8])
    ecef_z_km = float(sys.argv[9])
else:
    print('Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km')
    exit()

# Calculate Julian Date
jd = ymdhms_to_jd(year, month, day, hour, minute, second)

# Convert ECEF to ECI
eci_x_km, eci_y_km, eci_z_km = ecef_to_eci(jd, ecef_x_km, ecef_y_km, ecef_z_km)

# Print ECI coordinates
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
