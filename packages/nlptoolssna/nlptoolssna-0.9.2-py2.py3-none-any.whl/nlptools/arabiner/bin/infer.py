import os
from collections import namedtuple
from nlptools.arabiner.utils.helpers import load_checkpoint
from nlptools.arabiner.utils.data import get_dataloaders, text2segments
from nlptools.DataDownload import downloader

def ner(text, batch_size=32):
    # Load tagger
    filename = 'Wj27012000.tar'
    path =downloader.get_appdatadir()
    model_path = os.path.join(path, filename)
    print('1',model_path)
    tagger, tag_vocab, train_config = load_checkpoint(model_path)

    # Convert text to a tagger dataset and index the tokens in args.text
    dataset, token_vocab = text2segments(text)

    vocabs = namedtuple("Vocab", ["tags", "tokens"])
    vocab = vocabs(tokens=token_vocab, tags=tag_vocab)

    # From the datasets generate the dataloaders
    dataloader = get_dataloaders(
        (dataset,),
        vocab,
        train_config.data_config,
        batch_size=batch_size,
        shuffle=(False,),
    )[0]
    # Perform inference on the text and get back the tagged segments
    segments = tagger.infer(dataloader)
    segments_lists = []
    # Print results
    for segment in segments:
        for token in segment:
            segments_list = []
            segments_list.append(token.text)
            #print([t['tag'] for t in token.pred_tag])
            list_of_tags = [t['tag'] for t in token.pred_tag]
            list_of_tags = [i for i in list_of_tags if i not in('O',' ','')]
            print(list_of_tags)
            if list_of_tags == []:
               segments_list.append(' '.join(['O']))
            else:
               segments_list.append(' '.join(list_of_tags))
            segments_lists.append(segments_list)         
    return segments_lists
    # # Perform inference on the text and get back the tagged segments
    # segments = tagger.infer(dataloader)

    # # Print results
    # output_result=""
    # for segment in segments:
    #     s = [
    #         f"{token.text} ({'|'.join([t['tag'] for t in token.pred_tag])})"
    #         for token in segment
    #         ]
    #     print(" ".join(s))
    #     output_result=" ".join(s)
    # return output_result

#Print results
    # for segment in segments:
    #     s = [
    #         (token.text, token.pred_tag[0]['tag'])
    #         for token in segment
    #         if token.pred_tag[0]['tag'] != 'O'
    #     ]
    #     print(", ".join([f"({token}, {tag})" for token, tag in s]))

