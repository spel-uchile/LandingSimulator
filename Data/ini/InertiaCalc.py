"""
Created: 4/13/2020
Autor: Elias Obreque Sepulveda
email: els.obrq@gmail.com

"""
# kg
mass = 24.0

dx = 0.2
dy = 0.3
dz = 0.2

Ixx = mass/12 * (dy**2 + dz**2)
Iyy = mass/12 * (dz**2 + dx**2)
Izz = mass/12 * (dx**2 + dy**2)

print(Ixx, Iyy, Izz)