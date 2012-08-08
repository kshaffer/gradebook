#!/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python
from gradebook import *

studentNames = []
c = Course(course)
for student in c.roster():
	s = Student(student)
	studentNames.append(s.name)
	s.writeReport(c)

c.writeReport()

for name in studentNames:
	mmd(name)
	os.system('mv ' + name + '-report.pdf ' + name + '/')
	
os.system('multimarkdown -t latex courseReport.md > courseReport.tex')
os.system('latexmk -f courseReport.tex')
os.system('pdflatex courseReport.tex')
os.system('latexmk -c courseReport.tex')

os.system('rm *.dvi')
os.system('rm *.glo')
os.system('rm *.ist')
os.system('rm *.tex')
os.system('rm *.md')