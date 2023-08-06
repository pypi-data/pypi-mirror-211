#!/usr/bin/env python3

import numpy as np
import astropy.units as unit
from astropy.constants import G, kpc
import matplotlib.pyplot as plt

def parameter(*args):

	if len(args) != 8:
		print("Error: perlu 8 arguments")
	else:
		try:
			if len(args[2]) == 3 and len(args[3]) == 3 and len(args[4]) == 3:
				return {"massa"      	: args[0]*unit.M_sun,
						"radius"     	: args[1]*unit.kpc,
						"posisi_pusat"	: args[2]*unit.kpc,
						"kec_pusat" 	: args[3]*unit.km/unit.s,
						"grs_normal"    : args[4],
						"N_rings"		: args[5],
						"N_bintang"		: args[6],
						"softening"		: args[7] }
			else:
				print("Error: 3., 4., dan 5. harus 3-tuple")
		except TypeError:
			print("Error: argument salah")

def awal(galaxy, time_step=0.1*unit.Myr):

	dr = (1 - galaxy['softening'])*galaxy['radius']/galaxy['N_rings'] 
	N_stars_per_ring = int(galaxy['N_bintang']/galaxy['N_rings'])
	
	norm = np.sqrt(galaxy['grs_normal'][0]**2 + galaxy['grs_normal'][1]**2 + galaxy['grs_normal'][2]**2)
	cos_theta = galaxy['grs_normal'][2]/norm
	sin_theta = np.sqrt(1-cos_theta**2)
	u = np.cross([0,0,1], galaxy['grs_normal']/norm)
	norm = np.sqrt(u[0]**2 + u[1]**2 + u[2]**2)
	
	if norm > 0:
		u /= norm
		rotation = [[u[0]*u[0]*(1-cos_theta) + cos_theta,
					 u[0]*u[1]*(1-cos_theta) - u[2]*sin_theta,
					 u[0]*u[2]*(1-cos_theta) + u[1]*sin_theta],
					[u[1]*u[0]*(1-cos_theta) + u[2]*sin_theta,
					 u[1]*u[1]*(1-cos_theta) + cos_theta,
					 u[1]*u[2]*(1-cos_theta) - u[0]*sin_theta],
					[u[2]*u[0]*(1-cos_theta) - u[1]*sin_theta,
					 u[2]*u[1]*(1-cos_theta) + u[0]*sin_theta,
					 u[2]*u[2]*(1-cos_theta) + cos_theta]]
			
		phi = np.arctan2(galaxy['grs_normal'][1], galaxy['grs_normal'][0])
		theta = np.arccos(cos_theta)
		print("Garis normal: phi = {:.1f}°, theta = {:.1f}°".format(np.degrees(phi), np.degrees(theta)))
			
	else:
		rotation = np.identity(3)
			
	galaxy['posisi_bintang'] = np.array([])
	galaxy['kec_bintang'] = np.array([])
	
	R = galaxy['softening']*galaxy['radius']
	
	for n in range(galaxy['N_rings']):
			
		r_star = R + dr * np.random.random_sample(size=N_stars_per_ring)
		phi_star = 2*np.pi * np.random.random_sample(size=N_stars_per_ring)
			
		vec_r = np.dot(	rotation,
						r_star*[np.cos(phi_star),
						np.sin(phi_star),
						np.zeros(N_stars_per_ring)])	
	
		x = galaxy['posisi_pusat'][0] + vec_r[0]
		y = galaxy['posisi_pusat'][1] + vec_r[1]
		z = galaxy['posisi_pusat'][2] + vec_r[2]
			
		T_star = 2*np.pi * ((G*galaxy['massa'])**(-1/2) * r_star**(3/2)).to(unit.s)
		delta_phi = 2*np.pi * time_step.to(unit.s).value / T_star.value
			
		vec_v = np.dot( rotation,
						(r_star.to(unit.km)/time_step.to(unit.s)) * 
						 [(np.cos(phi_star) - np.cos(phi_star - delta_phi)),
						  (np.sin(phi_star) - np.sin(phi_star - delta_phi)), 
						  np.zeros(N_stars_per_ring)])
			
		v_x = galaxy['kec_pusat'][0] + vec_v[0]
		v_y = galaxy['kec_pusat'][1] + vec_v[1]
		v_z = galaxy['kec_pusat'][2] + vec_v[2]
			
		if  galaxy['posisi_bintang'].size == 0:
			galaxy['posisi_bintang'] = np.array([x,y,z])
			galaxy['kec_bintang'] = np.array([v_x,v_y,v_z])
		else:
			galaxy['posisi_bintang'] = np.append(galaxy['posisi_bintang'], np.array([x,y,z]), axis=1)
			galaxy['kec_bintang'] = np.append(galaxy['kec_bintang'], np.array([v_x,v_y,v_z]), axis=1)
					
		R += dr
			
	galaxy['posisi_bintang'] *= unit.kpc
	galaxy['kec_bintang'] *= unit.km/unit.s
	galaxy['skala_kecepatan'] = np.sqrt(G*galaxy['massa']/(0.5*R)).to(unit.km/unit.s)
	
