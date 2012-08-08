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

instructor = 'Kris P. Shaffer'


class Student():

	def __init__(self, filename):
		self.data = []

		self.filename = filename
		self.name = filename.split('.')[0]
		self.latexHeader = 'latex input: mmd-article-header\n' + 'Title: Grade report for ' + self.name + '\n' + 'Author: ' + instructor + '\n' + 'Base Header Level: 2' + '\n' + 'latex mode: memoir' + '\n' + 'latex input: mmd-article-begin-doc' + '\n' + 'latex footer: mmd-memoir-footer\n\n'



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
		
	def categoryTable(self, category):
		table = '| Objective | Status | Scale | Assessment 1 | Date 1 | Assessment 2 | Date 2 |\n'
		table += '| --: | :-: | :-: | :-: | :-: | :-: | :-: |\n'
		for assess in self.assessments():
			if assess[1] == category:
				table += ("| " + assess[0] + " | " + assess[2] + " | " + assess[3] + " | " + assess[4] + " | " + assess[5] + " | " + assess[6] + " | " + assess[7] + " |\n")
		table += '[Assessments for ' + category + ']\n'
		return table
		
	def report(self, course):
		report = self.latexHeader + '\n'
		for category in course.categories():
			report += self.categoryTable(category)
			report += '\n\n'
		return report
		
	def writeReport(self, course):
		reportFile = self.name.split('.')[0] + '-report.md'
		f = open(reportFile, 'wb')
		f.write(self.report(course))
		print('Report generated for ' + self.name)
		return 0
		
		
class Course():

	def __init__(self):
		self.data = []
		
	def assessments(self):
		
		assessments = []
		for stud in self.roster():
			assessList = Student(stud).assessments()
			for assess in assessList:
				assessments.append(assess)
		return sorted(set(assessments))

	def categories(self):
		
		categories = []
		for stud in self.roster():
			catList = Student(stud).categories()
			for cat in catList:
				categories.append(cat)
		return sorted(set(categories))

	def roster(self):
		roster = []
		for filename in os.listdir('./'):
			if filename.split('.')[1] == 'csv':
				roster.append(filename)
		i = 0
		for file in roster:
			if file == 'studentTemplate.csv':
				roster.pop(i)
			i = i + 1
		return roster
			