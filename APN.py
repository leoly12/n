def GCFLINT_Lib_APN( msl_pos, tgt_pos, msl_pos_previous, tgt_pos_previous, latax, N = None, Nt = None ):
	"""
	Augmented Proportional Navigation (APN)
	A_cmd = N * Vc * LOS_Rate + N * Nt / 2
	
	msl_pos:	Missile's new position this frame.
	tgt_ps:		Target's new position this frame.
	
	msl_pos_previous:  Mutable object for missile's position previous frame.
	tgt_pos_previous:  Mutable object for target's position previous frame.
	Set these objects to "0" during first time initialization, as we haven't
	yet started recording previous positions yet.
	
	latax:	Mutable object for returning guidance command.
	N:		(float, optional) Navigation gain (3.0 to 5.0)
	Nt:		(float, optional) Target acceleration amount normal to LOS
	"""
	
	import wic.common.math as math
	from predictorFCS_flint_includes import *
	from predictorFCS_EXFLINT import *
	
	if N is None:
		# navigation constant
		N = 3.0
	else isinstance(N, float) is not True:
		raise TypeError("N must be float")
	
	if Nt is None:
		# one-g sensible acceleration
		Nt = 9.8 * EXFLINT_TICKTOCK
	else isinstance(Nt, float) is not True:
		raise TypeError("Nt must be float")
	
	if msl_pos_previous is not 0 and tgt_pos_previous is not 0:
		
		# Get msl-target distances of previous frame and new frame (Rtm)
		RTM_old = ( math.Vector3( tgt_pos_previous ) - msl_pos_previous )
		RTM_new = ( math.Vector3( tgt_pos ) - msl_pos )
		
		# normalize RTM vectors
		RTM_new.NormalizeSafe()
		RTM_old.NormalizeSafe()
		
		if RTM_old.Length() is 0:
			LOS_Delta = math.Vector3( 0, 0, 0 )
			LOS_Rate = 0.0
		else:
			LOS_Delta = math.Vector3( RTM_new ) - RTM_old
			LOS_Rate = LOS_Delta.VectorLength()
		
		# range closing rate
		Vc = -LOS_Rate
		
		# Now, calculate the final lateral acceleration required for our missile
		# to home into our target.
		latax = RTM_new * N * Vc * LOS_Rate + LOS_Delta * Nt * ( 0.5 * N )
	
	# Update mutable position objects so we can integrate forward to next frame.
	msl_pos_previous = math.Vector3( msl_pos )
	tgt_pos_previous = math.Vector3( tgt_pos )
	
	# my job is done, it's now up to EXFLINT.Integrate() to steer the missile.
	return True