def proses(primary, secondary, time_step=0.1*unit.Myr, N_steps=1000, N_snapshots=100):
	
	dt = time_step.to(unit.s).value
	
	r_min1 = primary['softening']*primary['radius'].to(unit.m).value
	r_min2 = secondary['softening']*secondary['radius'].to(unit.m).value
	
	N1, N2 = primary['N_bintang'], secondary['N_bintang']
	
	M1 = primary['massa'].to(unit.kg).value
	X1, Y1, Z1 = primary['posisi_pusat'].to(unit.m).value
	V1_x, V1_y, V1_z = primary['kec_pusat'].to(unit.m/unit.s).value
	
	M2 = secondary['massa'].to(unit.kg).value
	X2, Y2, Z2 = secondary['posisi_pusat'].to(unit.m).value
	V2_x, V2_y, V2_z = secondary['kec_pusat'].to(unit.m/unit.s).value
	
	x = primary['posisi_bintang'][0].to(unit.m).value
	y = primary['posisi_bintang'][1].to(unit.m).value
	z = primary['posisi_bintang'][2].to(unit.m).value
	
	x = np.append(x, secondary['posisi_bintang'][0].to(unit.m).value)
	y = np.append(y, secondary['posisi_bintang'][1].to(unit.m).value)
	z = np.append(z, secondary['posisi_bintang'][2].to(unit.m).value)
	
	v_x = primary['kec_bintang'][0].to(unit.m/unit.s).value
	v_y = primary['kec_bintang'][1].to(unit.m/unit.s).value
	v_z = primary['kec_bintang'][2].to(unit.m/unit.s).value
	
	v_x = np.append(v_x, secondary['kec_bintang'][0].to(unit.m/unit.s).value)
	v_y = np.append(v_y, secondary['kec_bintang'][1].to(unit.m/unit.s).value)
	v_z = np.append(v_z, secondary['kec_bintang'][2].to(unit.m/unit.s).value)
	
	snapshots = np.zeros(shape=(N_snapshots+1,3,N1+N2+2))
	snapshots[0] = [np.append([X1,X2], x), np.append([Y1,Y2], y), np.append([Z1,Z2], z)]
	# print(snapshots.shape)
	
	div = max(int(N_steps/N_snapshots), 1)
	
	print("-------------------------------")
	print("Simulasi Tumbukan antar Galaksi")
	print("    Eka Suyatno [20221007]     ")
	print("-------------------------------")
	print("Memproses ... ")
	
	for n in range(1,N_steps+1):
			
		r1 = np.maximum(np.sqrt((X1 - x)**2 + (Y1 - y)**2 + (Z1 - z)**2), r_min1)
		r2 = np.maximum(np.sqrt((X2 - x)**2 + (Y2 - y)**2 + (Z2 - z)**2), r_min2)
		# print("\nr {:.6e} {:.6e} {:.6e} {:.6e}".format(r1[0],r2[0],r1[N1],r2[N1]))
			
		v_x += G.value*(M1*(X1 - x)/r1**3 + M2*(X2 - x)/r2**3) * dt
		v_y += G.value*(M1*(Y1 - y)/r1**3 + M2*(Y2 - y)/r2**3) * dt
		v_z += G.value*(M1*(Z1 - z)/r1**3 + M2*(Z2 - z)/r2**3) * dt
		# print("v_x {:.1f} {:.1f}".format(v_x[0],v_x[N1]))
			
		x += v_x*dt
		y += v_y*dt
		z += v_z*dt
		# print("x {:.6e} {:.6e}".format(x[0],x[N1]))
			
		D_sqr_min = (r_min1+r_min2)**2
		D_cubed = (max((X1 - X2)**2 + (Y1 - Y2)**2 + (Z1 - Z2)**2, D_sqr_min))**(3/2)
			
		A1_x = G.value*M2*(X2 - X1)/D_cubed
		A1_y = G.value*M2*(Y2 - Y1)/D_cubed
		A1_z = G.value*M2*(Z2 - Z1)/D_cubed
			
		V1_x += A1_x*dt; V2_x -= (M1/M2)*A1_x*dt
		V1_y += A1_y*dt; V2_y -= (M1/M2)*A1_y*dt
		V1_z += A1_z*dt; V2_z -= (M1/M2)*A1_z*dt
		# print("V {:.1f} {:.1f} {:.1f}".format(V1_x,V2_x,(M1*V1_x+M2*V2_x)/(M1+M2)))
			
		X1 += V1_x*dt; X2 += V2_x*dt
		Y1 += V1_y*dt; Y2 += V2_y*dt
		Z1 += V1_z*dt; Z2 += V2_z*dt
		# print("X {:.6e} {:.6e} {:.6e}".format(X1,X2,X1+X2))
		
		if n % div == 0:
			i = int(n/div)
			snapshots[i] = [np.append([X1,X2], x), np.append([Y1,Y2], y), np.append([Z1,Z2], z)]
					
		print("\r{:3d} %".format(int(100*n/N_steps)), end="")
			
	time = np.linspace(0*time_step, N_steps*time_step, N_snapshots+1, endpoint=True)
	print(" (Berakhir di t = {:.1f})".format(time[-1]))
	
	snapshots *= unit.m
	
	return time, snapshots.to(unit.kpc)

