

## Copyright(c) 2022, 2023 Yoann Robin
## 
## This file is part of XSBCK.
## 
## XSBCK is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## XSBCK is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with XSBCK.  If not, see <https://www.gnu.org/licenses/>.

#############
## Imports ##
#############

import sys
import itertools as itt
import os
import gc
import logging
import datetime as dt

import numpy  as np
import xarray as xr
import cftime
import dask
import distributed
import netCDF4

import zarr
import SBCK

from .__XSBCKParams import xsbckParams

from .__release import version
from .__logs    import log_start_end
from .__utils   import SizeOf
from .__utils   import build_reference
from .__utils   import delete_hour_from_time_axis
from .__utils   import time_match

from .__XZarr import XZarr


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


#################################################
## Function to read data and create zarr files ##
#################################################

## load_data ##{{{
@log_start_end(logger)
def load_data():
	"""
	XSBCK.load_data
	===============
	Function used to read data and copy in a temporary zarr file
	
	Returns
	-------
	zX:
		XZarr file of the biased dataset
	zY:
		XZarr file of the reference dataset
	zZ:
		XZarr file of the corrected dataset (empty)
	"""
	
	##
	time_axis = xsbckParams.time_axis
	cvarsX = xsbckParams.cvarsX
	cvarsY = xsbckParams.cvarsY
	cvarsZ = xsbckParams.cvarsZ
	
	## Open with xarray to decode all variables and time axis
	xX = xr.open_mfdataset( xsbckParams.input_biased    , data_vars = "minimal" , coords = "minimal" , compat = "override" , combine_attrs = "drop" )
	xY = xr.open_mfdataset( xsbckParams.input_reference , data_vars = "minimal" , coords = "minimal" , compat = "override" , combine_attrs = "drop" )
	
	## Init cvars
	logger.info("Check cvars")
	if (cvarsX is not None and cvarsY is None) or (cvarsY is not None and cvarsX is None):
		raise Exception( "If cvars is given for the ref (or the biased), cvars must be given for the biased (or the ref)" )
	check_cvarsXY_is_same = False
	if cvarsX is None:
		cvarsX  = [key for key in xX.data_vars]
		cvarsX.sort()
		check_cvarsXY_is_same = True
	else:
		cvarsX = cvarsX.split(",")
	if cvarsY is None:
		cvarsY  = [key for key in xY.data_vars]
		cvarsY.sort()
		check_cvarsXY_is_same = True
	else:
		cvarsY = cvarsY.split(",")
	if check_cvarsXY_is_same:
		if ( not all([cvar in cvarsX for cvar in cvarsY]) ) or (not all([cvar in cvarsY for cvar in cvarsX])):
			raise Exception( "Variables from ref or biased differs" )
	if cvarsZ is None:
		cvarsZ = cvarsX
	else:
		cvarsZ = cvarsZ.split(",")
	
	xsbckParams.cvarsX = cvarsX
	xsbckParams.cvarsY = cvarsY
	xsbckParams.cvarsZ = cvarsZ
	
	logger.info( f" * cvarsX: {cvarsX}" )
	logger.info( f" * cvarsY: {cvarsY}" )
	logger.info( f" * cvarsZ: {cvarsZ}" )
	
	for cvarX in cvarsX:
		if cvarX not in xX:
			raise Exception( f"Variable '{cvarX}' not in biased data" )
	for cvarY in cvarsY:
		if cvarY not in xY:
			raise Exception( f"Variable '{cvarY}' not in reference data" )
	
	## Remove of the dataset all variables without time axis
	keys_to_del = [key for key in xX.data_vars if time_axis not in xX[key].dims]
	for key in keys_to_del:
		del xX[key]
	keys_to_del = [key for key in xY.data_vars if time_axis not in xY[key].dims]
	for key in keys_to_del:
		del xY[key]
	
	## Find spatial memory available
	total_memory       = xsbckParams.total_memory.o
	frac_mem_per_array = xsbckParams.frac_memory_per_array
	max_mem_per_chunk  = SizeOf( n = int(frac_mem_per_array * total_memory) , unit = "o" )
	max_time           = 365 * max( np.diff([int(s) for s in xsbckParams.calibration]) + 1 , sum(xsbckParams.window) )
	max_cvar           = len(cvarsZ)
	avail_spatial_mem  = SizeOf( n = int( max_mem_per_chunk.o / ( max_time * max_cvar * (np.finfo('float32').bits // max_mem_per_chunk.bits_per_octet) ) ) , unit = "o" )
	
	logger.info( "Check memory:" )
	logger.info( f" * Max mem. per chunk: {max_mem_per_chunk}" )
	logger.info( f" * Max time step     : {max_time}" )
	logger.info( f" * Max cvar          : {max_cvar}" )
	logger.info( f" * Avail Spat. Mem.  : {avail_spatial_mem}" )
	
	## Find chunks
	dask_chunks = xsbckParams.chunks
	if dask_chunks == -1:
		dask_chunks = xsbckParams.n_workers * xsbckParams.threads_per_worker
	
	ny = xX[xX[cvarsX[0]].dims[1]].size
	nx = xX[xX[cvarsX[0]].dims[2]].size
	avail_spatial_numb = int( avail_spatial_mem.o / (np.finfo(xX[cvarsX[0]].dtype).bits // max_mem_per_chunk.bits_per_octet) )
	zch_ny = max( int(ny / np.sqrt(avail_spatial_numb)) , 1 )
	zch_nx = max( int(nx / np.sqrt(avail_spatial_numb)) , 1 )
	zarr_chunks = [ None , ny // zch_ny , nx // zch_nx , 1 ]
	
	logger.info( "Chunks found:" )
	logger.info( f" * dask_chunks: {dask_chunks}" )
	logger.info( f" * zarr_chunks: {zarr_chunks}" )
	
	## Now zarr file
	logger.info( "Create biased zarr file..." )
	zX = XZarr.from_dataset( os.path.join( xsbckParams.tmp , "X.zarr" ) , xX , ifiles = xsbckParams.input_biased    , xcvars = cvarsX , zcvars = cvarsZ , dask_chunks = dask_chunks , zarr_chunks = zarr_chunks , time_axis = time_axis )
	logger.info( "Create reference zarr file..." )
	zY = XZarr.from_dataset( os.path.join( xsbckParams.tmp , "Y.zarr" ) , xY , ifiles = xsbckParams.input_reference , xcvars = cvarsY , zcvars = cvarsZ , dask_chunks = dask_chunks , zarr_chunks = zarr_chunks , time_axis = time_axis )
	logger.info( "Create corrected (empty) zarr file..." )
	zZ = zX.copy( os.path.join( xsbckParams.tmp , "Z.zarr" ) , np.nan )
	
	logger.info( f"About biased data:" )
	logger.info( f" * shape  : {str(zX.shape)}" )
	logger.info( f" * zchunks: {str(zX.zarr_chunks)}" )
	logger.info( f"About reference data:" )
	logger.info( f" * shape  : {str(zY.shape)}" )
	logger.info( f" * zchunks: {str(zY.zarr_chunks)}" )
	
	## Free memory
	del xX
	del xY
	gc.collect()
	
	return zX,zY,zZ
##}}}

## save_data ##{{{ 

@log_start_end(logger)
def save_data( zX : XZarr , zZ : XZarr ):
	"""
	XSBCK.save_data
	===============
	Function used to read the XZarr file of the corrected dataset and rewrite
	in netcdf.
	
	Arguments
	---------
	zX:
		XZarr file of the biased dataset
	zZ:
		XZarr file of the corrected dataset
	
	Returns
	-------
	None
	"""
	
	## Build mapping between cvarsX and cvarsZ
	cvarsX = xsbckParams.cvarsX
	cvarsZ = xsbckParams.cvarsZ
	mcvars = { x : z for x,z in zip(cvarsX,cvarsZ) }
	
	time_chunk = zZ.zarr_chunks[0]
	time_axis  = xsbckParams.time_axis
	tstart     = xsbckParams.start_year
	tend       = xsbckParams.end_year
	
	## Loop on input files
	for ifile in xsbckParams.input_biased:
		
		logger.info( f"File {os.path.basename(ifile)}" )
		
		with netCDF4.Dataset( ifile , mode = "r" ) as incfile:
			
			## The FUCKING problem of TIME
			## i_time   : time of the input file
			## i_time_wh: time of the input file, with hour == 00:00:00 (because in some dataset, the value of hour seems random)
			## o_time_wh: time of the output data, with hour == 00:00:00
			## idx_o_i_t: index of the output data,  w.r.t. i_time
			## o_time   : time of the output data
			## d_time   : time of ALL files, with hour == 00:00:00
			## idx_o_d_t: index of the output data, w.r.t. d_time
			i_time    = cftime.num2date( incfile.variables[time_axis] , incfile.variables[time_axis].units , incfile.variables[time_axis].calendar )
			i_time_wh = delete_hour_from_time_axis(i_time)
			o_time_wh = xr.DataArray( i_time_wh , dims = [time_axis] , coords = [i_time_wh] ).sel( time = slice(tstart,tend) )
			if o_time_wh.size == 0:
				logger.info( " * Not in time selection, continue" )
				continue
			o_time_wh = delete_hour_from_time_axis(o_time_wh)
			idx_o_i_t = time_match( o_time_wh , i_time_wh )
			o_time    = i_time[idx_o_i_t]
			d_time    = zZ.dtime
			idx_o_d_t = time_match( o_time_wh , d_time )
			
			
			## Find the variable
			cvarX = list(set(cvarsX) & set(incfile.variables))[0]
			icvar = cvarsX.index(cvarX)
			cvarZ = cvarsZ[icvar]
			logger.info( f" * cvarX: {cvarX}, cvarZ: {cvarZ}" )
			
			## The output file
			bifile = os.path.basename(ifile)
			prefix = f"{cvarZ}_{xsbckParams.method}"
			if cvarX in bifile:
				ofile = bifile.replace(cvarX,prefix)
			else:
				ofile = f"{prefix}_{bifile}"
			ofile = os.path.join( xsbckParams.output_dir , ofile )
			logger.info( f" * ofile: {ofile}" )
			
			## Now write the output file
			with netCDF4.Dataset( ofile , mode = "w" ) as oncfile:
				
				oncfile.set_fill_off()
				
				## Copy main attributes
				for name in incfile.ncattrs():
					try:
						oncfile.setncattr( name , incfile.getncattr(name) )
					except AttributeError:
						pass
				
				## Add BC attributes
				oncfile.setncattr( "bc_creation_date" , str(dt.datetime.utcnow())[:19] + " (UTC)" )
				oncfile.setncattr( "bc_method"        , xsbckParams.method )
				oncfile.setncattr( "bc_period_calibration" , "/".join( [str(x) for x in xsbckParams.calibration] ) )
				oncfile.setncattr( "bc_window"        , ",".join( [str(x) for x in xsbckParams.window] ) )
				oncfile.setncattr( "bc_reference"     , build_reference(xsbckParams.method) )
				oncfile.setncattr( "bc_pkgs_versions" , ", ".join( [f"XSBCK:{version}"] + [f"{name}:{pkg.__version__}" for name,pkg in zip(["SBCK","numpy","xarray","dask","distributed","zarr","netCDF4"],[SBCK,np,xr,dask,distributed,zarr,netCDF4]) ] ) )
				
				## Start with dimensions
				dims   = [d for d in incfile.dimensions]
				ncdims = { d : oncfile.createDimension( d  , incfile.dimensions[d].size )  for d in dims if not d == time_axis }
				if incfile.dimensions[time_axis] in [None,0]: ## Unlimited dimensions
					ncdims[time_axis] = oncfile.createDimension( d  , None )
				else:
					ncdims[time_axis] = oncfile.createDimension( time_axis  , o_time.size )
				
				## Define variables of dimensions
				ncv_dims = {}
				for d in dims:
					if not d in incfile.variables:
						continue
					chk    = incfile.variables[d].chunking()
					params = { "shuffle" : False }
					if chk == "contiguous":
						params["contiguous"] = True
					else:
						params["compression"] = "zlib"
						params["complevel"]   = 5
						params["chunksizes"]  = chk
					ncv_dims[d] = oncfile.createVariable( d , incfile.variables[d].dtype , (d,)  , **params )
				
				## Copy attributes of the dimensions
				for d in ncv_dims:
					for name in incfile.variables[d].ncattrs():
						try:
							ncv_dims[d].setncattr( name , incfile.variables[d].getncattr(name) )
						except AttributeError:
							pass
				
				## And fill dimensions (except time_axis)
				for d in list(set(dims) & set([k for k in ncv_dims])):
					if d == time_axis:
						continue
					ncv_dims[d][:] = incfile.variables[d][:]
				
				## Now fill time_axis, and add to list of dimensions
				ncv_dims[time_axis][:] = cftime.date2num( o_time , incfile.variables[time_axis].units , incfile.variables[time_axis].calendar )
				
				## Continue with all variables, except the "main" variable
				variables = [v for v in incfile.variables if v not in dims + [cvarX]]
				ncvars = {}
				for v in variables:
					
					## Create the variable
					chk    = incfile.variables[v].chunking()
					params = { "shuffle" : False }
					if chk == "contiguous":
						params["contiguous"] = True
					else:
						params["compression"] = "zlib"
						params["complevel"]   = 5
						params["chunksizes"]  = chk
					ncvars[v] = oncfile.createVariable( v , incfile.variables[v].dtype , incfile.variables[v].dimensions , **params )
					
					## Copy attributes
					for name in incfile.variables[v].ncattrs():
						try:
							ncvars[v].setncattr( name , incfile.variables[v].getncattr(name) )
						except AttributeError:
							pass
					
					## And Fill it
					if len(incfile.variables[v].shape) == 0: ## Scalar variable
						ncvars[v].assignValue(incfile.variables[v].getValue())
					else:
						if time_axis in incfile.variables[v].dimensions:
							
							## Tuple of selection
							sel = [slice(None) for _ in range(len(incfile.variables[v].dimensions))]
							sel[list(incfile.variables[v].dimensions).index(time_axis)] = idx_o_i_t
							sel = tuple(sel)
							
							## And copy var
							ncvars[v][:] = incfile.variables[v][sel]
						else:
							ncvars[v][:] = incfile.variables[v][:]
				
				## Find fill and missing value
				try:
					fill_value = incfile.variables[cvarX].getncattr("_FillValue")
				except AttributeError:
					fill_value = np.nan
				try:
					missing_value = incfile.variables[cvarX].getncattr("missing_value")
				except AttributeError:
					missing_value = None
				
				## Create the main variable
				S = SizeOf( f"{np.prod(incfile.variables[cvarX].shape) * (np.finfo(incfile.variables[cvarX].dtype).bits // SizeOf('1o').bits_per_byte)}o" )
				params = { "shuffle" : False , "fill_value" : fill_value }
				if incfile.variables[cvarX].chunking() == "contiguous":
					params["contiguous"] = True
				elif S < "5Go":
					params["compression"] = "zlib"
					params["complevel"]   = 5
					params["chunksizes"]  = incfile.variables[cvarX].chunking()
				ncvar = oncfile.createVariable( cvarZ , incfile.variables[cvarX].dtype , incfile.variables[cvarX].dimensions , **params )
				if missing_value is not None:
					ncvar.setncattr( "missing_value" , missing_value )
				
				## Copy attributes
				for name in incfile.variables[cvarX].ncattrs():
					try:
						if name == "long_name":
							ncvar.setncattr( name , "Bias Corrected " + incfile.variables[cvarX].getncattr(name) )
						else:
							ncvar.setncattr( name , incfile.variables[cvarX].getncattr(name) )
					except AttributeError:
						pass
				
				## Now loop on zchunks
				for zc in zZ.iter_zchunks():
					
					zc_y,zc_x = zc
					i0y =  zc_y    * zZ.data.chunks[1]
					i1y = (zc_y+1) * zZ.data.chunks[1]
					i0x =  zc_x    * zZ.data.chunks[2]
					i1x = (zc_x+1) * zZ.data.chunks[2]
					
					## And loop on time chunk to limit memory used
					for it in range(0,len(idx_o_d_t),time_chunk):
						it0 = it
						it1 = min( it + time_chunk , len(idx_o_d_t) )
						sel = (idx_o_d_t[it0:it1],slice(i0y,i1y),slice(i0x,i1x),icvar)
						M   = zZ.data.get_orthogonal_selection(sel)
						ncvar[it0:it1,i0y:i1y,i0x:i1x] = np.where( np.isfinite(M) , M , fill_value )
	
##}}}


