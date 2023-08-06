class Exponential(PrimitiveCoordinate):
    def __init__(self, a, b, rab=1.0, alpha=1.0, w=1.0):
        self.a = a
        self.b = b
        self.rab = rab
        self.alpha = alpha
        self.w = 1.0
        if a == b:
            raise RuntimeError('a and b must be different')
        self.isAngular = False
        self.isPeriodic = False

    def __repr__(self):
        return "Exponential %i-%i (rab=%.3f alpha=%.3f w=%.3f)" % (self.a+1, self.b+1, self.rab, self.alpha, self.w)
        
    def __eq__(self, other):
        if type(self) is not type(other): return False
        if self.a == other.a:
            if self.b == other.b:
                return True
        if self.a == other.b:
            if self.b == other.a:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def value(self, xyz):
        xyz = xyz.reshape(-1,3)
        a = self.a
        b = self.b
        rab = self.rab
        alpha = self.alpha
        w = self.w
        r = np.linalg.norm(xyz[a] - xyz[b])
        answer = w*np.exp(-alpha*(r-rab)/rab)
        return answer
    
    def derivative(self, xyz):
        xyz = xyz.reshape(-1,3)
        a = self.a
        b = self.b
        rab = self.rab
        alpha = self.alpha
        w = self.w

        r = np.linalg.norm(xyz[a] - xyz[b])
        derivatives = np.zeros_like(xyz)

        u = (xyz[a] - xyz[b]) / r
        prefactor = -(w * alpha / rab) * np.exp(-alpha*(r-rab)/rab)
        derivatives[a, :] = u * prefactor
        derivatives[b, :] = -u * prefactor
        return derivatives

    def second_derivative(self, xyz):
        xyz = xyz.reshape(-1,3)
        a = self.a
        b = self.b
        rab = self.rab
        alpha = self.alpha
        w = self.w

        r = np.linalg.norm(xyz[a] - xyz[b])
        deriv2 = np.zeros((xyz.shape[0], xyz.shape[1], xyz.shape[0], xyz.shape[1]))

        u = (xyz[a] - xyz[b]) / r
        mtx = (np.outer(u, u) - np.eye(3)) / r
        prefactor = -(w * alpha / rab) * np.exp(-alpha*(r-rab)/rab)
        prefactor2 = (w * alph / rab)**2 * np.exp(-alpha*(r-rab)/rab)
        deriv2[a, :, a, :] = -mtx * prefactor + np.outer(u, u) * prefactor2
        deriv2[b, :, b, :] = -mtx * prefactor + np.outer(u, u) * prefactor2
        deriv2[a, :, b, :] =  mtx * prefactor - np.outer(u, u) * prefactor2
        deriv2[b, :, a, :] =  mtx * prefactor - np.outer(u, u) * prefactor2
        return deriv2

