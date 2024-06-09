import json

with open(r'C:\Users\manas\Documents\gcn_research\HyperGAT_TextClassification-main\raw_files\bloom_split.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

data_list = [(index, v["text"], v["label"]) for index, (k, v) in enumerate(data["train"].items())]

split_index = int(0.7 * len(data_list))
train_data = data_list[:split_index]
test_data = data_list[split_index:]

with open(r'C:\Users\manas\Documents\gcn_research\HyperGAT_TextClassification-main\trydata\bloom_corpus.txt', 'w', encoding='utf-8') as data_file, open(r'C:\Users\manas\Documents\gcn_research\HyperGAT_TextClassification-main\trydata\bloom_labels.txt', 'w', encoding='utf-8') as label_file:
    for index, text, label in train_data:
        data_file.write(f"{text}\n")
        label_file.write(f"{index}\ttrain\t{label}\n")
    for index, text, label in test_data:
        data_file.write(f"{text}\n")
        label_file.write(f"{index}\ttest\t{label}\n")
