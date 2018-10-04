# py3.6
# still cannot search the word that does not exist in posting list
import re
import pdb
import math

def parseString(txt):
	## parse a string into a list of words
	## remove space, punctuations and words shorter than 4
	## return: para_new: list of parsed words
	para = txt.split(' ')
	para_new = []
	for word in para:
		word = re.sub(r'[^a-zA-Z0-9]', '', word)
		if len(word)<4:
			word = ''
		if len(word)>=1 and word[-1] == 's':
			word = word[0:-1]
		if word != '':
			para_new.append(word)
	return para_new

def makeIndex(paras):
	## return: index: a dict {"word":[N lists: pos of word in each para]}
	index = {}
	for did in range(N):
		for pos in range(len(paras[did])):
			if not index.get(paras[did][pos]):
				index[paras[did][pos]]=[[] for i in range(N)]
				index[paras[did][pos]][did].append(pos)
			else:
				index[paras[did][pos]][did].append(pos)
	return index

def Weight(keywords, did):
	## keywords: list of keywords
	## did: index of para
	## return weights 1*len(query)
	weights = []
	# pdb.set_trace()
	for keyword in keywords:
		# keyword = re.sub(r'[^a-zA-Z0-9]', '', keyword)
		tf = len(index[keyword][did])/len(paras[did])
		tcall = [len(index[key][did]) for key in index]
		tfmax = max(tcall)/len(paras[did])
		df = N-index[keyword].count([])
		idf = math.log(N/df,2)
		weights.append(tf*idf/tfmax)
	return weights


def CosSim(w1,w2):
	## cosine similarity
	## "(w1 dot w2)/{||w1||*||w2||)"
	sumxx = 0
	sumxy = 0
	sumyy = 0
	for i in range(len(w1)):
		x = w1[i]; y = w2[i]
		sumxx += x*x
		sumyy += y*y
		sumxy += x*y
		# pdb.set_trace()
	if sumxx*sumyy==0:
		return 0
	else:
		return sumxy/math.sqrt(sumxx*sumyy)

def Search(query):
	# query: query string
	# return 3 top result did: [did1,did2,did3]
	keywords = parseString(query)
	weight_q = [1]*len(keywords)
	cossim = [CosSim(weight_q,Weight(keywords,did)) for did in range(N)]
	# pdb.set_trace()
	cossim = [(cossim[i],i) for i in range(len(cossim))]
	# pdb.set_trace()
	cossim.sort(reverse=True, key=lambda k:k[0])
	return cossim[0:3]

def findUniqueKeyword(did):
	count=0
	words_u = []
	for word in paras[did]:
		if sum([bool(i) for i in index[word]]) == 1:
			count+=1
			words_u.append(word)
	return (count,words_u)


def showResult(query, result):
	## res: list of result (cossim_score,did)
	# pdb.set_trace()
	print('Result for "'+query+'":')
	for res in result:
		print('D'+str(res[1]))
		print('number of unique keywords = %d' % findUniqueKeyword(res[1])[0])
		# print(findUniqueKeyword(res[1])[1])
		keywords_5 = []
		for key in index:
			keywords_5.append((key,Weight([key],res[1])[0]))
		keywords_5 = sorted(keywords_5, reverse=True, key=lambda k:k[1])[0:5]
		posting_list = ""
		for keyword in keywords_5:
			key = keyword[0]
			posting = key+'\t\t-> | '
			for did in range(N):
				if index[key][did]!=[]:
					posting+=("D%d:%s | " %(did,str(index[key][did])[1:-1]))
			posting_list+=posting+"\n"
		print(posting_list)
		weights = Weight(parseString(query),res[1])
		L2_norm = 0
		for w in weights:
			L2_norm+=w*w
		L2_norm = math.sqrt(L2_norm)
		print("L2_norm of document vector = "+str(L2_norm))
		print("cosine similarity score = "+str(res[0])+'\n')



file = open("collection-100.txt")
## paragraph strings
texts = file.read().split('\n\n')
N = len(texts)
## text_new: the peprocessed text string
text_new = ""
## paras: list of paragraphs, which are splitted by word
paras = []
for txt in texts:
	## para: a paragraph splitted into a list of words
	para = parseString(txt)
	txt_new = ''
	for word in para:
		txt_new += word
	paras.append(para)
	text_new += (txt_new+'\n\n')
# pdb.set_trace()
## writing th processed text
fo = open("doc_processed.txt",'w')
fo.write(text_new)

## index: a dict {"word":[N lists: pos of word in each para]}
index = makeIndex(paras)

## output the posting.txt
posting_list = ""
for key in index:
	posting = key+'\t\t-> | '
	for did in range(N):
		if index[key][did]!=[]:
			posting+=("D%d:%s | " %(did,str(index[key][did])[1:-1]))
	posting_list+=posting+"\n"
fo_posting = open("posting.txt",'w')
fo_posting.write(posting_list)

queries = ['bank','stock banking','the company share','company benefit shares','"Brown Forman"']
# query = 'bank'
# query ='"Brown Forman"'
# query = 'stock banking'
# query = 'the company share'
# query = 'company benefit shares'
for query in queries:
	result = Search(query)
	showResult(query,result)