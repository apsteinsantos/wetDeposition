# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:23:31 2025

@author: anapa
"""

import numpy as np
Dp_min = 0
Dp_max = 0.6
Dp = (Dp_max-Dp_min)*np.random.rand(1000) + Dp_min #diametro da gota cm

z_min = 100
z_max = 100000
z = (z_max-z_min)*np.random.rand(1000) + z_min  #altura da precipitação cm

Ut_min = 0
Ut_max = 1
Ut = (Ut_max-Ut_min)*np.random.rand(1000) + Ut_min #velocidade da gota cm*s−1

T_min = 275
T_max = 310
T = (T_max-T_min)*np.random.rand(1000) + T_min  #temp Kelvin

H = 1.45E-02 # Cte Henry
R = 0.082 #cte molar

#variáveis Kc
Dg_min = 0
Dg_max = 1
Dg = (Dg_max-Dg_min)*np.random.rand(1000) + Dg_min  #difusibilidade das espécies químicas cm2*s−1

p_air_min = 0
p_air_max = 1
p_air = (p_air_max-p_air_min)*np.random.rand(1000) + p_air_min #densidade do ar g*cm−3

mi_air_min = 0
mi_air_max = 1
mi_air = (mi_air_max-mi_air_min)*np.random.rand(1000) + mi_air_min #viscosidade do car g*cm−1*s−1

#calculo coeficente de transf de massa cm s−1
Kc = Dg/Dp*(2+0.6*((p_air*Dp*Ut/mi_air)**0.5)*((mi_air/(p_air*Dg))**(1/3)))

#coeficiente de lavagem
A = np.pi*Dp**2*Kc*np.exp((-6.0 * Kc * z) / (Dp * Ut * H * R * T))

print(A)