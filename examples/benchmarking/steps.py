#!/usr/bin/env python

##
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # of Standards and Technology, an agency of the Federal Government.
 # Pursuant to title 17 section 105 of the United States Code,
 # United States Code this software is not subject to copyright
 # protection, and this software is considered to be in the public domain.
 # FiPy is an experimental system.
 # NIST assumes no responsibility whatsoever for its use by whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 #
 # To the extent that NIST may hold copyright in countries other than the
 # United States, you are hereby granted the non-exclusive irrevocable and
 # unconditional right to print, publish, prepare derivative works and
 # distribute this software, in any medium, or authorize others to do so on
 # your behalf, on a royalty-free basis throughout the world.
 #
 # You may improve, modify, and create derivative works of the software or
 # any portion of the software, and you may copy and distribute such
 # modifications or works.  Modified works should carry a notice stating
 # that you changed the software and should note the date and nature of any
 # such change.  Please explicitly acknowledge the National Institute of
 # Standards and Technology as the original source.
 #
 # This software can be redistributed and/or modified freely provided that
 # any derivative works bear some notice that they are derived from it, and
 # any modified versions bear some notice that they have been modified.
 # ========================================================================
 #
 # ###################################################################
 ##

import os
import sys
import re
from subprocess import Popen, PIPE

from fipy.tools.parser import parse

from examples.benchmarking.utils import monitor

steps = parse('--numberOfSteps', action='store',
              type='int', default=20)

blocks = parse('--numberOfBlocks', action='store',
               type='int', default=20)

benchmarker = os.path.join(os.path.dirname(__file__),
                           "benchmarker.py")

args = sys.argv[1:]

p = Popen(["python", benchmarker] + args
          + ["--numberOfSteps=0"],
          stdout=PIPE,
          stderr=PIPE)

cpu0, rsz0, vsz0 = monitor(p)

print "step\tcpu / (s / step / cell)\trsz / (B / cell)\tvsz / (B / cell)"

for block in range(blocks):
    p = Popen(["python", benchmarker,
               "--startingStep=%d" % (block * steps),
               "--cpuBaseLine=%f" % cpu0] + args,
              stdout=PIPE,
              stderr=PIPE)

    cpu, rsz, vsz = monitor(p)

    print "%d\t%g\t%g\t%g" % (block * steps, cpu, rsz, vsz)
