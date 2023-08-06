    def newCartesian(self, xyz, dQ, verbose=True):
	# Perform iterations to find new coordinates starting from xyz
	# with the requested internal coordinate change dQ.
        cached = self.readCache(xyz, dQ)
        if cached is not None:
            return cached
	# The coordinates at the start of each iteration
        xyz1 = xyz.copy()
	# The required IC change at the start of each iteration
        dQ1 = dQ.copy()
	# Iteration counter
        microiter = 0
	# The history of the required IC changes; should converge with iteration nr.
        ndqs = [np.linalg.norm(dQ)]
	# The current-best (smallest) IC change out of all iterations taken
        ndqt = ndqs[0]
	# The RMSD of the Cartesian step taken
        rmsds = []
	# Whether we failed to get the desired step
        self.bork = False
        # Damping factor
        damp = 1.0
        # Function to exit from loop
        if verbose >= 2: logger.info("    InternalCoordinates.newCartesian converting internal to Cartesian step (desired |dQ| = %.3e)\n" % np.linalg.norm(dQ))
        def finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1):
            # This function returns the result, and is called from inside the iterations.
            if ndqt > 1e-1:
                if verbose: logger.info("      newCartesian Iter: %i Failed to obtain coordinates (rmsd = %.3e Err-dQ = %.3e)\n" % (microiter, rmsdt, ndqt))
                self.bork = True
                self.writeCache(xyz, dQ, xyz_iter1)
                # Return the result after taking just one step.
                return xyz_iter1.flatten()
            elif ndqt > 1e-3:
                if verbose: logger.info("      newCartesian Iter: %i Approximate coordinates obtained (rmsd = %.3e Err-dQ = %.3e)\n" % (microiter, rmsdt, ndqt))
            else:
                if verbose: logger.info("      newCartesian Iter: %i Cartesian coordinates obtained (rmsd = %.3e Err-dQ = %.3e)\n" % (microiter, rmsdt, ndqt))
            # Return the final result.
            self.writeCache(xyz, dQ, xyzsave)
            return xyzsave.flatten()
        fail_counter = 0
        # Start iterations.
        while True:
            microiter += 1
            # Get generalized inverse of Wilson B-matrix
            Bmat = self.wilsonB(xyz1)
            Ginv = self.GInverse(xyz1)
            # Get new Cartesian coordinates
            dxyz = damp*multi_dot([Bmat.T,Ginv,dQ1.T])
            xyz2 = xyz1 + np.array(dxyz).flatten()
            # The coordinates after the first step are saved no matter good or bad.
            if microiter == 1:
                xyzsave = xyz2.copy()
                xyz_iter1 = xyz2.copy()
            # Calculate the actual change in internal coordinates
            dQ_actual = self.calcDiff(xyz2, xyz1)
            dQ_Prims = self.Prims.calcDiff(xyz2, xyz1)
            for i in range(len(dQ_Prims)):
                if np.abs(dQ_Prims[i]) > 1:
                    logger.info("Iter: %2i LargeDiff: % 10.5f %s" % (microIter, dQ_Prims[i], self.Prims.Internals[i]))
            rmsd = np.sqrt(np.mean((np.array(xyz2-xyz1).flatten())**2))
            # dQ1-dQ_actual is the remaining IC step needed to achieve convergence
            ndq = np.linalg.norm(dQ1-dQ_actual)
            if ndq > ndqt:
                # Bad result: |dQ1-dQ_actual| increases from previous iteration
                # Discard the IC step and retry with damping.
                if verbose >= 2: logger.info("      newCartesian Iter: %i |dQ(Step)| = %.5e Err-dQ (Best) = %.5e (%.5e) RMSD: %.5e Damp: %.5e (Bad)\n" % (microiter, np.linalg.norm(dQ_actual), ndq, ndqt, rmsd, damp))
                damp /= 2
                fail_counter += 1
                xyz2 = xyz1.copy()
                dQ_actual *= 0
            else:
                if verbose >= 2: logger.info("      newCartesian Iter: %i |dQ(Step)| = %.5e Err-dQ (Best) = %.5e (%.5e) RMSD: %.5e Damp: %.5e (Good)\n" % (microiter, np.linalg.norm(dQ_actual), ndq, ndqt, rmsd, damp))
                fail_counter = 0
                damp = min(damp*1.2, 1.0)
                rmsdt = rmsd
                ndqt = ndq
                xyzsave = xyz2.copy()
            ndqs.append(ndq)
            rmsds.append(rmsd)
            # Check convergence / fail criteria
            if rmsd < 1e-6 or ndq < 1e-6:
                return finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1)
            if fail_counter >= 5:
                return finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1)
            if microiter == 50:
                return finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1)
            # The next IC step required to reach convergence.
            dQ1 = dQ1 - dQ_actual
            xyz1 = xyz2.copy()
