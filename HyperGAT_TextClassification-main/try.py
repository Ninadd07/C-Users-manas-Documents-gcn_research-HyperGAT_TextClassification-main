def read_file(dataset, LDA=True):
    doc_content_list = []
    doc_sentence_list = []
    f = open('trydata/' + dataset + '_corpus.txt', 'rb')

    for line in f.readlines():
        doc_content_list.append(line.strip().decode('latin1'))
        doc_sentence_list.append(tokenize.sent_tokenize(clean_str_simple_version(doc_content_list[-1], dataset)))
    f.close()

    doc_content_list = clean_document(doc_sentence_list, dataset)

    max_num_sentence = show_statisctic(doc_content_list)

    doc_train_list_original = []
    doc_test_list_original = []
    labels_dic = {}
    label_count = Counter()

    i = 0
    f = open('trydata/' + dataset + '_labels.txt', 'r')
    lines = f.readlines()
    for line in lines:
        temp = line.strip().split("\t")
        if temp[1].find('test') != -1:
            doc_test_list_original.append((doc_content_list[i], temp[2]))
        elif temp[1].find('train') != -1:
            doc_train_list_original.append((doc_content_list[i], temp[2]))
        if not temp[2] in labels_dic:
            labels_dic[temp[2]] = len(labels_dic)
        label_count[temp[2]] += 1
        i += 1

    f.close()
    print(label_count)

    word_freq = Counter()
    word_set = set()
    for doc_words in doc_content_list:
        for words in doc_words:
            for word in words:
                word_set.add(word)
                word_freq[word] += 1

    vocab = list(word_set)
    vocab_size = len(vocab)

    vocab_dic = {}
    for i in word_set:
        vocab_dic[i] = len(vocab_dic) + 1

    print('Total_number_of_words: ' + str(len(vocab)))
    print('Total_number_of_categories: ' + str(len(labels_dic)))

    doc_train_list = []
    doc_test_list = []

    for doc, label in doc_train_list_original:
        temp_doc = []
        for sentence in doc:
            temp = []
            for word in sentence:
                if word in vocab_dic:
                    temp.append(vocab_dic[word])
            if temp:
                temp_doc.append(temp)
        if temp_doc:
            doc_train_list.append((temp_doc, labels_dic[label]))

    for doc, label in doc_test_list_original:
        temp_doc = []
        for sentence in doc:
            temp = []
            for word in sentence:
                if word in vocab_dic:
                    temp.append(vocab_dic[word])
            if temp:
                temp_doc.append(temp)
        if temp_doc:
            doc_test_list.append((temp_doc, labels_dic[label]))

    keywords_dic = {}
    if LDA:
        keywords_dic_original = pickle.load(open('trydata/' + dataset + '_LDA.p', "rb"))

        for i in keywords_dic_original:
            if i in vocab_dic:
                keywords_dic[vocab_dic[i]] = keywords_dic_original[i]

    train_set_y = [j for i, j in doc_train_list]

    # Compute class weights using NLTK's class_weight
    class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(train_set_y), y=train_set_y)

    return doc_content_list, doc_train_list, doc_test_list, vocab_dic, labels_dic, max_num_sentence, keywords_dic, class_weights
