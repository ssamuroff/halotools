#!/usr/bin/env python

"""
Very simple set of sanity checks on halo_occupation module 
Will copy and paste my additional tests once I figure out the basic design conventions.
"""

#from __future__ import (absolute_import, division, print_function,
#                        unicode_literals)

import numpy as np
from ..halo_occupation import Zheng07_HOD_Model
from ..halo_occupation import Satcen_Correlation_Polynomial_HOD_Model as satcen
from ..halo_occupation import Polynomial_Assembly_Biased_HOD_Model as abhod


def test_zheng_model():

	m = Zheng07_HOD_Model(threshold=-20.0)
	test_mass = np.array([10,11,12,13,14,15])
	halo_types = np.ones(len(test_mass))
	test_mean_ncen = m.mean_ncen(test_mass,halo_types)

	assert np.all(test_mean_ncen >= 0)

def test_satcen():

	m = satcen(threshold=-19.0)
	# array of a few test masses
	p = np.arange(5,20,0.1)
	primary_halo_property = np.append(p,p)
	# array of halo_types
	h0 = np.zeros(len(p))
	h1 = np.zeros(len(p)) + 1
	halo_types = np.append(h0,h1)
	# arrays of indices for bookkeeping
	idx0=np.where(halo_types == 0)[0]
	idx1=np.where(halo_types == 1)[0]

	#probability of having halo_type=0
	phs0 = m.halo_type_fraction_satellites(primary_halo_property[idx0],halo_types[idx0])
	#probability of having halo_type=1
	phs1 = m.halo_type_fraction_satellites(primary_halo_property[idx1],halo_types[idx1])
	# Compute the value of mean_nsat that derives from the conditioned occupations
	derived_nsat = (phs0*m.mean_nsat(primary_halo_property[idx0],halo_types[idx0]) + 
		phs1*m.mean_nsat(primary_halo_property[idx1],halo_types[idx1]))
	# Compute the value of mean_nsat of the underlying baseline HOD model
	underlying_nsat = m.baseline_hod_model.mean_nsat(
		primary_halo_property[idx0],halo_types[idx0])
	# Require that the derived and underlying 
	# satellite occupations are equal (highly non-trivial)
	assert np.allclose(derived_nsat, underlying_nsat,rtol=1e-6)

def test_abhod():

	m = abhod(threshold=-20.0)
	# array of a few test masses
	p = np.arange(5,20,0.1)
	primary_halo_property = np.append(p,p)
	# array of halo_types
	h0 = np.zeros(len(p))
	h1 = np.ones(len(p)) 
	halo_types = np.append(h0,h1)
	# arrays of indices for bookkeeping
	idx0=np.where(halo_types == 0)[0]
	idx1=np.where(halo_types == 1)[0]


	#### Ensure underlying satellite HOD is preserved ####
	#probability of having halo_type=0
	phs0 = m.halo_type_fraction_satellites(primary_halo_property[idx0],halo_types[idx0])
	#probability of having halo_type=1
	phs1 = m.halo_type_fraction_satellites(primary_halo_property[idx1],halo_types[idx1])
	# Compute the value of mean_nsat that derives from the conditioned occupations
	derived_nsat = (phs0*m.mean_nsat(primary_halo_property[idx0],halo_types[idx0]) + 
		phs1*m.mean_nsat(primary_halo_property[idx1],halo_types[idx1]))
	# Compute the value of mean_nsat of the underlying baseline HOD model
	underlying_nsat = m.baseline_hod_model.mean_nsat(primary_halo_property[idx0],halo_types[idx0])
	# Require that the derived and underlying 
	# satellite occupations are equal (highly non-trivial)
	assert np.allclose(derived_nsat, underlying_nsat,rtol=1e-6)

	#### Ensure underlying central HOD is preserved ####
	#probability of having halo_type=0
	phs0 = m.halo_type_fraction_centrals(primary_halo_property[idx0],halo_types[idx0])
	#probability of having halo_type=1
	phs1 = m.halo_type_fraction_centrals(primary_halo_property[idx1],halo_types[idx1])
	# Compute the value of mean_nsat that derives from the conditioned occupations
	derived_ncen = (phs0*m.mean_ncen(primary_halo_property[idx0],halo_types[idx0]) + 
		phs1*m.mean_ncen(primary_halo_property[idx1],halo_types[idx1]))
	# Compute the value of mean_ncen of the underlying baseline HOD model
	underlying_ncen = m.baseline_hod_model.mean_ncen(primary_halo_property[idx0],halo_types[idx0])
	# Require that the derived and underlying 
	# satellite occupations are equal (highly non-trivial)
	assert np.allclose(derived_ncen, underlying_ncen,rtol=1e-6)

	# Require that < Ncen > doesn't exceed unity for type 0 halos
	assert np.all( m.mean_ncen(primary_halo_property[idx0],halo_types[idx0]) <= 1.0001 )
	# Require that < Ncen > doesn't exceed unity for type 1 halos
	assert np.all( m.mean_ncen(primary_halo_property[idx1],halo_types[idx1]) <= 1.0001 )

	# Require that < Ncen > is non-negative for type 0 halos
	assert np.all( m.mean_ncen(primary_halo_property[idx0],halo_types[idx0]) >= 0 )
	# Require that < Ncen > doesn't exceed unity for type 1 halos
	assert np.all( m.mean_ncen(primary_halo_property[idx1],halo_types[idx1]) >= 0 )




# Can't figure out the relative import syntax for a module-wide function
# comment out for now
#def test_solve_for_quenching_polynomial_coefficients():
	""" 
	Use known pencil-and-paper answer to check 
	that solve_for_quenching_polynomial_coefficients
	is correctly solving the input linear system"""

#	x=[0,1,-1,2]
#	y=[10,15,11,26]
#	coeff = solve_for_polynomial_coefficients(x,y)
#	test_coeff = coeff - np.array([10,2,3,0])
#	assert np.allclose(coeff, np.array([10,2,3,0])







