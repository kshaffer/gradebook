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


class Student(object):

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
		
	def percentPassed(self, category):
		objectives = 0
		passed = 0
		for assess in self.assessments():
			if assess[1] == category:
				objectives += 1
				if assess[2] == 'P':
					passed += 1
		return int(100 * float(passed) / float(objectives))
		
	def percentAttempted(self, category):
		attempts = 0
		objectives = 0
		for assess in self.assessments():
			if assess[1] == category:
				objectives += 1
				if assess[2] == 'P':
					attempts += 1
				if assess[2] == 'A':
					attempts += 1
		return int(100 * float(attempts) / float(objectives))
		
	def report(self, course):
		report = self.latexHeader + '\n\n'
		report += self.summaryTable(course)
		report += '<!--\pagebreak-->\n\n'
		for category in course.categories():
			report += self.categoryTable(category)
			report += '\n\n'
		return report
		
	def writeReport(self, course):
		reportFile = self.name.split('.')[0] + '-report.md'
		f = open(reportFile, 'wb')
		f.write(self.report(course))
		print('Report generated for ' + self.name)
	
	def summaryTable(self, course):
		table = '| Category | Objectives met | Objectives attempted |\n'
		table += '| --: | :-: | :-: |\n'
		for category in course.categories():
			table += ('| ' + category + ' | ' + str(self.percentPassed(category)) + ' | ' + str(self.percentAttempted(category)) + ' |\n')
		table += '[Summary of course objectives met by category.]\n\n'
		return table
		
		
class Course(object):

	def __init__(self, name):
		self.data = []
		self.name = name
		self.latexHeader = 'latex input: mmd-article-header\n' + 'Title: Class report for ' + self.name + '\n' + 'Author: ' + instructor + '\n' + 'Base Header Level: 2' + '\n' + 'latex mode: memoir' + '\n' + 'latex input: mmd-article-begin-doc' + '\n' + 'latex footer: mmd-memoir-footer\n\n'
		
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
		return sorted(set(roster))
		
	def classReportTable(self, category):
		table = '| Student | Objectives met | Objectives attempted |\n'
		table += '| --: | :-: | :-: |\n'
		for student in self.roster():
			stud = Student(student)
			report = '| ' + stud.name + ' | ' + str(stud.percentPassed(category)) + ' | ' + str(stud.percentAttempted(category)) + ' |\n'
			table += report
		table += '[Assessments for ' + category + ']\n'
		return table
		
	def classReport(self):
		report = self.latexHeader + '\n\n'
		for category in self.categories():
			report += self.classReportTable(category)
			report += '\n\n'
		return report
		
	def writeReport(self):
		reportFile = 'courseReport.md'
		f = open(reportFile, 'wb')
		f.write(self.classReport())
		print('Report generated for ' + self.name)
	
			
			