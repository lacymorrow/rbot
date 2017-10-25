def bot_login():
	print "Logging in..."
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
	print "Logged in!"

	return r

def run_bot(r, comments_replied_to):
	# list of manipulated subs: subscribed subreddits (currently defaults)
	subscribed = list(r.user.subreddits(limit=None))

	# get top posts from all time
	top_posts = r.subreddit('all').top('all', limit=10)
	for post in top_posts:
		post.age = datetime.date.today() - datetime.date.fromtimestamp(post.created)
			# check if post is old enough to warrant a repost
			if(post.age > AGE_THRESHOLD):
				create_post(post)



	# Get the newest submissions from a subreddit ('all')
	# for submission in r.subreddit('askreddit').stream.submissions():
	#     print(submission)


	## print "subscribed to " str(subscribed)
	#print "most subscribers" + str(subs.most_subscribed_subs)
	#print "most activity" + str(subs.most_active_subs)

	active_subs = ['test'] 

	# for comment in r.subreddit('test').comments(limit=10):
	# 	if "!joke" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
	# 		print "String with \"!joke\" found in comment " + comment.id

	# 		comment_reply = "You requested a Chuck Norris joke! Here it is:\n\n"

	# 		joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke']

	# 		comment_reply += ">" + joke

	# 		comment_reply += "\n\nThis joke came from [ICNDb.com](http://icndb.com)."

	# 		comment.reply(comment_reply)
	# 		print "Replied to comment " + comment.id

	# 		comments_replied_to.append(comment.id)

	# 		with open ("comments_replied_to.txt", "a") as f:
	# 			f.write(comment.id + "\n")

	print "10 seconds..."
	#Sleep for 10 seconds...
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to







	
# print(dir(gensim))

# raw_documents = ["I'm taking the show on the road.",
#                  "My socks are a force multiplier.",
#                "I am the barber who cuts everyone's hair who doesn't cut their own.",
#                "Legend has it that the mind is a mad monkey.",
#                "I make my own fun."]
# print "Number of documents: ", len(raw_documents)


# # We will use NLTK to tokenize.
# # A document will now be a list of tokens.
# from nltk.tokenize import word_tokenize
# gen_docs = [[w.lower() for w in word_tokenize(text)] 
#             for text in raw_documents]
# print str(gen_docs) + "\n"

# # We will create a dictionary from a list of documents. A dictionary maps every word to a number.
# dictionary = gensim.corpora.Dictionary(gen_docs)

# # print("dict", str(dictionary[5]))
# # print('assd', str(dictionary.token2id['road']))
# print "Number of words in dictionary: ",len(dictionary)
# for i in range(len(dictionary)):
#     print i, dictionary[i]

# # Now we will create a corpus. A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times each word occurs in the document.
# corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
# print corpus

# # Now we create a tf-idf model from the corpus. Note that num_nnz is the number of tokens.
# tf_idf = gensim.models.TfidfModel(corpus)
# print(tf_idf)
# s = 0
# for i in corpus:
#     s += len(i)
# print(s)

# 

# sims = gensim.similarities.Similarity('/usr/workdir/',tf_idf[corpus],
#                                       num_features=len(dictionary))
# print 'sims' + str(   sims)
# print 'sims type' + str(  sims)

# query_doc = [w.lower() for w in word_tokenize("Socks are a force for good.")]
# print(query_doc)
# query_doc_bow = dictionary.doc2bow(query_doc)
# print(query_doc_bow)
# query_doc_tf_idf = tf_idf[query_doc_bow]
# print(query_doc_tf_idf)


# sims[query_doc_tf_idf]