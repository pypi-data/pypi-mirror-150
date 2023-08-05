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

cdef extern from "libssh/ssh2.h" nogil:
    enum:
        SSH2_MSG_DISCONNECT
        SSH2_MSG_IGNORE
        SSH2_MSG_UNIMPLEMENTED
        SSH2_MSG_DEBUG
        SSH2_MSG_SERVICE_REQUEST
        SSH2_MSG_SERVICE_ACCEPT
        SSH2_MSG_KEXINIT
        SSH2_MSG_NEWKEYS
        SSH2_MSG_KEXDH_INIT
        SSH2_MSG_KEXDH_REPLY
        SSH2_MSG_KEX_ECDH_INIT
        SSH2_MSG_KEX_ECDH_REPLY
        SSH2_MSG_ECMQV_INIT
        SSH2_MSG_ECMQV_REPLY
        SSH2_MSG_KEX_DH_GEX_REQUEST_OLD
        SSH2_MSG_KEX_DH_GEX_GROUP
        SSH2_MSG_KEX_DH_GEX_INIT
        SSH2_MSG_KEX_DH_GEX_REPLY
        SSH2_MSG_KEX_DH_GEX_REQUEST
        SSH2_MSG_USERAUTH_REQUEST
        SSH2_MSG_USERAUTH_FAILURE
        SSH2_MSG_USERAUTH_SUCCESS
        SSH2_MSG_USERAUTH_BANNER
        SSH2_MSG_USERAUTH_PK_OK
        SSH2_MSG_USERAUTH_PASSWD_CHANGEREQ
        SSH2_MSG_USERAUTH_INFO_REQUEST
        SSH2_MSG_USERAUTH_GSSAPI_RESPONSE
        SSH2_MSG_USERAUTH_INFO_RESPONSE
        SSH2_MSG_USERAUTH_GSSAPI_TOKEN
        SSH2_MSG_USERAUTH_GSSAPI_EXCHANGE_COMPLETE
        SSH2_MSG_USERAUTH_GSSAPI_ERROR
        SSH2_MSG_USERAUTH_GSSAPI_ERRTOK
        SSH2_MSG_USERAUTH_GSSAPI_MIC
        SSH2_MSG_GLOBAL_REQUEST
        SSH2_MSG_REQUEST_SUCCESS
        SSH2_MSG_REQUEST_FAILURE
        SSH2_MSG_CHANNEL_OPEN
        SSH2_MSG_CHANNEL_OPEN_CONFIRMATION
        SSH2_MSG_CHANNEL_OPEN_FAILURE
        SSH2_MSG_CHANNEL_WINDOW_ADJUST
        SSH2_MSG_CHANNEL_DATA
        SSH2_MSG_CHANNEL_EXTENDED_DATA
        SSH2_MSG_CHANNEL_EOF
        SSH2_MSG_CHANNEL_CLOSE
        SSH2_MSG_CHANNEL_REQUEST
        SSH2_MSG_CHANNEL_SUCCESS
        SSH2_MSG_CHANNEL_FAILURE
        SSH2_DISCONNECT_HOST_NOT_ALLOWED_TO_CONNECT
        SSH2_DISCONNECT_PROTOCOL_ERROR
        SSH2_DISCONNECT_KEY_EXCHANGE_FAILED
        SSH2_DISCONNECT_HOST_AUTHENTICATION_FAILED
        SSH2_DISCONNECT_RESERVED
        SSH2_DISCONNECT_MAC_ERROR
        SSH2_DISCONNECT_COMPRESSION_ERROR
        SSH2_DISCONNECT_SERVICE_NOT_AVAILABLE
        SSH2_DISCONNECT_PROTOCOL_VERSION_NOT_SUPPORTED
        SSH2_DISCONNECT_HOST_KEY_NOT_VERIFIABLE
        SSH2_DISCONNECT_CONNECTION_LOST
        SSH2_DISCONNECT_BY_APPLICATION
        SSH2_DISCONNECT_TOO_MANY_CONNECTIONS
        SSH2_DISCONNECT_AUTH_CANCELLED_BY_USER
        SSH2_DISCONNECT_NO_MORE_AUTH_METHODS_AVAILABLE
        SSH2_DISCONNECT_ILLEGAL_USER_NAME
        SSH2_OPEN_ADMINISTRATIVELY_PROHIBITED
        SSH2_OPEN_CONNECT_FAILED
        SSH2_OPEN_UNKNOWN_CHANNEL_TYPE
        SSH2_OPEN_RESOURCE_SHORTAGE
        SSH2_EXTENDED_DATA_STDERR
