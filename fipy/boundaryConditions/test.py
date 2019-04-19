"""Test numeric implementation of the mesh
"""

__all__ = []

from fipy.tests.doctestPlus import _LateImportDocTestSuite
import fipy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(
        docTestModuleNames = (
            'fipy.boundaryConditions.boundaryCondition',
            'fipy.boundaryConditions.fixedFlux',
        ))

if __name__ == '__main__':
    fipy.tests.testProgram.main(defaultTest='_suite')
