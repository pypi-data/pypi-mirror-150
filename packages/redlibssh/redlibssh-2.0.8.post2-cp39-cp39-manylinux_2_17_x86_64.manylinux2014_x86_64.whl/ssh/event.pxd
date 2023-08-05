# This file is part of RedLibSSH.
# Copyright (C) 2018 Panos Kittenis
# Copyright (C) 2022 Red-M
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-130

from .session cimport Session
from .connector cimport Connector

from . cimport c_ssh


cdef class Event:
    cdef c_ssh.ssh_event _event
    cdef object _sock
    cdef readonly Session session
    cdef readonly Connector connector

    @staticmethod
    cdef Event from_ptr(c_ssh.ssh_event _event)

    @staticmethod
    cdef int event_callback(c_ssh.socket_t fd, int revent, void *userdata)
