#!/usr/bin/env python

"""ExtractPaperFeatures.py: extract various features detailed according to literature review"""

__author__      = "James Marquardt"
__copyright__   = "Copyright 2015, UWT"

import tldextract, csv, sys, codecs, timeit
from MeaningfulCharacters import meaningful_characters
from EntropyExtractor import domain_entropy

print "Extracting DGA Features"
start_time = timeit.default_timer()
with open("DGA_Data", "rU") as infile1, open("DGA_PaperFeatures_no_mcr.csv", "wb") as outfile:

	writer = csv.writer(outfile)
	#writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","domain_mcr","subdomain_mcr","url_entropy","domain_entropy","subdomain_entropy"])
	writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","url_entropy","domain_entropy","subdomain_entropy"])


	line_count = 0

	for line in infile1:
		line_count += 1
		domain = line.split("\t")[0].strip()
		label = line.split("\t")[1].strip()

		tld = tldextract.extract(domain)

		row = []

		#class and url
		row.append(label)
		row.append(domain)

		#TLD info
		row.append(tld.subdomain)
		row.append(tld.domain)
		row.append(tld.suffix)

		#length
		row.append(len(domain))
		row.append(len(tld.subdomain))
		row.append(len(tld.domain))
		row.append(len(tld.suffix))

		#dots
		row.append(domain.count("."))

		#meaningful characters ratio
		'''
		row.append(meaningful_characters(tld.domain))
		row.append(meaningful_characters(tld.subdomain))
		'''

		#shannon entropy
		row.append(domain_entropy(domain))
		row.append(domain_entropy(tld.domain))
		row.append(domain_entropy(tld.subdomain))

		writer.writerow(row)

		if line_count % 10000 == 0:
			print line_count

elapsed = timeit.default_timer() - start_time
print "DGA features extracted in " + str(elapsed) + " seconds"

print "Extracting Alexa Features"
start_time = timeit.default_timer()
with codecs.open("Alexa_top_1M_country", "rU", encoding='utf-8') as infile1, open("Alexa_PaperFeatures_no_mcr.csv", "wb") as outfile:

	line_count = 0

	tld_errors = 0
	write_errors = 0

	writer = csv.writer(outfile)
	#writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","domain_mcr","subdomain_mcr","url_entropy","domain_entropy","subdomain_entropy"])
	writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","url_entropy","domain_entropy","subdomain_entropy"])


	for line in infile1:
		line_count+=1
		domain = line.split(" ")[0].strip()
		label = "Non-DGA"

		try:
			tld = tldextract.extract(domain)
		except:
			tld_errors += 1
			continue

		row = []


		#class and url
		row.append(label)
		row.append(domain)

		#TLD info
		row.append(tld.subdomain)
		row.append(tld.domain)
		row.append(tld.suffix)

		#length
		row.append(len(domain))
		row.append(len(tld.subdomain))
		row.append(len(tld.domain))
		row.append(len(tld.suffix))

		#dots
		row.append(domain.count("."))

		#meaningful characters ratio
		'''
		row.append(meaningful_characters(tld.domain))
		row.append(meaningful_characters(tld.subdomain))
		'''

		#shannon entropy
		row.append(domain_entropy(domain))
		row.append(domain_entropy(tld.domain))
		row.append(domain_entropy(tld.subdomain))

		try:
			writer.writerow(row)
		except UnicodeEncodeError, UnicodeError:
			#print row
			write_errors += 1

		if line_count % 10000 == 0:
			print line_count

	print "There were " + str(write_errors) + " write errors in Alexa"
	print "There were " + str(tld_errors) + " tld errors in Alexa"
