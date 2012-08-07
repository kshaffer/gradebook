#!/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python

# Python module for a standards-based/criterion-referenced/objectives-based gradebook and report generator.

# Copyright (C) 2012 Kris P. Shaffer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import sys
import os


class Student():

	def __init__(self, filename):
		self.data = []

		self.filename = filename
		self.name = filename.split('.')[0]

	def assessments(self):
		f = open(self.filename, 'rb')
		r = csv.reader(f, delimiter=',')
		assessmentList = []
		assessmentList.extend(r)
		assessmentList.pop(0)
		return assessmentList
		
	def criteria(self):
		criteriaList = []
		for assessment in self.assessments():
			criteriaList.append(assessment[0])
		return criteriaList

	def categories(self):
		categoryList = []
		for assessment in self.assessments():
			categoryList.append(assessment[1])
		return sorted(set(categoryList))
		
#	def categoryTable(self, category):
		