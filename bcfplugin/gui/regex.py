"""
Copyright (C) 2019 PODEST Patrick

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

"""
Author: Patrick Podest
Date: 2019-08-16
Github: @podestplatz

**** Description ****
This file's purpose is just to provide some RegExp used by some parts of the
plugin.
"""

dueDateRegex = "\d{4}-[01]\d-[0-3]\d"
""" RegExp for the DueDate field """

emailRegex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)|(^\s*$)"
""" RegExp to check entered E-Mail addresses for validity. """