def show(snapshot, N1, xlim=None, ylim=None, zlim=None, time=None, name=None):

	N2 = snapshot.shape[1]-2-N1
	
	fig = plt.figure(figsize=(10,10), dpi=150)
	ax = fig.add_subplot(111, projection='3d')
	
	ax.set_box_aspect((1, 1, 1))
	ax.set_xlabel(r'$x$ [kpc]', fontsize=12)
	ax.set_ylabel(r'$y$ [kpc]', fontsize=12)
	ax.set_zlabel(r'$z$ [kpc]', fontsize=12)
	
	if xlim != None: ax.set_xlim(xlim[0], xlim[1])
	if ylim != None: ax.set_ylim(ylim[0], ylim[1])
	if zlim != None: ax.set_zlim(zlim[0], zlim[1])
	
	if time != None:
		title = ax.set_title('$t$ = {:.1f}'.format(time))
			
	ax.scatter( snapshot[0,0:2],          
				snapshot[1,0:2],          
				snapshot[2,0:2], 
				marker='+', 
				color='black')
	ax.scatter( snapshot[0,2:N1+2],       
				snapshot[1,2:N1+2],
				snapshot[2,2:N1+2], 
				marker='.', 
				color='blue', 
				s=2)
	ax.scatter( snapshot[0,N1+2:N1+N2+2], 
				snapshot[1,N1+2:N1+N2+2], 
				snapshot[2,N1+2:N1+N2+2], 
				marker='.', 
				color='red', 
				s=2)
	
	if name != None:
		plt.savefig(name + '_{:.0f}.png'.format(time))
			
	plt.close()

