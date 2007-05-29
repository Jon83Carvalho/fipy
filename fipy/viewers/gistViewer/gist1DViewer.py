#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "gist1DViewer.py"
 #                                    created: 11/10/03 {2:48:25 PM} 
 #                                last update: 2/21/07 {12:19:53 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

__docformat__ = 'restructuredtext'

from fipy.tools import numerix
 
from fipy.viewers.gistViewer.gistViewer import GistViewer

class Gist1DViewer(GistViewer):
    """
    Displays a y vs. x plot of one or more 1D `CellVariable` objects.

        >>> from fipy import *
        >>> mesh = Grid1D(nx=100)
        >>> x = mesh.getCellCenters()[...,0]
        >>> var1 = CellVariable(mesh=mesh, name=r"$sin(x)$", value=numerix.sin(x))
        >>> var2 = CellVariable(mesh=mesh, name=r"$cos(x/\pi)$", value=numerix.cos(x / numerix.pi))
        >>> viewer = Gist1DViewer(vars=(var1, var2), 
        ...                       limits={'xmin':10, 'xmax':90, 'datamin':-0.9, 'datamax':2.0},
        ...                       title="Gist1DViewer test")
        >>> viewer._promptForOpinion()
        >>> del viewer

    """
    
    def __init__(self, vars, title = None, limits = None, xlog = 0, ylog = 0, style = "work.gs"):
        """
        Creates a `Gist1DViewer`.
        
        :Parameters:
          - `vars`: a `CellVariable` or tuple of `CellVariable` objects to plot
          - `limits`: a dictionary with possible keys `'xmin'`, `'xmax'`, 
            `'datamin'`, `'datamax'`. Any limit set to a (default) value of
            `None` will autoscale.
          - `title`: displayed at the top of the Viewer window
          - `xlog`: set `True` to give logarithmic scaling of the x axis
          - `ylog`: set `True` to give logarithmic scaling of the y axis
          - `style`: the Gist style file to use

        """
        GistViewer.__init__(self, vars = vars, limits = limits, title = title)
        
        self.xlog = xlog
        self.ylog = ylog
        self.style = style
        
    def _getSuitableVars(self, vars):
        from fipy.variables.cellVariable import CellVariable
        vars = [var for var in GistViewer._getSuitableVars(self, vars) \
          if (var.getMesh().getDim() == 1 and isinstance(var, CellVariable))]
        if len(vars) > 1:
            vars = [var for var in vars if var.getMesh() is vars[0].getMesh()]
        if len(vars) == 0:
            from fipy.viewers import MeshDimensionError
            raise MeshDimensionError, "Can only plot 1D data"
        return vars
        
    def _getArrays(self):
        arrays = []
        
        for var in self.vars:
            arrays.append((numerix.array(var), numerix.array(var.getMesh().getCellCenters()[:,0])))
            
        return arrays
        
    def _plotArrays(self):
        import gist
        
        for array in self._getArrays():
            gist.plg(*array)
            
        gist.logxy(self.xlog, self.ylog)

    def plot(self, filename = None):
        """
        Plot the `CellVariable` or list of `CellVariables` as a y vs x plot.
        """
        import gist

        gist.window(self.id, wait = 1, style = self.style)
        gist.pltitle(self.title)
        gist.animate(1)

        if self.limits != None:
            gist.limits(self._getLimit('xmin'), 
                        self._getLimit('xmax'), 
                        self._getLimit(('datamin', 'ymin')), 
                        self._getLimit(('datamax', 'ymax')))
            
        self._plotArrays()
            
        GistViewer.plot(self, filename = filename)

if __name__ == "__main__": 
    import fipy.tests.doctestPlus
    fipy.tests.doctestPlus.execButNoTest()