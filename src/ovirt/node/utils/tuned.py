#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# tuned.py - Copyright (C) 2012 Red Hat, Inc.
# Written by Mike Burns <mburns@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.  A copy of the GNU General Public License is
# also available at http://www.gnu.org/copyleft/gpl.html.

"""
Some convenience functions related to tuned profiles
"""

from ovirt.node.utils import process
import re


def get_available_profiles():
    """Gets a list of tuned profiles available on the system.

    Returns:
        A list of profiles
    """
    prof_list = [u'None']
    for i in process.check_output("/usr/sbin/tuned-adm list").split("\n"):
        if "- " in i:
            prof_list.append(i.replace("- ", ""))
    return prof_list


def get_active_profile():
    """Gets the active tuned profile on the system.

    Returns:
        A string with the active tuned profile
    """
    try:
        profile = process.check_output("/usr/sbin/tuned-adm active")
    except:
        return "None"
    return re.match(r'.*?: (.*)', profile).group(1)


def set_active_profile(profile):
    """Sets the active tuned profile on the system.

    Returns:
        A boolean based on the return of tuned-adm
    """
    try:
        if (profile == "None" or profile == "off"):
            ret = process.check_call("/usr/sbin/tuned-adm off")
            if not ret == 0:
                raise Exception("DISABLE")
                raise Exception("Failed to disable tuned")
        elif profile not in get_available_profiles():
            raise Exception("%s is not a known profile" % profile)
        else:
            ret = process.check_call("/usr/sbin/tuned-adm profile %s"
                                     % profile)
            if not ret == 0:
                raise Exception("Failed to set profile to %s" % profile)
    except Exception as e:
        print e
        return False

    return True
