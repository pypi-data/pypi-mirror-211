# Copyright (C) 2020-2023 Sebastian Blauth
#
# This file is part of cashocs.
#
# cashocs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cashocs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cashocs.  If not, see <https://www.gnu.org/licenses/>.

"""Database for geometry."""

from __future__ import annotations

from typing import TYPE_CHECKING

import fenics
import mpi4py.MPI

from cashocs import _utils

if TYPE_CHECKING:
    from petsc4py import PETSc

    from cashocs._database import function_database


class GeometryDatabase:
    """Database for geometry parameters."""

    transfer_matrix: PETSc.Mat
    old_transfer_matrix: PETSc.Mat

    def __init__(self, function_db: function_database.FunctionDatabase) -> None:
        """Initializes the geometry database.

        Args:
            function_db: The database for function parameters.

        """
        self.mesh: fenics.Mesh = function_db.state_spaces[0].mesh()
        self.dx: fenics.Measure = fenics.Measure("dx", self.mesh)
        self.mpi_comm: mpi4py.MPI.Intracomm = self.mesh.mpi_comm()

        self.function_db = function_db

    def init_transfer_matrix(self) -> None:
        """Initializes the transfer matrix for computing the global deformation."""
        interp = _utils.Interpolator(
            self.function_db.control_spaces[0], self.function_db.control_spaces[0]
        )
        self.transfer_matrix = interp.transfer_matrix
