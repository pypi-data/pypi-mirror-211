    def newCartesian(self, xyz, dQ, verbose=True):
        cached = self.readCache(xyz, dQ)
        if cached is not None:
            # print "Returning cached result"
            return cached
        xyz1 = xyz.copy()
        dQ1 = dQ.copy()
        # Iterate until convergence:
        microiter = 0
        ndqs = [np.linalg.norm(dQ)]
        ndqt = ndqs[0]
        rmsds = []
        self.bork = False
        # Damping factor
        damp = 1.0
        # Function to exit from loop
        if verbose >= 2: logger.info("    InternalCoordinates.newCartesian converting internal to Cartesian step (desired |dQ| = %.3e)\n" % np.linalg.norm(dQ))
        def finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1):
            if ndqt > 1e-1:
                if verbose: logger.info("      newCartesian Iter: %i Failed to obtain coordinates (rmsd = %.3e |dQ| = %.3e)\n" % (microiter, rmsdt, ndqt))
                self.bork = True
                self.writeCache(xyz, dQ, xyz_iter1)
                return xyz_iter1.flatten()
            elif ndqt > 1e-3:
                if verbose: logger.info("      newCartesian Iter: %i Approximate coordinates obtained (rmsd = %.3e |dQ| = %.3e)\n" % (microiter, rmsdt, ndqt))
            else:
                if verbose: logger.info("      newCartesian Iter: %i Cartesian coordinates obtained (rmsd = %.3e |dQ| = %.3e)\n" % (microiter, rmsdt, ndqt))
            self.writeCache(xyz, dQ, xyzsave)
            return xyzsave.flatten()
        fail_counter = 0
        while True:
            microiter += 1
            Bmat = self.wilsonB(xyz1)
            Ginv = self.GInverse(xyz1)
            # Get new Cartesian coordinates
            dxyz = damp*multi_dot([Bmat.T,Ginv,dQ1.T])
            xyz2 = xyz1 + np.array(dxyz).flatten()
            if microiter == 1:
                xyzsave = xyz2.copy()
                xyz_iter1 = xyz2.copy()
            # Calculate the actual change in internal coordinates
            dQ_actual = self.calcDiff(xyz2, xyz1)
            dQ_Prims = self.Prims.calcDiff(xyz2, xyz1)
            for i in range(len(dQ_Prims)):
                if np.abs(dQ_Prims[i]) > 1:
                    print("LargeDiff: % 10.5f %s" % (dQ_Prims[i], self.Prims.Internals[i]))
                    M = Molecule()
                    M.elem = self.Prims.elem
                    na = len(self.Prims.elem)
                    M.xyzs = [xyz.reshape(-1,3)*bohr2ang, xyz1.reshape(-1,3)*bohr2ang, xyz2.reshape(-1,3)*bohr2ang]
                    M.write("largediff.xyz")
                    sys.exit()
            rmsd = np.sqrt(np.mean((np.array(xyz2-xyz1).flatten())**2))
            ndq = np.linalg.norm(dQ1-dQ_actual)
            if ndq > ndqt:
                if verbose >= 2: logger.info("      newCartesian Iter: %i |dxyz| = %.5f |dQ(Step)| = %.5e Err-dQ (Best) = %.5e (%.5e) RMSD: %.5e Damp: %.5e (Bad)\n" % (microiter, np.linalg.norm(dxyz), np.linalg.norm(dQ_actual), ndq, ndqt, rmsd, damp))
                damp /= 2
                fail_counter += 1
                # The step fails and should be discarded completely.
                xyz2 = xyz1.copy()
                dQ_actual *= 0
                # dQ_actual *= 0.0
            else:
                if verbose >= 2: logger.info("      newCartesian Iter: %i |dxyz| = %.5f |dQ(Step)| = %.5e Err-dQ (Best) = %.5e (%.5e) RMSD: %.5e Damp: %.5e (Good)\n" % (microiter, np.linalg.norm(dxyz), np.linalg.norm(dQ_actual), ndq, ndqt, rmsd, damp))
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
            if fail_counter >= 50:
                return finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1)
            if microiter == 100:
                return finish(microiter, rmsdt, ndqt, xyzsave, xyz_iter1)
            # Figure out the further change needed
            # Maybe this is the problematic part??
            # dQ1 = self.calcDiff(val1=dQ1, val2=dQ_actual)
            dQ1 = dQ1 - dQ_actual
            # dQ1 = self.calcDiff(
            xyz1 = xyz2.copy()
