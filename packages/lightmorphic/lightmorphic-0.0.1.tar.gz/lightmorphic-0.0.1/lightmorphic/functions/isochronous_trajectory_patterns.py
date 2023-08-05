"""
=============
Created on Mon May 29 12:00:00 2023
=============
@author: Damian
=============
Assessing and mapping isochronous trajectory patterns to specific locations
=============
"""
def travel_time(m):
    """The required time to travel between specific locations."""
    return m

def state_change(m):
    """For 1 time step."""
    return m

def vim(m):
    """The velocity isochronous matrix."""
    return m

def nn_vim(m):
    """The number of nodes that make the velocity isochronous matrix."""
    return m

def ptp(m):
    """Predictive trajectory paths"""
    return m

def flags(m):
    """Specific isochronous surface type and flag such segmentation surfaces that lead to changes in the trajectory path."""
    return m

def triangle_mesh(m):
    """2D geometric mesh used to represent the discretization of the geometric domain into smaller and simpler shapes."""
    return m

def quadrilateral_mesh(m):
    """2D geometric mesh used to represent the discretization of the geometric domain into smaller and simpler shapes."""
    return m

def tetrahedral_mesh(m):
    """3D geometric mesh used to represent the discretization of the geometric domain into smaller and simpler shapes."""
    return m

def hexahedral_mesh(m):
    """3D geometric mesh used to represent the discretization of the geometric domain into smaller and simpler shapes."""
    return m

def isc(m):
    """The isochronous surface chords.
    If one of the chords is disturbed, the disturbance is instantaneous transmitted troughout the complete trajectory.
    By observing the amplitude of the chords disturbance it will be possible to build predictive paths for the remaining
    trajectory while at the same time updating the already known path."""
    return m

def iscv(m):
    """The isochronous surface chords vibrations signal the intent to change the trajectory."""
    return m

def cvpp(m):
    """The chords vibrations propagation probability."""
    return m

